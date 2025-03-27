-- Create a 'Colors' table
CREATE TABLE shared_schema.colors (
    id SERIAL PRIMARY KEY,
    created_by_entity_type VARCHAR(50), -- 'users', 'system', 'api_key'
    created_by_entity_id INTEGER,       -- ID in auth_schema.users, etc.
    updated_by_entity_type VARCHAR(50),
    updated_by_entity_id INTEGER,
    category VARCHAR(50) NOT NULL,  -- Category of the color (e.g., Brand, Error, Background)
    color_name VARCHAR(50),         -- Name of the color (e.g., Primary Blue, Error Red)
    hex_code CHAR(7) NOT NULL,      -- HEX code of the color (e.g., #1A73E8)
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
