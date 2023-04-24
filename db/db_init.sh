#!/usr/bin/env bash


if [ "$1" = 'postgres' ]; then
    mkdir -p "$PGDATA"
    chmod 700 "$PGDATA" || :
    
    mkdir -p /var/run/postgresql || :
	  chmod 775 /var/run/postgresql || :
    
    if [ "$(id -u)" = '0' ]; then
	    exec su-exec postgres "$BASH_SOURCE" "$@"
    fi
    
    if [ ! -s "$PGDATA/PG_VERSION" ]; then
        eval "initdb --username postgres -D $PGDATA"
        echo "host all all 0.0.0.0/0 md5" >> /var/lib/postgresql/data/pg_hba.conf
        echo "listen_addresses='*'" >> /var/lib/postgresql/data/postgresql.conf	
    fi

    POSTGRES_USER='postgres'
    PGUSER="${PGUSER:-POSTGRES_USER}"
    
    pg_ctl -D "$PGDATA" -w start

    psql -c "ALTER USER postgres PASSWORD 'postgres';"

    if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='satellite'" )" != '1' ]; then
        psql -c "CREATE DATABASE satellite OWNER postgres;"
        psql satellite < satellite.sql
    fi

    if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='iss_visibility'" )" != '1' ]; then
        psql -c "CREATE DATABASE iss_visibility OWNER postgres;"
        psql iss_visibility < iss_visibility.sql
    fi

    if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='responses'" )" != '1' ]; then
        psql -c "CREATE DATABASE responses OWNER postgres;"
        psql responses < responses.sql
    fi

    if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='airflow_db'" )" != '1' ]; then
        psql -c "CREATE DATABASE airflow_db;"
        psql -c "CREATE USER airflow_user WITH PASSWORD 'airflow_pass';"
        psql -c "GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;"
    fi

    pg_ctl stop

    exec "$@"
fi
