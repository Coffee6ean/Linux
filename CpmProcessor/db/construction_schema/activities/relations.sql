-- shared_schema
-- Relate 'Acticities' entity with 'Colors' entity (O:M)
CREATE TABLE construction_schema.colors2activity (
    color_id INTEGER REFERENCES shared_schema.colors(id) ON DELETE CASCADE,
    activity_id INTEGER REFERENCES construction_schema.activities(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (color_id, activity_id)
);

-- Relate 'Activities' entity with 'Tags' entity (O:M)
CREATE TABLE construction_schema.tags2activity (
    tag_id INTEGER REFERENCES shared_schema.tags(id) ON DELETE CASCADE,
    activity_id INTEGER REFERENCES construction_schema.activities(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (tag_id, activity_id)
);


-- Relate 'Activities' entity with 'Activities' entity (M:M)
CREATE TABLE construction_schema.activities2activities (
    id SERIAL PRIMARY KEY,
    related_activity_id INTEGER REFERENCES construction_schema.activities(id) ON DELETE CASCADE,
    activity_id INTEGER REFERENCES construction_schema.activities(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT no_self_reference CHECK (activity_id <> related_activity_id)
);

-- Relate 'Phases' entity with 'Activity' entity (O:M)
CREATE TABLE construction_schema.activities2phase (
    phase_id INTEGER REFERENCES construction_schema.phases(id) ON DELETE CASCADE,
    activity_id INTEGER REFERENCES construction_schema.activities(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (phase_id, activity_id)
);

-- Relate 'Areas' entity with 'Activity' entity (O:M)
CREATE TABLE construction_schema.activities2area (
    area_id INTEGER REFERENCES construction_schema.areas(id) ON DELETE CASCADE,
    activity_id INTEGER REFERENCES construction_schema.activities(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (area_id, activity_id)
);

-- Relate 'Zones' entity with 'Activity' entity (O:M)
CREATE TABLE construction_schema.activities2zone (
    zone_id INTEGER REFERENCES construction_schema.zones(id) ON DELETE CASCADE,
    activity_id INTEGER REFERENCES construction_schema.activities(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (zone_id, activity_id)
);

-- Relate 'Trades' entity with 'Activity' entity (O:M)
CREATE TABLE construction_schema.activities2trade (
    trade_id INTEGER REFERENCES construction_schema.trades(id) ON DELETE CASCADE,
    activity_id INTEGER REFERENCES construction_schema.activities(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (trade_id, activity_id)
);
