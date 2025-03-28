-- Create a 'Phases' table
CREATE TABLE construction_schema.phases (
    id SERIAL PRIMARY KEY,
    version_id INTEGER REFERENCES shared_schema.versions(id) NOT NULL,
    project_id INTEGER REFERENCES construction_schema.projects(id) ON DELETE CASCADE,
    created_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    updated_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    display_order INTEGER NOT NULL CHECK (display_order >= 0),
    planned_start DATE,
    planned_end DATE,
    actual_start DATE,
    actual_end DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
