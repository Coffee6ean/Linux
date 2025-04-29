-- shared_schema
-- Relate 'Phases' entity with 'Colors' entity (O:M)
CREATE TABLE construction_schema.colors2phase (
    color_id INTEGER REFERENCES shared_schema.colors(id) ON DELETE CASCADE,
    phase_id INTEGER REFERENCES construction_schema.phases(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (color_id, phase_id)
);

-- Relate 'Phases' entity with 'Colors' entity (O:M)
CREATE TABLE construction_schema.tags2phase (
    tag_id INTEGER REFERENCES shared_schema.tags(id) ON DELETE CASCADE,
    phase_id INTEGER REFERENCES construction_schema.phases(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (tag_id, phase_id)
);

-- construction_schema
-- Relate 'Phases' entity with 'Phases' entity (M:M)
CREATE TABLE construction_schema.phases2phases (
    related_phase_id INTEGER REFERENCES construction_schema.phases(id) ON DELETE CASCADE,
    phase_id INTEGER REFERENCES construction_schema.phases(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT no_self_reference CHECK (phase_id <> related_phase_id)
);
