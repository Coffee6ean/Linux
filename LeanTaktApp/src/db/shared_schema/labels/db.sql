-- Create a 'Lables' table
CREATE TABLE shared_schema.labels(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    entity_type VARCHAR(255) NOT NULL,  -- Type of label (e.g., User, Tenant, Project)
    type VARCHAR(255) NOT NULL,         -- Type of label (e.g., STATUS, PRIORITY, TYPE)
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_combination UNIQUE (name, entity_type, type)
);
