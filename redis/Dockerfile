FROM redis:7.2-alpine

COPY redis.conf /usr/local/etc/redis/redis.conf

VOLUME /data

WORKDIR /data

EXPOSE 6379

CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
