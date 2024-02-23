-- Drop existing table if exists
DROP TABLE IF EXISTS projects;

-- Create a 'Projects' table with additional columns
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    description TEXT,
    link TEXT,
    topic TEXT,
    board TEXT,
    -- Entity associated with this file
    entity_id INTEGER REFERENCES entities(id)
);
