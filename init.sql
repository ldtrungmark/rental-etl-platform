CREATE DATABASE IF NOT EXISTS admin;
CREATE DATABASE IF NOT EXISTS airflow;

CREATE SCHEMA IF NOT EXISTS rental;

CREATE TABLE IF NOT EXISTS rental.account (
    account_id BIGINT PRIMARY KEY,
    account_name TEXT,
    full_name TEXT
);

CREATE TABLE IF NOT EXISTS rental.rental (
    list_id BIGINT PRIMARY KEY,
    account_id BIGINT REFERENCES rental.account(account_id),
    average_rating INT,
    category INT,
    category_name TEXT,
    list_time BIGINT,
    price BIGINT,
    size_unit INT,
    size_unit_string TEXT,
    type TEXT,
    area_name TEXT,
    region_name TEXT,
    address TEXT
);

--
-- drop table if exists rental.rental;
-- drop table if exists rental.account;