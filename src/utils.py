import json
import os
import time
from functools import wraps

import aiohttp
import pandas as pd

from db_init import dw_conn


def transform(df: pd.DataFrame):
    """
    Transforms raw data before inserting into the warehouse

    :param df: pandas DataFrame to process
    :return: processed DataFrame
    """

    df = pd.concat([df.drop("response", axis=1),
                    df["response"].apply(json.loads).apply(pd.Series).
                   drop(["units", "id", "name"], axis=1)],
                   axis=1)

    df = df.rename(columns={"velocity": "velocity_km"})

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

    return df


def validate(data: list):
    """
    Validates data to match the expected schema from the database, represented
    as a DataFrame-able object(lists, dicts, dataframes...)

    :param data: data to validate
    :return: returns a tuple of two dataframes, valid and invalid rows
    """
    df = pd.DataFrame(data)
    df = transform(df)

    df_invalid_list = df[df.isnull().any(axis=1)].to_dict(orient="records")
    df_invalid = pd.DataFrame([json.loads(row) for row in df_invalid_list])

    df_valid = df[df.notnull().all(axis=1)]
    valid_columns = dw_conn.execute("SELECT * FROM iss25544 LIMIT 0;").keys()
    df_valid = df_valid[valid_columns]

    return df_valid, df_invalid


def data_quality(conn):
    """
    Generates a small data quality report about rows, storage, data lost
    in quality_report.txt file

    :param conn: SQLAlchemy connection/engine or sqlite3 connection
    """

    total_psa = pd.read_json("all.json", lines=True)
    total_db = pd.read_sql('iss25544', conn)

    total_db = total_db.drop("id", axis=1)
    total_psa = transform(total_psa)

    total_psa.to_json(".tmpjson", orient="records")
    total_db.to_json(".tmpdb", orient="records")

    psa_storage = os.path.getsize(".tmpjson")
    db_storage = os.path.getsize(".tmpdb")

    psa_size = len(total_psa)
    db_size = len(total_db)
    psa_mb = round(psa_storage / 1024)
    db_mb = round(db_storage / 1024)

    os.remove(".tmpjson")
    os.remove(".tmpdb")

    lost_pct = round(100 - (db_size / psa_size) * 100, 2)
    with open("quality_report.txt", "w") as f:
        f.write(f"Incoming Data: {psa_mb}KB | {psa_size} Rows\n")
        f.write(f"DW Data: {db_mb}KB | {db_size} Rows\n")
        f.write(f"{lost_pct}% of Data lost in ETL")


def backoff(max_tries, initial_wait):
    """
    Exponential backoff decorator

    :param max_tries: maximum number of tries
    :param initial_wait: initial wait time
    """

    def decorator(fn):
        @wraps(fn)
        def backoff_fn(*args, **kwargs):
            cur_tries = 1

            while cur_tries <= max_tries:
                try:
                    return fn(*args, **kwargs)
                except:
                    print(f"Function {fn.__name__} failed, retrying")
                    delay = (2 ** cur_tries) * initial_wait
                    time.sleep(delay)

                cur_tries += 1

        return backoff_fn

    return decorator


async def fetch_data(url: str, params=None, max_tries=5, initial_wait=1):
    """
    Fetch current data from the url

    :param url: url to fetch data from
    :param params: parameters for the request
    :param max_tries: maximum tries of api calls in case of errors
    :param initial_wait: initial wait time
    """

    params = [] if params is None else params

    @backoff(max_tries, initial_wait)
    async def fetch():
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()
                return data

    return await fetch()
