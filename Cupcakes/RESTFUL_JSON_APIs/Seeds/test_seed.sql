-- Drop Database if exists
DROP DATABASE IF EXISTS cupcakes_test_db;

-- Create Database
CREATE DATABASE cupcakes_test_db;

-- Connect to DB
\c cupcakes_test_db;

-- Create Table for cupcakes
CREATE TABLE cupcakes (
    id SERIAL PRIMARY KEY,
    flavor TEXT NOT NULL,
    size TEXT NOT NULL,
    rating FLOAT,
    image TEXT DEFAULT 'https://tinyurl.com/demo-cupcake'
)