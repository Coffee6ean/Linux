-- shared_schema

INSERT INTO shared_schema.labels (name, entity_type, type, notes)
VALUES
('STABLE', 'versions', 'STATUS', 'Stable/production-ready release'),
('BETA', 'versions', 'STATUS', 'Beta/pre-release version'),
('DEPRECATED', 'versions', 'STATUS', 'Version is no longer supported');

INSERT INTO shared_schema.labels (name, entity_type, type, notes)
VALUES
('PRIMARY', 'colors', 'TYPE', 'Dominant brand color used for key UI elements'),
('SECONDARY', 'colors', 'TYPE', 'Supporting brand color used for accents'),
('ACCENT', 'colors', 'TYPE', 'Highlight color for calls-to-action and important indicators'),
('NEUTRAL', 'colors', 'TYPE', 'Background and text colors for readability'),
('STATUS', 'colors', 'TYPE', 'Colors representing system states (success, warning, error)'),
('TEXT', 'colors', 'TYPE', 'Color palette for typography and readability'),
('BACKGROUND', 'colors', 'TYPE', 'Surface and layout colors'),
('DATA', 'colors', 'TYPE', 'Colors used in charts and data visualization');
('DARK_MODE', 'colors', 'RELATIONSHIP', 'Dark theme variant of this color'),
('LIGHT_MODE', 'colors', 'RELATIONSHIP', 'Light theme variant of this color'),
('COMPLEMENTARY', 'colors', 'RELATIONSHIP', 'Color that visually complements this one'),
('CONTRAST', 'colors', 'RELATIONSHIP', 'High-contrast pairing for accessibility');

-- auth_schema

INSERT INTO shared_schema.labels (name, entity_type, type, notes)
VALUES
('ACTIVE', 'roles', 'STATUS', 'The role is actively being used'),
('INACTIVE', 'roles', 'STATUS', 'The role has been deprecated'),
('SYSTEM', 'roles', 'TYPE', 'System-defined role (cannot be modified by users)'),
('CUSTOM', 'roles', 'TYPE', 'User-defined custom role');

INSERT INTO shared_schema.labels (name, entity_type, type, notes)
VALUES
('READ', 'permissions', 'CATEGORY', 'Read-only access'),
('WRITE', 'permissions', 'CATEGORY', 'Create/edit access'),
('DELETE', 'permissions', 'CATEGORY', 'Delete access'),
('ADMIN', 'permissions', 'CATEGORY', 'Administrative privileges'),
('ACTIVE', 'permissions', 'STATUS', 'The permission is actively grantable'),
('DEPRECATED', 'permissions', 'STATUS', 'The permission is no longer grantable (historical use only)');

INSERT INTO shared_schema.labels (name, entity_type, type, notes)
VALUES
('ACTIVE', 'users', 'STATUS', 'The user is actively being used'),
('INACTIVE', 'users', 'STATUS', 'The user has been deprecated');

INSERT INTO shared_schema.labels (name, entity_type, type, notes)
VALUES
('DEVELOPMENT', 'teams', 'CATEGORY', 'Team focused on software development'),
('SALES', 'teams', 'CATEGORY', 'Team focused on sales and customer acquisition'),
('SUPPORT', 'teams', 'CATEGORY', 'Team handling customer support'),
('ACTIVE', 'teams', 'STATUS', 'The team is actively being used'),
('INACTIVE', 'teams', 'STATUS', 'The team has been deprecated'),
('ARCHIVED', 'teams', 'STATUS', 'The team is no longer active but preserved for historical data');

INSERT INTO shared_schema.labels (name, entity_type, type, notes)
VALUES
('ACTIVE', 'tenants', 'STATUS', 'The tenant is actively being used'),
('INACTIVE', 'tenants', 'STATUS', 'The tenant has been deprecated'),
('SUSPENDED', 'tenants', 'STATUS', 'Tenant access is temporarily suspended (e.g., non-payment)'),
('TRIAL', 'tenants', 'STATUS', 'Tenant is in a trial period'),
('FREE', 'tenants', 'TIER', 'Free-tier tenant with basic features'),
('STANDARD', 'tenants', 'TIER', 'Standard paid tier'),
('ENTERPRISE', 'tenants', 'TIER', 'Custom enterprise-tier tenant');

-- construction_schema

INSERT INTO shared_schema.labels (name, entity_type, type, notes) 
VALUES
('UNSPECIFIED', 'projects', 'DIVISION', 'Used to determine project type'),
('DATA_CENTER', 'projects', 'DIVISION', 'Used to determine project type'),
('MULTI-FAMILAR', 'projects', 'DIVISION', 'Used to determine project type'),
('VERTICALS', 'projects', 'DIVISION', 'Used to determine project type'),
('CIVIL', 'projects', 'DIVISION', 'Used to determine project type'),
('COMERCIAL', 'projects', 'DIVISION', 'Used to determine project type'),
('TOWN_HOMES', 'projects', 'DIVISION', 'Used to determine project type'),
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
('NEW', 'projects', 'TYPE', 'Original approved project schedule baseline for ground-up construction'),
('RECOVERY', 'projects', 'TYPE', 'Project recovery plan after delays/disasters'),
('REFERENCE', 'projects', 'VERSIONING', 'Used to determine if project should be used as reference'),
('COMPARISON', 'projects', 'VERSIONING', 'Used to determine if project should be used as reference');

INSERT INTO shared_schema.labels (name, entity_type, type, notes)
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

INSERT INTO shared_schema.labels (name, entity_type, type, notes)
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


INSERT INTO shared_schema.labels (name, entity_type, type, notes)
VALUES
('NEW', 'activities', 'CATEGORY', 'Activity is newly created and requires review'),
('UPDATED', 'activities', 'CATEGORY', 'Activity has been updated and requires review'),
('MATCHING', 'activities', 'CATEGORY', 'Activity matches an existing record or template')
('REMOVED', 'activities', 'CATEGORY', 'Activity has been removed or deleted'),
('DUPLICATE', 'activities', 'CATEGORY', 'Activity is a duplicate of another record'),
('INVALID', 'activities', 'CATEGORY', 'Activity is invalid or contains errors'),
('LOGIC', 'activities', 'CATEGORY', 'Activity involves logic or rules that need validation'),
('LOW', 'activities', 'PRIORITY', 'Used to prioritize activities based on urgency or importance'),
('MEDIUM', 'activities', 'PRIORITY', 'Used to prioritize activities based on urgency or importance'),
('HIGH', 'activities', 'PRIORITY', 'Used to prioritize activities based on urgency or importance'),
('PREDECESSOR', 'activities', 'RELATIONSHIP', 'Activity that must be completed before this one can begin'),
('SUCCESSOR', 'activities', 'RELATIONSHIP', 'Activity that depends on this one being completed'),
('BLOCKER', 'activities', 'RELATIONSHIP', 'Activity that prevents progress on this one'),
('PLANNING', 'activities', 'STATUS', 'The activity is in the planning stage'),
('PENDING', 'activities', 'STATUS', 'The activity is awaiting approval, resources, or other dependencies'),
('ACTIVE', 'activities', 'STATUS', 'The activity is actively being worked on'),
('ON_HOLD', 'activities', 'STATUS', 'The activity is temporarily paused'),
('COMPLETED', 'activities', 'STATUS', 'The activity has been successfully completed'),
('CANCELLED', 'activities', 'STATUS', 'The activity has been cancelled'),
('ARCHIVED', 'activities', 'STATUS', 'The activity has been archived for historical reference'),
('ACTIVITY', 'activities', 'TYPE', 'Standard work activity or task'),
('MILESTONE', 'activities', 'TYPE', 'Key project milestone or deliverable'),
('PROCUREMENT', 'activities', 'TYPE', 'Material or equipment procurement activity'),
('BUFFER', 'activities', 'TYPE', 'Schedule buffer or contingency time'),
('HOLIDAY', 'activities', 'TYPE', 'Non-working holiday or break period');

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
