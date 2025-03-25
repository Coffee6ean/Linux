-- Create a 'Versions' polymorphic table
CREATE TABLE shared_schema.versions (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL, 
    major INTEGER NOT NULL DEFAULT 0,  -- Major version (breaking changes)
    minor INTEGER NOT NULL DEFAULT 0,  -- Minor version (new features)
    patch INTEGER NOT NULL DEFAULT 0,  -- Patch version (bug fixes)
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    changes JSONB,                     -- JSONB field for storing changes
    UNIQUE (entity_type, entity_id, major, minor, patch)  -- Ensure unique versions per entity
);
