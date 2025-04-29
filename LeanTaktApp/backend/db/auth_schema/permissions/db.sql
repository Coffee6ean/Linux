-- Create a 'Permissions' table
CREATE TABLE auth_schema.permissions (
    id SERIAL PRIMARY KEY,
    created_by_entity_type VARCHAR(50), -- 'users', 'system', 'api_key'
    created_by_entity_id INTEGER,       -- ID in auth_schema.users, etc.
    updated_by_entity_type VARCHAR(50),
    updated_by_entity_id INTEGER,
    name VARCHAR(255) NOT NULL,  -- Name of the permission (e.g., CREATE, READ, UPDATE)
    entity_type VARCHAR(50) NOT NULL,   -- Type of entity (e.g., ROLES, USERS, TENANTS)
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (name, entity_type)
);
