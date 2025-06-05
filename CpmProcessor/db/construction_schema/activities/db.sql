-- Create a 'Activities' table
CREATE TABLE construction_schema.activities (
    id SERIAL PRIMARY KEY,
    version_id INTEGER REFERENCES shared_schema.versions(id) ON DELETE SET NULL,
    project_id INTEGER REFERENCES construction_schema.projects(id) ON DELETE CASCADE,
    created_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    updated_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    type INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    display_order INTEGER CHECK (display_order >= 0),
    code VARCHAR(50),
    wbs_code VARCHAR(50) UNIQUE,
    name VARCHAR(255) NOT NULL,
    notes TEXT,
    duration INTEGER,
    start DATE NOT NULL,
    finish DATE NOT NULL,
    total_float INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT valid_timeline CHECK (start <= finish)
);
