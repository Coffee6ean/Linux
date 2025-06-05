-- Create a 'Users' table
CREATE TABLE auth_schema.users (
    id SERIAL PRIMARY KEY,
    created_by_entity_type VARCHAR(50), -- 'users', 'system', 'api_key'
    created_by_entity_id INTEGER,       -- ID in auth_schema.users, etc.
    updated_by_entity_type VARCHAR(50),
    updated_by_entity_id INTEGER,
    manager_id INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    role_id INTEGER REFERENCES auth_schema.roles(id) NOT NULL,
    name VARCHAR(30) NOT NULL,
    middle_name VARCHAR(30),
    last_name VARCHAR(30) NOT NULL,
    birth_date DATE,
    picture TEXT,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    about TEXT,
    profession VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
