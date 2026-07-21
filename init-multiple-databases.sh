#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE data_warehouse;
    CREATE USER dw_user WITH PASSWORD 'dw_pass';
    GRANT ALL PRIVILEGES ON DATABASE data_warehouse TO dw_user;
    
    \c data_warehouse
    GRANT ALL ON SCHEMA public TO dw_user;
EOSQL
