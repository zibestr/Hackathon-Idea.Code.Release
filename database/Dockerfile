FROM postgres:16

RUN apt-get update && apt-get install -y postgresql-16-cron

COPY create_user.sql /docker-entrypoint-initdb.d/01_create_user.sql
COPY create_script.sql /docker-entrypoint-initdb.d/02_create_script.sql

# Настраиваем права
RUN chmod a+r /docker-entrypoint-initdb.d/*