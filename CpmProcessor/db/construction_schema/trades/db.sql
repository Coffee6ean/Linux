-- Create a 'Trades' table
CREATE TABLE construction_schema.trades (
    id SERIAL PRIMARY KEY,
    version_id INTEGER REFERENCES shared_schema.versions(id) ON DELETE SET NULL,
    project_id INTEGER REFERENCES construction_schema.projects(id) ON DELETE CASCADE,
    created_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    updated_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    display_order INTEGER CHECK (display_order >= 0),
    code VARCHAR(20) NOT NULL,
    name VARCHAR(255) NOT NULL,
    notes TEXT,
    lead_time INTEGER CHECK (lead_time >= 0),
    crew_size INTEGER CHECK (crew_size > 0),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
  