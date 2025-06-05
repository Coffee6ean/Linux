-- Create a 'Teams' table 
CREATE TABLE auth_schema.teams (
    id SERIAL PRIMARY KEY,
    version_id INTEGER REFERENCES shared_schema.versions(id) NOT NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    location_id INTEGER REFERENCES shared_schema.locations(id) ON DELETE SET NULL,
    created_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    updated_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL UNIQUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
