-- Create a 'Phases' table
CREATE TABLE cpm_schema.phases (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create a 'Areas' table
CREATE TABLE cpm_schema.areas (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(255),
    notes TEXT,
    size REAL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create a 'Zones' table
CREATE TABLE cpm_schema.zones (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(255),
    notes TEXT,
    size REAL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create a 'Trades' table
CREATE TABLE cpm_schema.trades (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    type VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE cpm_schema.activities (
    id SERIAL PRIMARY KEY,
    version_id INTEGER REFERENCES cpm_schema.versions(id) NOT NULL,
    project_id INTEGER REFERENCES cpm_schema.projects(id) ON DELETE CASCADE,
    phase_id INTEGER REFERENCES cpm_schema.phases(id) ON DELETE SET NULL,
    area_id INTEGER REFERENCES cpm_schema.areas(id) ON DELETE SET NULL,
    zone_id INTEGER REFERENCES cpm_schema.locations(id) ON DELETE SET NULL,
    trade_id INTEGER REFERENCES cpm_schema.trades(id) ON DELETE SET NULL,
    color VARCHAR(50),
    parent_id INTEGER REFERENCES cpm_schema.activities(id) ON DELETE SET NULL,
    code VARCHAR(50) UNIQUE,
    wbs_code VARCHAR(255) UNIQUE,
    name VARCHAR(255) NOT NULL,
    category_id INTEGER REFERENCES cpm_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES cpm_schema.labels(id) ON DELETE SET NULL,
    duration INTEGER,
    ins VARCHAR(50),
    start DATE NOT NULL,
    finish DATE NOT NULL,
    total_float INTEGER,
    predecessor_id INTEGER REFERENCES cpm_schema.activities(id) ON DELETE SET NULL
);
