-- Create a 'Tags' table
CREATE TABLE shared_schema.tags (
    id SERIAL PRIMARY KEY,
    created_by_entity_type VARCHAR(50), -- 'users', 'system', 'api_key'
    created_by_entity_id INTEGER,       -- ID in auth_schema.users, etc.
    updated_by_entity_type VARCHAR(50),
    updated_by_entity_id INTEGER,
    name VARCHAR(255) NOT NULL UNIQUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
