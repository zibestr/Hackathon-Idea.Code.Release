FROM postgres:16

RUN apt-get update && apt-get install -y postgresql-16-cron

COPY create_script.sql /docker-entrypoint-initdb.d/01_create_script.sql
COPY migration.sql /docker-entrypoint-initdb.d/02_migration.sql
COPY create_user.sql /docker-entrypoint-initdb.d/03_create_user.sql

# Настраиваем права
RUN chmod a+r /docker-entrypoint-initdb.d/*