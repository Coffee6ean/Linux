-- Drop Database
DROP DATABASE IF EXISTS cpm_processor_db;

-- Create Database
CREATE DATABASE cpm_processor_db;

-- Connect to the Database
\c cpm_processor_db;

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
