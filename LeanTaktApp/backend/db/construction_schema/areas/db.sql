-- Create a 'Areas' table
CREATE TABLE construction_schema.areas (
    id SERIAL PRIMARY KEY,
    version_id INTEGER REFERENCES shared_schema.versions(id) ON DELETE SET NULL,
    project_id INTEGER REFERENCES construction_schema.projects(id) ON DELETE CASCADE,
    created_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    updated_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    display_order INTEGER CHECK (display_order >= 0),
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50),
    planned_start DATE,
    planned_end DATE,
    actual_start DATE,
    actual_end DATE,
    size REAL CHECK (size > 0),
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
