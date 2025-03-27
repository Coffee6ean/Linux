-- Create junction table for 'Tag' relationships
CREATE TABLE shared_schema.tagged (
    tag_id INTEGER NOT NULL REFERENCES shared_schema.tags(id) ON DELETE CASCADE,
    entity_type VARCHAR(255) NOT NULL,  -- Type of entity (e.g., User, Tenant, Project)
    entity_id INTEGER NOT NULL,         -- ID of the tagged entity 
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (tag_id, entity_type, entity_id)  -- Prevent duplicate tagging
);
