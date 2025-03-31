-- shared_schema
-- Relate 'Materials' entity with 'Colors' entity (O:M)
CREATE TABLE construction_schema.colors2material (
    color_id INTEGER REFERENCES shared_schema.colors(id) ON DELETE CASCADE,
    material_id INTEGER REFERENCES construction_schema.materials(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (color_id, material_id)
);

-- Relate 'Materials' entity with 'Tags' entity (O:M)
CREATE TABLE construction_schema.tags2material (
    tag_id INTEGER REFERENCES shared_schema.tags(id) ON DELETE CASCADE,
    material_id INTEGER REFERENCES construction_schema.materials(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (tag_id, material_id)
);

-- construction_schema
-- Relate 'Materials' entity with 'Activities' entity (O:M)
CREATE TABLE construction_schema.materials2activity (
    tag_id INTEGER REFERENCES shared_schema.tags(id) ON DELETE CASCADE,
    material_id INTEGER REFERENCES construction_schema.materials(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (tag_id, material_id)
);
