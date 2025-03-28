-- shared_schema
INSERT INTO auth_schema.permissions (name, entity_type, notes)
VALUES
('CREATE', 'versions', 'Permission to create new versions'),
('READ', 'versions', 'Permission to view version details'),
('UPDATE','versions', 'Permission to edit existing version'),
('DELETE','versions', 'Permission to delete existing version');

INSERT INTO auth_schema.permissions (name, entity_type, notes)
VALUES
('CREATE', 'labels', 'Permission to create new labels'),
('READ', 'labels', 'Permission to view label details'),
('UPDATE','labels', 'Permission to edit existing label'),
('DELETE','labels', 'Permission to delete existing label');

INSERT INTO auth_schema.permissions (name, entity_type, notes)
VALUES
('CREATE', 'locations', 'Permission to create new locations'),
('READ', 'locations', 'Permission to view location details'),
('UPDATE','locations', 'Permission to edit existing location'),
('DELETE','locations', 'Permission to delete existing location');

INSERT INTO auth_schema.permissions (name, entity_type, notes)
VALUES
('CREATE', 'colors', 'Permission to create new colors'),
('READ', 'colors', 'Permission to view color details'),
('UPDATE','colors', 'Permission to edit existing color'),
('DELETE','colors', 'Permission to delete existing color');

-- auth_schema
INSERT INTO auth_schema.permissions (name, entity_type, notes)
VALUES
('CREATE', 'roles', 'Permission to create new roles'),
('READ', 'roles', 'Permission to view role details'),
('UPDATE','roles', 'Permission to edit existing role'),
('DELETE','roles', 'Permission to delete existing role');

INSERT INTO auth_schema.permissions (name, entity_type, notes)
VALUES
('CREATE', 'permissions', 'Permission to create new permissions'),
('READ', 'permissions', 'Permission to view permission details'),
('UPDATE','permissions', 'Permission to edit existing permission'),
('DELETE','permissions', 'Permission to delete existing permission');

INSERT INTO auth_schema.permissions (name, entity_type, notes)
VALUES
('CREATE', 'users', 'Permission to create new users'),
('READ', 'users', 'Permission to view user details'),
('UPDATE','users', 'Permission to edit existing user'),
('DELETE','users', 'Permission to delete existing user');

INSERT INTO auth_schema.permissions (name, entity_type, notes)
VALUES
('CREATE', 'teams', 'Permission to create new teams'),
('READ', 'teams', 'Permission to view team details'),
('UPDATE','teams', 'Permission to edit existing team'),
('DELETE','teams', 'Permission to delete existing team');

INSERT INTO auth_schema.permissions (name, entity_type, notes)
VALUES
('CREATE', 'tenants', 'Permission to create new tenants'),
('READ', 'tenants', 'Permission to view tenant details'),
('UPDATE','tenants', 'Permission to edit existing tenant'),
('DELETE','tenants', 'Permission to delete existing tenant');

-- construction_schema
INSERT INTO auth_schema.permissions (name, entity_type, notes)
VALUES
('CREATE', 'projects', 'Permission to create new projects'),
('READ', 'projects', 'Permission to view project details'),
('UPDATE','projects', 'Permission to edit existing project'),
('DELETE','projects', 'Permission to delete existing project');

INSERT INTO auth_schema.permissions (name, entity_type, notes)
VALUES
('CREATE', 'phases', 'Permission to create new phases'),
('READ', 'phases', 'Permission to view phase details'),
('UPDATE','phases', 'Permission to edit existing phase'),
('DELETE','phases', 'Permission to delete existing phase');

INSERT INTO auth_schema.permissions (name, entity_type, notes)
VALUES
('CREATE', 'areas', 'Permission to create new areas'),
('READ', 'areas', 'Permission to view area details'),
('UPDATE','areas', 'Permission to edit existing area'),
('DELETE','areas', 'Permission to delete existing area');

INSERT INTO auth_schema.permissions (name, entity_type, notes)
VALUES
('CREATE', 'zones', 'Permission to create new zones'),
('READ', 'zones', 'Permission to view zone details'),
('UPDATE','zones', 'Permission to edit existing zone'),
('DELETE','zones', 'Permission to delete existing zone');

INSERT INTO auth_schema.permissions (name, entity_type, notes)
VALUES
('CREATE', 'trades', 'Permission to create new trades'),
('READ', 'trades', 'Permission to view trade details'),
('UPDATE','trades', 'Permission to edit existing trade'),
('DELETE','trades', 'Permission to delete existing trade');

INSERT INTO auth_schema.permissions (name, entity_type, notes)
VALUES
('CREATE', 'activities', 'Permission to create new activities'),
('READ', 'activities', 'Permission to view activity details'),
('UPDATE','activities', 'Permission to edit existing activity'),
('DELETE','activities', 'Permission to delete existing activity');

INSERT INTO auth_schema.permissions (name, entity_type, notes)
VALUES
('CREATE', 'issues', 'Permission to create new issues'),
('READ', 'issues', 'Permission to view issue details'),
('UPDATE','issues', 'Permission to edit existing issue'),
('DELETE','issues', 'Permission to delete existing issue');

INSERT INTO auth_schema.permissions (name, entity_type, notes)
VALUES
('CREATE', 'tags', 'Permission to create new tags'),
('READ', 'tags', 'Permission to view tag details'),
('UPDATE','tags', 'Permission to edit existing tag'),
('DELETE','tags', 'Permission to delete existing tag');
