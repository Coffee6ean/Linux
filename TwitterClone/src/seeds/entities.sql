-- Drop existing tables if they exist
DROP TABLE IF EXISTS entities;
DROP TABLE IF EXISTS links;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS files;
DROP TABLE IF EXISTS pictures;
DROP TABLE IF EXISTS posts;

-- Create a 'Entity' table to manage relationships and common attributes
CREATE TABLE entities (
    id SERIAL PRIMARY KEY,
    -- Foreign key to link to the user who created the entity
    user_id INTEGER,                  
    -- Foreign key to link to the project associated with the entity  
    project_id INTEGER,     
    -- Foreign key to link to the board associated with the entity            
    board_id INTEGER,            
    -- Type of the entity (e.g., picture, file, task, link)       
    type VARCHAR(50) NOT NULL,   
    -- Name of the entity (optional)       
    name VARCHAR(255),            
    -- Content of the entity (optional)      
    content TEXT,          
    -- Picture URL of the entity (optional)             
    picture TEXT,                 
    -- Topic of the entity (optional)      
    topic VARCHAR(255),            
    -- Date stamp     
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create 'Files' table
CREATE TABLE files (
    id SERIAL PRIMARY KEY,
    -- Entity associated with this file
    entity_id INTEGER REFERENCES entities(id),  
    url TEXT,
    description TEXT
);

-- Create 'Links' table
CREATE TABLE links (
    id SERIAL PRIMARY KEY,
    -- Entity associated with this link
    entity_id INTEGER REFERENCES entities(id),  
    url TEXT,
    description TEXT
);

-- Create 'Pictures' table
CREATE TABLE pictures (
    id SERIAL PRIMARY KEY,
    -- Entity associated with this picture
    entity_id INTEGER REFERENCES entities(id),  
    url TEXT,
    description TEXT
);

-- Create the 'Posts' table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    -- Entity associated with this picture
    entity_id INTEGER REFERENCES entities(id),  
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    picture TEXT,
    topic VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create 'Tasks' table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    -- Entity associated with this task
    entity_id INTEGER REFERENCES entities(id),  
    task_description TEXT,
    completed BOOLEAN
);
