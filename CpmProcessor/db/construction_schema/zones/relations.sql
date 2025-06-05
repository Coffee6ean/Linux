-- shared_schema
-- Relate 'Colors' entity with 'Zone' entity (O:M)
CREATE TABLE construction_schema.colors2zone (
    color_id INTEGER REFERENCES shared_schema.colors(id) ON DELETE CASCADE,
    zone_id INTEGER REFERENCES construction_schema.zones(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (color_id, zone_id)
);

-- Relate 'Tags' entity with 'Zone' entity (O:M)
CREATE TABLE construction_schema.tags2zone (
    tag_id INTEGER REFERENCES shared_schema.tags(id) ON DELETE CASCADE,
    zone_id INTEGER REFERENCES construction_schema.zones(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (tag_id, zone_id)
);

-- construction_schema
-- Relate 'Zone' entity with 'Zone' entity (M:M)
CREATE TABLE construction_schema.zones2zones (
    id SERIAL PRIMARY KEY,
    related_zone_id INTEGER REFERENCES construction_schema.zones(id) ON DELETE CASCADE,
    zone_id INTEGER REFERENCES construction_schema.zones(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT no_self_reference CHECK (zone_id <> related_zone_id)
);

-- Relate 'Phases' entity with 'Zone' entity (O:M)
CREATE TABLE construction_schema.zones2phase (
    phase_id INTEGER REFERENCES construction_schema.phases(id) ON DELETE CASCADE,
    zone_id INTEGER REFERENCES construction_schema.zones(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (phase_id, zone_id)
);

-- Relate 'Areas' entity with 'Zone' entity (O:M)
CREATE TABLE construction_schema.zones2area (
    area_id INTEGER REFERENCES construction_schema.areas(id) ON DELETE CASCADE,
    zone_id INTEGER REFERENCES construction_schema.zones(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (area_id, zone_id)
);
