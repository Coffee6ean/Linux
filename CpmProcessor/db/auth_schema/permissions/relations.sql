-- Relate 'Permissions' entity with 'Roles' entity
CREATE TABLE auth_schema.permissions2roles (
    id SERIAL PRIMARY KEY,
    role_id INTEGER NOT NULL REFERENCES auth_schema.roles(id) ON DELETE CASCADE,
    permission_id INTEGER NOT NULL REFERENCES auth_schema.permissions(id) ON DELETE CASCADE,
    status_id INTEGER REFERENCES shared_schema.labels(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (role_id, permission_id)
);
