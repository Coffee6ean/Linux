-- Create a 'Types' table 
CREATE TABLE cpm_schema.types(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create a 'Tags' table 
CREATE TABLE cpm_schema.locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(255),
    size REAL,
    notes TEXT,
    coordinates VARCHAR(255),
    wheather VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create a 'Tags' table 
CREATE TABLE cpm_schema.tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Create a 'Projects' table 
CREATE TABLE cpm_schema.projects (
    id SERIAL PRIMARY KEY,
    version_id INTEGER REFERENCES cpm_schema.versions(id) NOT NULL,
    client_id INTEGER REFERENCES cpm_schema.clients(id) ON DELETE CASCADE,
    division VARCHAR(255),
    type_id INTEGER REFERENCES cpm_schema.types(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(25),
    notes TEXT,
    workweek VARCHAR(50),
    billing_address TEXT,
    payment_terms TEXT,
    location_id INTEGER REFERENCES cpm_schema.locations(id),
    assignee_id INTEGER REFERENCES cpm_schema.users(id),
    status_id INTEGER REFERENCES cpm_schema.labels(id) ON DELETE SET NULL,
    start DATE,
    finish DATE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_project_name_per_client UNIQUE (client_id, name)  -- Corrected UNIQUE constraint
);
