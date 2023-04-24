FROM alpine

RUN apk add --no-cache postgresql postgresql-contrib &&\
    mkdir -p /var/run/postgresql &&\
    chown -R postgres:postgres /var/run/postgresql &&\
    chmod 2777 /var/run/postgresql &&\
    chown -R postgres:postgres /var/lib/postgresql

RUN apk add --no-cache bash su-exec

COPY ./ ./
RUN chmod 777 "db_init.sh"
RUN cp db_init.sh /usr/local/bin/db_init.sh

ENV PGDATA /var/lib/postgresql/data
RUN mkdir -p "$PGDATA" && chown -R postgres:postgres "$PGDATA" && chmod 777 "$PGDATA"

VOLUME /var/lib/postgresql/data
ENTRYPOINT ["db_init.sh"]

EXPOSE 5434
CMD ["postgres"]
