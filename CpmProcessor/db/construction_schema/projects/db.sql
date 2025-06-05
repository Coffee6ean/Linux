-- Create a 'Projects' table 
CREATE TABLE construction_schema.projects (
    id SERIAL PRIMARY KEY,
    version_id INTEGER REFERENCES shared_schema.versions(id) NOT NULL,
    location_id INTEGER REFERENCES shared_schema.locations(id) ON DELETE SET NULL,
    created_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    updated_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    assignee_id INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    division INTEGER REFERENCES shared_schema.labels(id) NOT NULL,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(25) UNIQUE,
    notes TEXT,
    workweek VARCHAR(25),
    planned_start DATE,
    planned_finish DATE,
    actual_start DATE,
    actual_finish DATE,
    budget DECIMAL(12,2) CHECK (budget >= 0),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT valid_timeline CHECK (planned_start <= planned_finish)
);
