-- Создание базы данных (если не существует)
CREATE DATABASE IF NOT EXISTS analytics_service;

-- Переключение на целевую БД
USE analytics_service;

-- Таблица user_views
CREATE TABLE IF NOT EXISTS user_views (
    user_id Int32,
    viewed_user_id Int32,
    created_at DateTime DEFAULT now(),
    INDEX user_id_idx user_id TYPE minmax GRANULARITY 3,
    INDEX viewed_user_idx viewed_user_id TYPE minmax GRANULARITY 3
) ENGINE = MergeTree()
ORDER BY (user_id, viewed_user_id, created_at);

-- Таблица habitation_views
CREATE TABLE IF NOT EXISTS habitation_views (
    user_id Int32,
    viewed_habitation_id Int32,
    created_at DateTime DEFAULT now(),
    INDEX user_id_idx user_id TYPE minmax GRANULARITY 3,
    INDEX habitation_idx viewed_habitation_id TYPE minmax GRANULARITY 3
) ENGINE = MergeTree()
ORDER BY (user_id, viewed_habitation_id, created_at);

-- Таблица user_filter_ei
CREATE TABLE IF NOT EXISTS user_filter_ei (
    user_id Int32,
    filtered_ei_id Int32,
    created_at DateTime DEFAULT now(),
    INDEX user_id_idx user_id TYPE bloom_filter(0.025) GRANULARITY 3,
    INDEX ei_idx filtered_ei_id TYPE bloom_filter(0.025) GRANULARITY 3
) ENGINE = MergeTree()
ORDER BY (user_id, filtered_ei_id, created_at);

-- Таблица user_filter_locality
CREATE TABLE IF NOT EXISTS user_filter_locality (
    user_id Int32,
    filtered_locality_id Int32,
    created_at DateTime DEFAULT now(),
    INDEX user_id_idx user_id TYPE bloom_filter(0.025) GRANULARITY 3,
    INDEX locality_idx filtered_locality_id TYPE bloom_filter(0.025) GRANULARITY 3
) ENGINE = MergeTree()
ORDER BY (user_id, filtered_locality_id, created_at);
