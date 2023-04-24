import asyncio
import json
import select
from concurrent.futures import ThreadPoolExecutor

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from constants import Const
from db_init import rclient, psa_conn
from helpers import write_dw, write_psa_redis, write_psa_sql
from recover import recover
from utils import fetch_data

executor = ThreadPoolExecutor(max_workers=7)


def psa_to_dw():
    """
    Listens to the postgres psa and writes new rows to the warehouse
    """

    listener = psycopg2.connect(database=Const.PSA_DB,
                                user=Const.POSTGRES_USER,
                                password=Const.POSTGRES_PASS,
                                host=Const.POSTGRES_HOST,
                                port=Const.POSTGRES_PORT)

    listener.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = listener.cursor()
    cur.execute("LISTEN new_row;")

    while True:
        # wait for data
        select.select([listener], [], [])
        listener.poll()

        while listener.notifies:
            notification = listener.notifies.pop()
            row_id = notification.payload
            data = rclient.json().get(row_id, ".")
            write_dw([{"id": row_id, "response": json.dumps(data)}])


async def fetch_new():
    """
    Fetches current data from the API and writes to redis storage with executor
    """

    data = await fetch_data(Const.URL)
    loop.run_in_executor(executor, write_psa_redis, [data])

    return "OK"


def update_psql():
    """
    Writes new data from redis to Postgres database
    """

    latest_redis = rclient.dbsize() - 1
    latest_psql = psa_conn.execute("SELECT MAX(id) FROM raw;").fetchone()[0]
    print(latest_psql)
    data = []
    for i in range(latest_redis - latest_psql):
        data.append({"id": latest_redis - i,
                     "response": rclient.json().get(latest_redis - i)})

    write_psa_sql(data)

    return "OK"


async def main():
    """
    Main program loop: recover missing data after the previous run
                       write new second data to all.json and from it to db
                       write new minute data to separate json files
    """

    # asyncio.ensure_future(recover(loop))
    asyncio.ensure_future(loop.run_in_executor(executor, psa_to_dw))

    while True:
        for i in range(60):
            asyncio.ensure_future(fetch_new())
            await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
