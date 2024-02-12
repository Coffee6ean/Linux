-- Drop existing table if exists
DROP TABLE IF EXISTS users;

-- Create a 'User' table with additional columns
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
    profession VARCHAR(50),
    -- Entity associated with this file
    entity_id INTEGER REFERENCES entities(id)
);
