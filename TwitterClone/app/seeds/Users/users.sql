-- Drop existing users table if it exists
DROP TABLE IF EXISTS users;

-- Create a new users table with additional columns
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    banner TEXT,
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
    linked_in TEXT,
    role VARCHAR(20),
    profession VARCHAR(50)
);

-- Create Pictures table
CREATE TABLE pictures (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    url TEXT,
    description TEXT
);

-- Create Files table
CREATE TABLE files (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    url TEXT,
    description TEXT
);

-- Create Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    task_description TEXT,
    completed BOOLEAN
);

-- Create Links table
CREATE TABLE links (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    url TEXT,
    description TEXT
);
