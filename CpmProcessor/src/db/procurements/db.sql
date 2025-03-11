-- Create a 'Procurements' table 
CREATE TABLE cpm_schema.procurements (
    id SERIAL PRIMARY KEY,
    version_id INTEGER REFERENCES cpm_schema.versions(id) NOT NULL,
    project_id INTEGER REFERENCES cpm_schema.projects(id) ON DELETE CASCADE,
    phase_id INTEGER REFERENCES cpm_schema.phases(id) ON DELETE SET NULL,
    area_id INTEGER REFERENCES cpm_schema.areas(id) ON DELETE SET NULL,
    zone_id INTEGER REFERENCES cpm_schema.locations(id) ON DELETE SET NULL,
    trade_id INTEGER REFERENCES cpm_schema.trades(id) ON DELETE SET NULL,
    color VARCHAR(50),
    code VARCHAR(50) UNIQUE,
    wbs_code VARCHAR(255) UNIQUE,
    name VARCHAR(255) NOT NULL,
    category_id INTEGER REFERENCES cpm_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES cpm_schema.labels(id) ON DELETE SET NULL,
    duration INTEGER,
    start DATE NOT NULL,
    finish DATE NOT NULL,
    total_float INTEGER,
    predecessor_id INTEGER REFERENCES cpm_schema.procurements(id) ON DELETE SET NULL
);
