-- Drop existing table if exists
DROP TABLE IF EXISTS boards;

-- Create a 'Boards' table with additional columns
CREATE TABLE boards (
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    description TEXT,
    topic TEXT,
    board TEXT,
    -- Entity associated with this file
    entity_id INTEGER REFERENCES entities(id)
);
