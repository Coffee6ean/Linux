-- shared_schema
-- Relate 'Colors' entity with 'Projects' entity (O:M)
CREATE TABLE construction_schema.colors2project (
    color_id INTEGER REFERENCES shared_schema.colors(id) ON DELETE CASCADE,
    project_id INTEGER REFERENCES construction_schema.projects(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (color_id, project_id)
);

-- Relate 'Tags' entity with 'Projects' entity (O:M)
CREATE TABLE construction_schema.tags2project (
    tag_id INTEGER REFERENCES shared_schema.tags(id) ON DELETE CASCADE,
    project_id INTEGER REFERENCES construction_schema.projects(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (tag_id, project_id)
);

-- construction_schema
-- Relate 'Tenants' entity with 'Projects' entity (O:M)
CREATE TABLE construction_schema.projects2tenant (
    tenant_id INTEGER REFERENCES auth_schema.tenants(id) ON DELETE CASCADE,
    project_id INTEGER REFERENCES construction_schema.projects(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (tenant_id, project_id)
);

-- Relate 'Teams' entity with 'Projects' entity (O:M)
CREATE TABLE construction_schema.projects2team (
    team_id INTEGER REFERENCES auth_schema.teams(id) ON DELETE CASCADE,
    project_id INTEGER REFERENCES construction_schema.projects(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (team_id, project_id)
);
