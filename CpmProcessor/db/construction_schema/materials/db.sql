-- Create a 'Materials' table
CREATE TABLE construction_schema.materials (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES construction_schema.projects(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    created_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    updated_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    type INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(25),
    notes TEXT,
    unit VARCHAR(20),
    unit_cost DECIMAL(12,2) CHECK (unit_cost >= 0),
    currency VARCHAR(3) DEFAULT 'USD',
    quantity DECIMAL(12,2) DEFAULT 0 CHECK (quantity >= 0),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
