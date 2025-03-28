CREATE USER hackathonshik WITH PASSWORD 'g01da_p0wer!';

-- Назначение прав на базу данных
GRANT CONNECT, TEMPORARY ON DATABASE neighbor_service TO hackathonshik;

-- Подключение к целевой БД
\connect neighbor_service;

-- Полные права на все ТАБЛИЦЫ в схеме public
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hackathonshik;

-- Полные права на все ПОСЛЕДОВАТЕЛЬНОСТИ в схеме public
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO hackathonshik;

-- Права на будущие объекты
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
    GRANT ALL PRIVILEGES ON TABLES TO hackathonshik;

ALTER DEFAULT PRIVILEGES IN SCHEMA public 
    GRANT ALL PRIVILEGES ON SEQUENCES TO hackathonshik;

-- Права на выполнение функций (если используются)
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
    GRANT EXECUTE ON FUNCTIONS TO hackathonshik;