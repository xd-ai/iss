# ISS

## Setting up

After cloning the repository, make sure create necessary folders and update permissions  
for the project files and directories so airflow runs successfully

```shell
$ cd iss
$ mkdir logs scripts files
$ chmod -R 777 logs scripts files 
```

We need to manually create and give permissions to those directories as the ones  
created automatically by docker will be lacking the permissions.  
Then we can start the service

```shell
$ docker-compose up
```

## Caveats

The postgres instance takes some seconds to be initialized, which is why the cron job will not start immediately, as
you'll see. It will instead wait for a successful health check from the database container using the `pg_isready` tool
provided by postgres.

Same goes for the airflow-init image which initializes databases for airflow  
thus the scheduler and the webserver will take time to start, on the first run.

New data from Redis to PSQL will be written by an Airflow DAG.  
Default host port for airflow is 8181, specified in docker-compose.yaml file  
Default login credentials for Airflow is user `admin` with password `admin`

Default host port for PSQL is 5434  
Default host port for Redis is 6379

Warnings from Pip about package versions can be safely ignored