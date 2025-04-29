-- Create a 'Lables' table
CREATE TABLE shared_schema.labels(
    id SERIAL PRIMARY KEY,
    created_by_entity_type VARCHAR(50), -- 'users', 'system', 'api_key'
    created_by_entity_id INTEGER,       -- ID in auth_schema.users, etc.
    updated_by_entity_type VARCHAR(50),
    updated_by_entity_id INTEGER,
    name VARCHAR(255) NOT NULL,
    entity_type VARCHAR(255) NOT NULL,  -- Type of entity (e.g., User, Tenant, Project)
    type VARCHAR(255) NOT NULL,         -- Type of label (e.g., STATUS, PRIORITY, TYPE)
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT unique_combination UNIQUE (name, entity_type, type)
);
