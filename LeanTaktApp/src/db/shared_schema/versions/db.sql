CREATE TABLE shared_schema.versions (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,   -- 'projects', 'contracts', etc.
    entity_id INTEGER NOT NULL,         -- ID in the target table
    created_by_entity_type VARCHAR(50), -- 'users', 'system', 'api_key'
    created_by_entity_id INTEGER,       -- ID in auth_schema.users, etc.
    updated_by_entity_type VARCHAR(50),
    updated_by_entity_id INTEGER,
    name VARCHAR(255) NOT NULL,         -- Human-readable title for the version (e.g., "Initial Release")
    major INTEGER NOT NULL DEFAULT 0 CHECK (major >= 0),
    minor INTEGER NOT NULL DEFAULT 0 CHECK (minor >= 0),
    patch INTEGER NOT NULL DEFAULT 0 CHECK (patch >= 0),
    changes JSONB,                      -- Store diffs/audit logs
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (entity_type, entity_id, major, minor, patch)  -- Unique versions per entity
);
