-- Issues Tracking Table
CREATE TABLE construction_schema.issues (
    id SERIAL PRIMARY KEY,
    parent_type VARCHAR(50) NOT NULL,
    parent_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    notes TEXT NOT NULL,
    category_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    priority_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    type_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    reported_by INTEGER NOT NULL REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    assigned_to INTEGER REFERENCES auth_schema.users(id) ON DELETE SET NULL,
    due_date DATE,
    resolved_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT resolution_requires_date CHECK (
        (status_id IS NULL AND resolved_at IS NULL) OR 
        (status_id IS NOT NULL AND resolved_at IS NOT NULL)
    )
);
