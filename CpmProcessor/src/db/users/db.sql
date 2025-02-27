-- Create a 'Teams' table
CREATE TABLE cpm_schema.teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create a 'Users' table
CREATE TABLE cpm_schema.users (
    id SERIAL PRIMARY KEY,
    version_id INTEGER REFERENCES cpm_schema.versions(id) NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    middle_name VARCHAR(30),
    last_name VARCHAR(30) NOT NULL,
    birth_date DATE,
    picture TEXT,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    about TEXT,
    role VARCHAR(255) NOT NULL,
    status_id INTEGER REFERENCES cpm_schema.labels(id) ON DELETE SET NULL,
    profession VARCHAR(50),
    team_id INTEGER REFERENCES cpm_schema.teams(id) ON DELETE SET NULL,
    manager_id INTEGER REFERENCES cpm_schema.users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
