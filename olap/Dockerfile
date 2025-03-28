# Используем официальный образ ClickHouse
FROM clickhouse/clickhouse-server:23.8-alpine

# Копируем конфигурационные файлы
COPY config.xml /etc/clickhouse-server/config.d/custom.xml
COPY init.sql /docker-entrypoint-initdb.d/init.sql

# Настраиваем права
RUN chmod a+r /etc/clickhouse-server/config.d/custom.xml \
    && chmod a+r /docker-entrypoint-initdb.d/init.sql