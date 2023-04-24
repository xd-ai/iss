import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import pandas as pd

from constants import Const
from db_init import dw_conn, rclient, psa_conn
from helpers import write_psa_redis
from utils import fetch_data
from utils import transform, validate

executor = ThreadPoolExecutor(max_workers=4)


def recover_dw():
    """
    Recovers missing data from all.json to the database
    """

    df_psa = pd.read_sql(Const.PSA_RAW_TABLE, psa_conn)
    df_psa = df_psa.drop_duplicates()
    df_psa["timestamp"] = df_psa["response"].apply(json.loads). \
        apply(pd.Series)["timestamp"]

    df_dw = pd.read_sql(Const.DW_ISS_TABLE, dw_conn)

    # Get the date from which mismatch happens
    df_psa = df_psa.sort_values("timestamp", ascending=True)
    df_dw = df_dw.sort_values("timestamp", ascending=True)

    if len(df_dw) == 0:
        last_match_index = 0
    else:
        dw_last = df_dw.iloc[-1]
        last_match = df_psa.index[df_psa["timestamp"] == dw_last["timestamp"]]

        # data warehouse is up-to-date
        if len(last_match) == 0 or last_match[0] == len(df_psa) - 1:
            return "OK"

        last_match_index = last_match[0]

    df_psa = df_psa.drop("timestamp", axis=1)

    df_missing = df_psa[last_match_index + 1:]
    df_missing = transform(df_missing)

    df_valid, df_invalid = validate(df_missing)
    df_valid.to_sql(Const.DW_ISS_TABLE,
                    dw_conn,
                    if_exists="append",
                    index=False)

    df_invalid = df_invalid["id"].join(df_missing[["id"], ["response"]],
                                       on="id")

    df_invalid.to_sql(Const.PSA_FAILED_TABLE,
                      psa_conn,
                      if_exists="append",
                      index=False)


async def fetch_old(params, event_loop):
    """
    Fetches and stores old missing data to redis storage

    :param params: get request parameters in format:
                    { "timestamps" : [164803123, 164803124...] }
                   with a maximum of 10 elements in the list
    :param event_loop: asyncio event loop
    """

    data = await fetch_data(Const.URL_OLD, params=params)
    event_loop.run_in_executor(executor, write_psa_redis, data)

    return "OK"


async def recover_psa(event_loop):
    """
    Recover missing data to all.json by retrieving old from the API

    :param event_loop: asyncio event loop
    """

    time_to = datetime.utcnow().replace(microsecond=0)

    # Epoch values for the same date differ for built-in/pandas timestamps
    # Insert time to a temporary dataframe for accuracy
    tmp_df = pd.DataFrame([{"timestamp": time_to}])

    # pandas dataframe stores timestamp in nanoseconds
    # so divide by 10^9 for seconds
    time_to_pd = tmp_df["timestamp"][0].value // 1e9
    time_from = rclient.json().get(rclient.dbsize() - 1, '.timestamp')

    seconds_diff = int(time_to_pd) - int(time_from)

    timestamps = [time_from + n + 1 for n in range(seconds_diff)]

    timestamps_str = [str(date) for date in timestamps]

    # API accepts at max 10 timestamps at once
    params_all = [timestamps_str[i:i + 10] for i in range(0, seconds_diff, 10)]
    for params in params_all:
        # convert timestamps to the acceptable API parameter type(comma delim)
        asyncio.ensure_future(
            fetch_old({"timestamps": ",".join(params)}, event_loop))
        await asyncio.sleep(1)

    return "OK"


async def recover(event_loop):
    """
    Recovers missing data from API to PSA and from PSA to DW

    :param event_loop: asyncio event loop
    """

    await recover_psa(event_loop)
    recover_dw()

    return "OK"


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(recover(loop))
