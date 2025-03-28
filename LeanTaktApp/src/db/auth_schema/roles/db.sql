-- Create a 'Roles' table
CREATE TABLE auth_schema.roles (
    id SERIAL PRIMARY KEY,
    created_by_entity_type VARCHAR(50), -- 'users', 'system', 'api_key'
    created_by_entity_id INTEGER,       -- ID in auth_schema.users, etc.
    updated_by_entity_type VARCHAR(50),
    updated_by_entity_id INTEGER,
    name VARCHAR(255) NOT NULL,          -- Role title (e.g., ADMIN, SUPER-USER, USER)
    is_internal BOOLEAN NOT NULL DEFAULT FALSE, -- Boolean value to check for internal entities
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (name, is_internal)
);
