import json

import pandas as pd
from sqlalchemy import TIMESTAMP

from constants import Const
from db_init import rclient, psa_conn, dw_conn
from utils import transform, validate


def write_dw(data: list):
    """
    Writes data to the database

    :param data: DataFrame-able object(lists, dicts, dataframes...)
    """

    try:
        df_valid, df_invalid = validate(data)
        df_valid.to_sql(Const.DW_ISS_TABLE, dw_conn, if_exists='append',
                        dtype={"timestamp": TIMESTAMP}, index=False)

        df_invalid.to_sql(Const.PSA_FAILED_TABLE, psa_conn, if_exists='append',
                          dtype={"timestamp": TIMESTAMP}, index=False)
        return "OK"
    except:
        return "Invalid data"


def write_psa_redis(data: list):
    """
    Dumps a list of json objects(dicts) into the redis storage

    :param data: data to write
    """

    for obj in data:
        try:
            rclient.json().set(rclient.dbsize(), ".", obj)
        except:
            print("Invalid data to redis")


def write_psa_sql(data: list):
    """
    Dumps a list of json objects(dicts) into the postgres database

    :param data: data to write
    """

    data = [{k: json.dumps(v) for k, v in e.items()} for e in data]

    for obj in data:
        try:
            df = pd.DataFrame([obj])
            df.to_sql(Const.PSA_RAW_TABLE, psa_conn,
                      if_exists="append", index=False)
        except:
            print("Invalid data to psql")
