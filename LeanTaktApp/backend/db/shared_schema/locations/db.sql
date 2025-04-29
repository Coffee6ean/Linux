-- Create a 'Locations' table
CREATE TABLE shared_schema.locations (
    id SERIAL PRIMARY KEY,
    created_by_entity_type VARCHAR(50), -- 'users', 'system', 'api_key'
    created_by_entity_id INTEGER,       -- ID in auth_schema.users, etc.
    updated_by_entity_type VARCHAR(50),
    updated_by_entity_id INTEGER,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(255),
    size REAL,
    notes TEXT,
    coordinates VARCHAR(255),
    weather VARCHAR(255),
    address TEXT,
    postal_code VARCHAR(20),
    city VARCHAR(255),
    state VARCHAR(255),
    country VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
