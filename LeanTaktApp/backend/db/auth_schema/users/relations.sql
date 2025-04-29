-- Relate 'Versions' entity with 'Users' entity
CREATE TABLE auth_schema.versions2users (
    id SERIAL PRIMARY KEY,
    version_id INTEGER REFERENCES shared_schema.versions(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES auth_schema.users(id) ON DELETE CASCADE,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    created_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    updated_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Relate 'Users' entity with 'Teams' entity
CREATE TABLE auth_schema.users2teams (
    id SERIAL PRIMARY KEY,
    team_id INTEGER REFERENCES auth_schema.teams(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES auth_schema.users(id) ON DELETE CASCADE,
    created_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    updated_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Relate 'Users' entity with 'Tenants' entity
CREATE TABLE auth_schema.users2tenants (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES auth_schema.tenants(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES auth_schema.users(id) ON DELETE CASCADE,
    created_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    updated_by INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
