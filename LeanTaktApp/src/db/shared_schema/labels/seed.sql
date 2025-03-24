-- For 'Roles'
INSERT INTO shared_schema.labels (name, entity_type, type, notes)
VALUES
('ACTIVE', 'roles', 'STATUS', 'The role is actively being used'),
('INACTIVE', 'roles', 'STATUS', 'The role has been deprecated');

-- For 'Projects'
INSERT INTO shared_schema.labels (name, entity_type, type, notes) 
VALUES
('LOW', 'projects', 'PRIORITY',  'Used to prioritize'),
('MEDIUM', 'projects', 'PRIORITY', 'Used to prioritize'),
('HIGH', 'projects', 'PRIORITY', 'Used to prioritize'),
('PLANNING', 'projects', 'STATUS', 'The project is in the planning stage'),
('PENDING', 'projects', 'STATUS', 'The project is awaiting approval/resources/etc'),
('ACTIVE', 'projects', 'STATUS', 'The project is actively being worked on'),
('ON_HOLD', 'projects', 'STATUS', 'The project is temporarily paused'),
('COMPLETED', 'projects', 'STATUS', 'The project has been successfully completed'),
('CANCELLED', 'projects', 'STATUS', 'The project has been cancelled'),
('ARCHIVED', 'projects', 'STATUS', 'The project has been archived for historical reference'),
('UNSPECIFIED', 'projects', 'TYPE', 'Used to determine project type'),
('DATA_CENTER', 'projects', 'TYPE', 'Used to determine project type'),
('MULTI-FAMILAR', 'projects', 'TYPE', 'Used to determine project type'),
('VERTICALS', 'projects', 'TYPE', 'Used to determine project type'),
('CIVIL', 'projects', 'TYPE', 'Used to determine project type'),
('COMERCIAL', 'projects', 'TYPE', 'Used to determine project type'),
('TOWN_HOMES', 'projects', 'TYPE', 'Used to determine project type'),
('REFERENCE', 'projects', 'VERSIONING', 'Used to determine if project should be used as reference'),
('COMPARISON', 'projects', 'VERSIONING', 'Used to determine if project should be used as reference');

-- For 'Phases'
INSERT INTO shared_schema.labels(name, entity_type, type, notes)
VALUES 
('LOW', 'phases', 'PRIORITY',  'Used to prioritize'),
('MEDIUM', 'phases', 'PRIORITY', 'Used to prioritize'),
('HIGH', 'phases', 'PRIORITY', 'Used to prioritize'),
('PLANNING', 'phases', 'STATUS', 'The phase is in the planning stage'),
('PENDING', 'phases', 'STATUS', 'The phase is awaiting approval/resources/etc'),
('ACTIVE', 'phases', 'STATUS', 'The phase is actively being worked on'),
('ON_HOLD', 'phases', 'STATUS', 'The phase is temporarily paused'),
('COMPLETED', 'phases', 'STATUS', 'The phase has been successfully completed'),
('CANCELLED', 'phases', 'STATUS', 'The phase has been cancelled'),
('ARCHIVED', 'phases', 'STATUS', 'The phase has been archived for historical reference');

-- For 'Areas'
INSERT INTO shared_schema.labels (name, entity_type, type, notes)
VALUES
('LOW', 'areas', 'PRIORITY', 'Used to prioritize areas based on urgency or importance'),
('MEDIUM', 'areas', 'PRIORITY', 'Used to prioritize areas based on urgency or importance'),
('HIGH', 'areas', 'PRIORITY', 'Used to prioritize areas based on urgency or importance'),
('PLANNING', 'areas', 'STATUS', 'The area is in the planning stage'),
('PENDING', 'areas', 'STATUS', 'The area is awaiting approval, resources, or other dependencies'),
('ACTIVE', 'areas', 'STATUS', 'The area is actively being worked on'),
('ON_HOLD', 'areas', 'STATUS', 'The area is temporarily paused'),
('COMPLETED', 'areas', 'STATUS', 'The area has been successfully completed'),
('CANCELLED', 'areas', 'STATUS', 'The area has been cancelled'),
('ARCHIVED', 'areas', 'STATUS', 'The area has been archived for historical reference');

-- For 'Zones'
INSERT INTO shared_schema.labels (name, entity_type, type, notes)
VALUES
('LOW', 'zones', 'PRIORITY', 'Used to prioritize zones based on urgency or importance'),
('MEDIUM', 'zones', 'PRIORITY', 'Used to prioritize zones based on urgency or importance'),
('HIGH', 'zones', 'PRIORITY', 'Used to prioritize zones based on urgency or importance'),
('PLANNING', 'zones', 'STATUS', 'The zone is in the planning stage'),
('PENDING', 'zones', 'STATUS', 'The zone is awaiting approval, resources, or other dependencies'),
('ACTIVE', 'zones', 'STATUS', 'The zone is actively being worked on'),
('ON_HOLD', 'zones', 'STATUS', 'The zone is temporarily paused'),
('COMPLETED', 'zones', 'STATUS', 'The zone has been successfully completed'),
('CANCELLED', 'zones', 'STATUS', 'The zone has been cancelled'),
('ARCHIVED', 'zones', 'STATUS', 'The zone has been archived for historical reference');

-- For 'Trades'
INSERT INTO shared_schema.labels(name, entity_type, type, notes)
VALUES
('LOW', 'trades', 'PRIORITY',  'Used to prioritize'),
('MEDIUM', 'trades', 'PRIORITY', 'Used to prioritize'),
('HIGH', 'trades', 'PRIORITY', 'Used to prioritize'),
('PLANNING', 'trades', 'STATUS', 'The phase is in the planning stage'),
('PENDING', 'trades', 'STATUS', 'The phase is awaiting approval/resources/etc'),
('ACTIVE', 'trades', 'STATUS', 'The phase is actively being worked on'),
('ON_HOLD', 'trades', 'STATUS', 'The phase is temporarily paused'),
('COMPLETED', 'trades', 'STATUS', 'The phase has been successfully completed'),
('CANCELLED', 'trades', 'STATUS', 'The phase has been cancelled'),
('ARCHIVED', 'trades', 'STATUS', 'The phase has been archived for historical reference');

-- For 'Milestones'
INSERT INTO shared_schema.labels(name, entity_type, type, notes)
VALUES
('LOW', 'milestones', 'PRIORITY',  'Used to prioritize'),
('MEDIUM', 'milestones', 'PRIORITY', 'Used to prioritize'),
('HIGH', 'milestones', 'PRIORITY', 'Used to prioritize'),
('PLANNING', 'milestones', 'STATUS', 'The phase is in the planning stage'),
('PENDING', 'milestones', 'STATUS', 'The phase is awaiting approval/resources/etc'),
('ACTIVE', 'milestones', 'STATUS', 'The phase is actively being worked on'),
('ON_HOLD', 'milestones', 'STATUS', 'The phase is temporarily paused'),
('COMPLETED', 'milestones', 'STATUS', 'The phase has been successfully completed'),
('CANCELLED', 'milestones', 'STATUS', 'The phase has been cancelled'),
('ARCHIVED', 'milestones', 'STATUS', 'The phase has been archived for historical reference');

-- For 'Procurements'
INSERT INTO shared_schema.labels(name, entity_type, type, notes)
VALUES
('LOW', 'procurements', 'PRIORITY',  'Used to prioritize'),
('MEDIUM', 'procurements', 'PRIORITY', 'Used to prioritize'),
('HIGH', 'procurements', 'PRIORITY', 'Used to prioritize'),
('PLANNING', 'procurements', 'STATUS', 'The phase is in the planning stage'),
('PENDING', 'procurements', 'STATUS', 'The phase is awaiting approval/resources/etc'),
('ACTIVE', 'procurements', 'STATUS', 'The phase is actively being worked on'),
('ON_HOLD', 'procurements', 'STATUS', 'The phase is temporarily paused'),
('COMPLETED', 'procurements', 'STATUS', 'The phase has been successfully completed'),
('CANCELLED', 'procurements', 'STATUS', 'The phase has been cancelled'),
('ARCHIVED', 'procurements', 'STATUS', 'The phase has been archived for historical reference');

-- For 'Activities'
INSERT INTO shared_schema.labels (name, entity_type, type, notes)
VALUES
('NEW', 'activities', 'CATEGORY', 'Activity is newly created and requires review'),
('UPDATED', 'activities', 'CATEGORY', 'Activity has been updated and requires review'),
('MATCHING', 'activities', 'CATEGORY', 'Activity matches an existing record or template'),
('REMOVED', 'activities', 'CATEGORY', 'Activity has been removed or deleted'),
('DUPLICATE', 'activities', 'CATEGORY', 'Activity is a duplicate of another record'),
('INVALID', 'activities', 'CATEGORY', 'Activity is invalid or contains errors'),
('LOGIC', 'activities', 'CATEGORY', 'Activity involves logic or rules that need validation'),
('LOW', 'activities', 'PRIORITY', 'Used to prioritize activities based on urgency or importance'),
('MEDIUM', 'activities', 'PRIORITY', 'Used to prioritize activities based on urgency or importance'),
('HIGH', 'activities', 'PRIORITY', 'Used to prioritize activities based on urgency or importance'),
('PLANNING', 'activities', 'STATUS', 'The activity is in the planning stage'),
('PENDING', 'activities', 'STATUS', 'The activity is awaiting approval, resources, or other dependencies'),
('ACTIVE', 'activities', 'STATUS', 'The activity is actively being worked on'),
('ON_HOLD', 'activities', 'STATUS', 'The activity is temporarily paused'),
('COMPLETED', 'activities', 'STATUS', 'The activity has been successfully completed'),
('CANCELLED', 'activities', 'STATUS', 'The activity has been cancelled'),
('ARCHIVED', 'activities', 'STATUS', 'The activity has been archived for historical reference');

-- For 'Issues'
INSERT INTO shared_schema.labels (name, entity_type, type, notes)
VALUES
('LOW', 'issues', 'PRIORITY', 'Used to prioritize issues based on urgency or importance'),
('MEDIUM', 'issues', 'PRIORITY', 'Used to prioritize issues based on urgency or importance'),
('HIGH', 'issues', 'PRIORITY', 'Used to prioritize issues based on urgency or importance'),
('OPEN', 'issues', 'STATUS', 'The issue is open and awaiting resolution'),
('IN_PROGRESS', 'issues', 'STATUS', 'The issue is actively being worked on'),
('CLOSED', 'issues', 'STATUS', 'The issue has been resolved and closed'),
('BUG', 'issues', 'TYPE', 'The issue is a bug or defect that needs to be fixed'),
('IMPROVEMENT', 'issues', 'TYPE', 'The issue is a request for improvement or enhancement'),
('FEATURE_REQUEST', 'issues', 'TYPE', 'The issue is a request for a new feature'),
('TASK', 'issues', 'TYPE', 'The issue is a general task or to-do item'),
('BLOCKER', 'issues', 'TYPE', 'The issue is blocking progress and requires immediate attention');
