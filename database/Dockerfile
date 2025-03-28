FROM postgres:15-alpine

# Копируем скрипты инициализации
COPY create_user.sql /docker-entrypoint-initdb.d/01_create_user.sql
COPY create_script.sql /docker-entrypoint-initdb.d/02_create_script.sql

# Настраиваем права
RUN chmod a+r /docker-entrypoint-initdb.d/*