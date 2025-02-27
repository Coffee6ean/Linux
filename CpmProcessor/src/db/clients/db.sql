-- Create a 'Labels' table
CREATE TABLE cpm_schema.labels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    type VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create a 'Clients' table 
CREATE TABLE cpm_schema.clients (
    id SERIAL PRIMARY KEY,
    version_id INTEGER REFERENCES cpm_schema.versions(id) NOT NULL,
    name VARCHAR(255) NOT NULL UNIQUE,
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(50),
    notes TEXT,
    status_id INTEGER REFERENCES cpm_schema.labels(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create a 'Contacts' table 
CREATE TABLE cpm_schema.contacts (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES cpm_schema.clients(id) NOT NULL,
    name VARCHAR(255) NOT NULL UNIQUE,   
    email VARCHAR(255),
    phone VARCHAR(255),
    role VARCHAR(255),
    status_id INTEGER REFERENCES cpm_schema.labels(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);