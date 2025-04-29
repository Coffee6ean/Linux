-- Drop Database
DROP DATABASE IF EXISTS lean_takt_db;

-- Create Database
CREATE DATABASE lean_takt_db;

-- Connect to the Database
\c lean_takt_db;

-- Drop Schemas
DROP SCHEMA IF EXISTS system_schema;
DROP SCHEMA IF EXISTS auth_schema;
DROP SCHEMA IF EXISTS shared_schema;
DROP SCHEMA IF EXISTS construction_schema;

-- Create schemas
CREATE SCHEMA system_schema;
CREATE SCHEMA shared_schema;
CREATE SCHEMA auth_schema;
CREATE SCHEMA construction_schema;

-- Call on other files to generate data pool
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/system_schema/init.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/shared_schema/init.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/auth_schema/init.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/construction_schema/init.sql;
