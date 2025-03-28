-- Create a 'Zones' table
CREATE TABLE construction_schema.zones (
    id SERIAL PRIMARY KEY,
    version_id INTEGER REFERENCES shared_schema.versions(id) NOT NULL,
    project_id INTEGER REFERENCES construction_schema.projects(id) ON DELETE CASCADE,
    created_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    updated_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    display_order INTEGER CHECK (display_order >= 0),
    name VARCHAR(255) NOT NULL,
    notes TEXT,
    size REAL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
