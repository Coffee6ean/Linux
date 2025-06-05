-- shared_schema
-- Relate 'Trades' entity with 'Colors' entity (O:M)
CREATE TABLE construction_schema.colors2trade (
    color_id INTEGER REFERENCES shared_schema.colors(id) ON DELETE CASCADE,
    trade_id INTEGER REFERENCES construction_schema.trades(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (color_id, trade_id)
);

-- Relate 'Trades' entity with 'Tags' entity (O:M)
CREATE TABLE construction_schema.tags2trade (
    tag_id INTEGER REFERENCES shared_schema.tags(id) ON DELETE CASCADE,
    trade_id INTEGER REFERENCES construction_schema.trades(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (tag_id, trade_id)
);

-- construction_schema
-- Relate 'Trades' entity with 'Trades' entity (M:M)
CREATE TABLE construction_schema.trades2trades (
    id SERIAL PRIMARY KEY,
    related_trade_id INTEGER REFERENCES construction_schema.trades(id) ON DELETE CASCADE,
    trade_id INTEGER REFERENCES construction_schema.trades(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT no_self_reference CHECK (trade_id <> related_trade_id)
);

-- Relate 'Phases' entity with 'Trades' entity (O:M)
CREATE TABLE construction_schema.trades2phase (
    phase_id INTEGER REFERENCES construction_schema.phases(id) ON DELETE CASCADE,
    trade_id INTEGER REFERENCES construction_schema.trades(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (phase_id, trade_id)
);

-- Relate 'Areas' entity with 'Trades' entity (O:M)
CREATE TABLE construction_schema.trades2area (
    area_id INTEGER REFERENCES construction_schema.areas(id) ON DELETE CASCADE,
    trade_id INTEGER REFERENCES construction_schema.trades(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,   
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (area_id, trade_id)
);

-- Relate 'Zones' entity with 'Trades' entity (O:M)
CREATE TABLE construction_schema.trades2zone (
    zone_id INTEGER REFERENCES construction_schema.zones(id) ON DELETE CASCADE,
    trade_id INTEGER REFERENCES construction_schema.trades(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL, 
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (zone_id, trade_id)
);
