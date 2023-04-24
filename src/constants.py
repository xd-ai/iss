class Const:
    POSTGRES_HOST = 'db'
    POSTGRES_PORT = '5432'
    POSTGRES_USER = 'postgres'
    POSTGRES_PASS = 'postgres'

    REDIS_HOST = "redis"
    REDIS_PORT = "6379"

    SATELLITE_NAME = 'iss'
    SATELLITE_ID = '25544'
    URL = "https://api.wheretheiss.at/v1/satellites/25544"
    URL_OLD = "https://api.wheretheiss.at/v1/satellites/25544/positions"
    TIME_FORMAT = "%Y%m%d_%H.%M"
    DW_DB = 'satellite'
    MART_DB = 'iss_visibility'
    PSA_DB = 'responses'
    DW_ISS_TABLE = SATELLITE_NAME + SATELLITE_ID
    PSA_RAW_TABLE = 'raw'
    PSA_FAILED_TABLE = 'failed'
