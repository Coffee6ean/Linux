-- shared_schema
-- Relate 'Areas' entity with 'Colors' entity (O:M)
CREATE TABLE construction_schema.colors2area (
    color_id INTEGER REFERENCES shared_schema.colors(id) ON DELETE CASCADE,
    area_id INTEGER REFERENCES construction_schema.areas(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (color_id, area_id)
);

-- Relate 'Areas' entity with 'Tags' entity (O:M)
CREATE TABLE construction_schema.tags2area (
    tag_id INTEGER REFERENCES shared_schema.tags(id) ON DELETE CASCADE,
    area_id INTEGER REFERENCES construction_schema.areas(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (tag_id, area_id)
);

-- construction_schema
-- Relate 'Area' entity with 'Area' entity (M:M)
CREATE TABLE construction_schema.areas2areas (
    id SERIAL PRIMARY KEY,
    related_area_id INTEGER REFERENCES construction_schema.areas(id) ON DELETE CASCADE,
    area_id INTEGER REFERENCES construction_schema.areas(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT no_self_reference CHECK (area_id <> related_area_id)
);

-- Relate 'Phases' entity with 'Area' entity (O:M)
CREATE TABLE construction_schema.areas2phase (
    phase_id INTEGER REFERENCES construction_schema.phases(id) ON DELETE CASCADE,
    area_id INTEGER REFERENCES construction_schema.areas(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (phase_id, area_id)
);
