-- System Core Entity with Full Description
INSERT INTO system_schema.system (name, version, notes)
VALUES 
('SYSTEM', '1.0.0',
 'This is the master system record that owns all core permissions, configurations, and seed data. '||
 'It serves as the parent entity for all system-level operations and automated processes.');
