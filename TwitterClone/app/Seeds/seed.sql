-- Drop Database
DROP DATABASE IF EXISTS twitter_clone_db;

-- Create Database
CREATE DATABASE twitter_clone_db;

-- Connect to the Database
\c twitter_clone_db

-- Create a user table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    picture TEXT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    first_name VARCHAR(30),
    sur_name VARCHAR(30),
    last_name VARCHAR(30),
    birth_date DATE NOT NULL,
    about TEXT,
    pronouns TEXT,
    website TEXT,
    linked_in TEXT
);

-- Create a boards table
CREATE TABLE boards (
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    description TEXT,
    topic TEXT,
    board TEXT,
    user_id INTEGER REFERENCES users(id)
);

-- Create a posts table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    picture TEXT,
    topic VARCHAR(255),
    user_id INTEGER REFERENCES users(id),
    board_id INTEGER REFERENCES boards(id)
);

-- Create a projects table
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    description TEXT,
    link TEXT,
    topic TEXT,
    board TEXT,
    user_id INTEGER REFERENCES users(id)
);

-- Create association tables
CREATE TABLE user_board_association (
    user_id INTEGER REFERENCES users(id),
    board_id INTEGER REFERENCES boards(id)
);

CREATE TABLE user_project_association (
    user_id INTEGER REFERENCES users(id),
    project_id INTEGER REFERENCES projects(id)
);
