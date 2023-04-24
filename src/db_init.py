import redis
import sqlalchemy

from constants import Const

dw_conn = sqlalchemy.create_engine(
    f"postgresql://{Const.POSTGRES_USER}:{Const.POSTGRES_PASS}@"
    f"{Const.POSTGRES_HOST}:{Const.POSTGRES_PORT}/{Const.DW_DB}")

psa_conn = sqlalchemy.create_engine(
    f"postgresql://{Const.POSTGRES_USER}:{Const.POSTGRES_PASS}@"
    f"{Const.POSTGRES_HOST}:{Const.POSTGRES_PORT}/{Const.PSA_DB}")

rclient = redis.Redis(host=Const.REDIS_HOST, port=Const.REDIS_PORT, db=0)
