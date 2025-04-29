-- shared_schema

INSERT INTO shared_schema.labels (created_by_entity_id, created_by_entity_type, name, entity_type, type, notes)
VALUES
(1, 'system', 'STABLE', 'versions', 'STATUS', 'Stable/production-ready release'),
(1, 'system', 'BETA', 'versions', 'STATUS', 'Beta/pre-release version'),
(1, 'system', 'DEPRECATED', 'versions', 'STATUS', 'Version is no longer supported');

INSERT INTO shared_schema.labels (created_by_entity_id, created_by_entity_type, name, entity_type, type, notes)
VALUES
(1, 'system', 'PRIMARY', 'colors', 'TYPE', 'Dominant brand color used for key UI elements'),
(1, 'system', 'SECONDARY', 'colors', 'TYPE', 'Supporting brand color used for accents'),
(1, 'system', 'ACCENT', 'colors', 'TYPE', 'Highlight color for calls-to-action and important indicators'),
(1, 'system', 'NEUTRAL', 'colors', 'TYPE', 'Background and text colors for readability'),
(1, 'system', 'STATUS', 'colors', 'TYPE', 'Colors representing system states (success, warning, error)'),
(1, 'system', 'TEXT', 'colors', 'TYPE', 'Color palette for typography and readability'),
(1, 'system', 'BACKGROUND', 'colors', 'TYPE', 'Surface and layout colors'),
(1, 'system', 'DATA', 'colors', 'TYPE', 'Colors used in charts and data visualization'),
(1, 'system', 'DARK_MODE', 'colors', 'RELATIONSHIP', 'Dark theme variant of this color'),
(1, 'system', 'LIGHT_MODE', 'colors', 'RELATIONSHIP', 'Light theme variant of this color'),
(1, 'system', 'COMPLEMENTARY', 'colors', 'RELATIONSHIP', 'Color that visually complements this one'),
(1, 'system', 'CONTRAST', 'colors', 'RELATIONSHIP', 'High-contrast pairing for accessibility');

-- auth_schema

INSERT INTO shared_schema.labels (created_by_entity_id, created_by_entity_type, name, entity_type, type, notes)
VALUES
(1, 'system', 'ACTIVE', 'roles', 'STATUS', 'The role is actively being used'),
(1, 'system', 'INACTIVE', 'roles', 'STATUS', 'The role has been deprecated'),
(1, 'system', 'system', 'roles', 'TYPE', 'System-defined role (cannot be modified by users)'),
(1, 'system', 'CUSTOM', 'roles', 'TYPE', 'User-defined custom role');

INSERT INTO shared_schema.labels (created_by_entity_id, created_by_entity_type, name, entity_type, type, notes)
VALUES
(1, 'system', 'READ', 'permissions', 'CATEGORY', 'Read-only access'),
(1, 'system', 'WRITE', 'permissions', 'CATEGORY', 'Create/edit access'),
(1, 'system', 'DELETE', 'permissions', 'CATEGORY', 'Delete access'),
(1, 'system', 'ADMIN', 'permissions', 'CATEGORY', 'Administrative privileges'),
(1, 'system', 'ACTIVE', 'permissions', 'STATUS', 'The permission is actively grantable'),
(1, 'system', 'DEPRECATED', 'permissions', 'STATUS', 'The permission is no longer grantable (historical use only)');

INSERT INTO shared_schema.labels (created_by_entity_id, created_by_entity_type, name, entity_type, type, notes)
VALUES
(1, 'system', 'ACTIVE', 'users', 'STATUS', 'The user is actively being used'),
(1, 'system', 'INACTIVE', 'users', 'STATUS', 'The user has been deprecated');

INSERT INTO shared_schema.labels (created_by_entity_id, created_by_entity_type, name, entity_type, type, notes)
VALUES
(1, 'system', 'DEVELOPMENT', 'teams', 'CATEGORY', 'Team focused on software development'),
(1, 'system', 'SALES', 'teams', 'CATEGORY', 'Team focused on sales and customer acquisition'),
(1, 'system', 'SUPPORT', 'teams', 'CATEGORY', 'Team handling customer support'),
(1, 'system', 'ACTIVE', 'teams', 'STATUS', 'The team is actively being used'),
(1, 'system', 'INACTIVE', 'teams', 'STATUS', 'The team has been deprecated'),
(1, 'system', 'ARCHIVED', 'teams', 'STATUS', 'The team is no longer active but preserved for historical data');

INSERT INTO shared_schema.labels (created_by_entity_id, created_by_entity_type, name, entity_type, type, notes)
VALUES
(1, 'system', 'ACTIVE', 'tenants', 'STATUS', 'The tenant is actively being used'),
(1, 'system', 'INACTIVE', 'tenants', 'STATUS', 'The tenant has been deprecated'),
(1, 'system', 'SUSPENDED', 'tenants', 'STATUS', 'Tenant access is temporarily suspended (e.g., non-payment)'),
(1, 'system', 'TRIAL', 'tenants', 'STATUS', 'Tenant is in a trial period'),
(1, 'system', 'FREE', 'tenants', 'TIER', 'Free-tier tenant with basic features'),
(1, 'system', 'STANDARD', 'tenants', 'TIER', 'Standard paid tier'),
(1, 'system', 'ENTERPRISE', 'tenants', 'TIER', 'Custom enterprise-tier tenant');

-- construction_schema

INSERT INTO shared_schema.labels (created_by_entity_id, created_by_entity_type, name, entity_type, type, notes) 
VALUES
(1, 'system', 'UNSPECIFIED', 'projects', 'DIVISION', 'Used to determine project type'),
(1, 'system', 'DATA_CENTER', 'projects', 'DIVISION', 'Used to determine project type'),
(1, 'system', 'MULTI-FAMILAR', 'projects', 'DIVISION', 'Used to determine project type'),
(1, 'system', 'VERTICALS', 'projects', 'DIVISION', 'Used to determine project type'),
(1, 'system', 'CIVIL', 'projects', 'DIVISION', 'Used to determine project type'),
(1, 'system', 'COMERCIAL', 'projects', 'DIVISION', 'Used to determine project type'),
(1, 'system', 'TOWN_HOMES', 'projects', 'DIVISION', 'Used to determine project type'),
(1, 'system', 'LOW', 'projects', 'PRIORITY',  'Used to prioritize'),
(1, 'system', 'MEDIUM', 'projects', 'PRIORITY', 'Used to prioritize'),
(1, 'system', 'HIGH', 'projects', 'PRIORITY', 'Used to prioritize'),
(1, 'system', 'PLANNING', 'projects', 'STATUS', 'The project is in the planning stage'),
(1, 'system', 'PENDING', 'projects', 'STATUS', 'The project is awaiting approval/resources/etc'),
(1, 'system', 'ACTIVE', 'projects', 'STATUS', 'The project is actively being worked on'),
(1, 'system', 'ON_HOLD', 'projects', 'STATUS', 'The project is temporarily paused'),
(1, 'system', 'COMPLETED', 'projects', 'STATUS', 'The project has been successfully completed'),
(1, 'system', 'CANCELLED', 'projects', 'STATUS', 'The project has been cancelled'),
(1, 'system', 'ARCHIVED', 'projects', 'STATUS', 'The project has been archived for historical reference'),
(1, 'system', 'NEW', 'projects', 'TYPE', 'Original approved project schedule baseline for ground-up construction'),
(1, 'system', 'RECOVERY', 'projects', 'TYPE', 'Project recovery plan after delays/disasters'),
(1, 'system', 'REFERENCE', 'projects', 'VERSIONING', 'Used to determine if project should be used as reference'),
(1, 'system', 'COMPARISON', 'projects', 'VERSIONING', 'Used to determine if project should be used as reference');

INSERT INTO shared_schema.labels (created_by_entity_id, created_by_entity_type, name, entity_type, type, notes)
VALUES 
(1, 'system', 'LOW', 'phases', 'PRIORITY',  'Used to prioritize'),
(1, 'system', 'MEDIUM', 'phases', 'PRIORITY', 'Used to prioritize'),
(1, 'system', 'HIGH', 'phases', 'PRIORITY', 'Used to prioritize'),
(1, 'system', 'PLANNING', 'phases', 'STATUS', 'The phase is in the planning stage'),
(1, 'system', 'PENDING', 'phases', 'STATUS', 'The phase is awaiting approval/resources/etc'),
(1, 'system', 'ACTIVE', 'phases', 'STATUS', 'The phase is actively being worked on'),
(1, 'system', 'ON_HOLD', 'phases', 'STATUS', 'The phase is temporarily paused'),
(1, 'system', 'COMPLETED', 'phases', 'STATUS', 'The phase has been successfully completed'),
(1, 'system', 'CANCELLED', 'phases', 'STATUS', 'The phase has been cancelled'),
(1, 'system', 'ARCHIVED', 'phases', 'STATUS', 'The phase has been archived for historical reference');

INSERT INTO shared_schema.labels (created_by_entity_id, created_by_entity_type, name, entity_type, type, notes)
VALUES
(1, 'system', 'LOW', 'areas', 'PRIORITY', 'Used to prioritize areas based on urgency or importance'),
(1, 'system', 'MEDIUM', 'areas', 'PRIORITY', 'Used to prioritize areas based on urgency or importance'),
(1, 'system', 'HIGH', 'areas', 'PRIORITY', 'Used to prioritize areas based on urgency or importance'),
(1, 'system', 'PLANNING', 'areas', 'STATUS', 'The area is in the planning stage'),
(1, 'system', 'PENDING', 'areas', 'STATUS', 'The area is awaiting approval, resources, or other dependencies'),
(1, 'system', 'ACTIVE', 'areas', 'STATUS', 'The area is actively being worked on'),
(1, 'system', 'ON_HOLD', 'areas', 'STATUS', 'The area is temporarily paused'),
(1, 'system', 'COMPLETED', 'areas', 'STATUS', 'The area has been successfully completed'),
(1, 'system', 'CANCELLED', 'areas', 'STATUS', 'The area has been cancelled'),
(1, 'system', 'ARCHIVED', 'areas', 'STATUS', 'The area has been archived for historical reference');

INSERT INTO shared_schema.labels (created_by_entity_id, created_by_entity_type, name, entity_type, type, notes)
VALUES
(1, 'system', 'LOW', 'zones', 'PRIORITY', 'Used to prioritize zones based on urgency or importance'),
(1, 'system', 'MEDIUM', 'zones', 'PRIORITY', 'Used to prioritize zones based on urgency or importance'),
(1, 'system', 'HIGH', 'zones', 'PRIORITY', 'Used to prioritize zones based on urgency or importance'),
(1, 'system', 'PLANNING', 'zones', 'STATUS', 'The zone is in the planning stage'),
(1, 'system', 'PENDING', 'zones', 'STATUS', 'The zone is awaiting approval, resources, or other dependencies'),
(1, 'system', 'ACTIVE', 'zones', 'STATUS', 'The zone is actively being worked on'),
(1, 'system', 'ON_HOLD', 'zones', 'STATUS', 'The zone is temporarily paused'),
(1, 'system', 'COMPLETED', 'zones', 'STATUS', 'The zone has been successfully completed'),
(1, 'system', 'CANCELLED', 'zones', 'STATUS', 'The zone has been cancelled'),
(1, 'system', 'ARCHIVED', 'zones', 'STATUS', 'The zone has been archived for historical reference');

INSERT INTO shared_schema.labels (created_by_entity_id, created_by_entity_type, name, entity_type, type, notes)
VALUES
(1, 'system', 'LOW', 'trades', 'PRIORITY',  'Used to prioritize'),
(1, 'system', 'MEDIUM', 'trades', 'PRIORITY', 'Used to prioritize'),
(1, 'system', 'HIGH', 'trades', 'PRIORITY', 'Used to prioritize'),
(1, 'system', 'PLANNING', 'trades', 'STATUS', 'The phase is in the planning stage'),
(1, 'system', 'PENDING', 'trades', 'STATUS', 'The phase is awaiting approval/resources/etc'),
(1, 'system', 'ACTIVE', 'trades', 'STATUS', 'The phase is actively being worked on'),
(1, 'system', 'ON_HOLD', 'trades', 'STATUS', 'The phase is temporarily paused'),
(1, 'system', 'COMPLETED', 'trades', 'STATUS', 'The phase has been successfully completed'),
(1, 'system', 'CANCELLED', 'trades', 'STATUS', 'The phase has been cancelled'),
(1, 'system', 'ARCHIVED', 'trades', 'STATUS', 'The phase has been archived for historical reference');


INSERT INTO shared_schema.labels (created_by_entity_id, created_by_entity_type, name, entity_type, type, notes)
VALUES
(1, 'system', 'NEW', 'activities', 'CATEGORY', 'Activity is newly created and requires review'),
(1, 'system', 'UPDATED', 'activities', 'CATEGORY', 'Activity has been updated and requires review'),
(1, 'system', 'MATCHING', 'activities', 'CATEGORY', 'Activity matches an existing record or template'),
(1, 'system', 'REMOVED', 'activities', 'CATEGORY', 'Activity has been removed or deleted'),
(1, 'system', 'DUPLICATE', 'activities', 'CATEGORY', 'Activity is a duplicate of another record'),
(1, 'system', 'INVALID', 'activities', 'CATEGORY', 'Activity is invalid or contains errors'),
(1, 'system', 'LOGIC', 'activities', 'CATEGORY', 'Activity involves logic or rules that need validation'),
(1, 'system', 'LOW', 'activities', 'PRIORITY', 'Used to prioritize activities based on urgency or importance'),
(1, 'system', 'MEDIUM', 'activities', 'PRIORITY', 'Used to prioritize activities based on urgency or importance'),
(1, 'system', 'HIGH', 'activities', 'PRIORITY', 'Used to prioritize activities based on urgency or importance'),
(1, 'system', 'PREDECESSOR', 'activities', 'RELATIONSHIP', 'Activity that must be completed before this one can begin'),
(1, 'system', 'SUCCESSOR', 'activities', 'RELATIONSHIP', 'Activity that depends on this one being completed'),
(1, 'system', 'BLOCKER', 'activities', 'RELATIONSHIP', 'Activity that prevents progress on this one'),
(1, 'system', 'PLANNING', 'activities', 'STATUS', 'The activity is in the planning stage'),
(1, 'system', 'PENDING', 'activities', 'STATUS', 'The activity is awaiting approval, resources, or other dependencies'),
(1, 'system', 'ACTIVE', 'activities', 'STATUS', 'The activity is actively being worked on'),
(1, 'system', 'ON_HOLD', 'activities', 'STATUS', 'The activity is temporarily paused'),
(1, 'system', 'COMPLETED', 'activities', 'STATUS', 'The activity has been successfully completed'),
(1, 'system', 'CANCELLED', 'activities', 'STATUS', 'The activity has been cancelled'),
(1, 'system', 'ARCHIVED', 'activities', 'STATUS', 'The activity has been archived for historical reference'),
(1, 'system', 'ACTIVITY', 'activities', 'TYPE', 'Standard work activity or task'),
(1, 'system', 'MILESTONE', 'activities', 'TYPE', 'Key project milestone or deliverable'),
(1, 'system', 'PROCUREMENT', 'activities', 'TYPE', 'Material or equipment procurement activity'),
(1, 'system', 'BUFFER', 'activities', 'TYPE', 'Schedule buffer or contingency time'),
(1, 'system', 'HOLIDAY', 'activities', 'TYPE', 'Non-working holiday or break period');

INSERT INTO shared_schema.labels (created_by_entity_id, created_by_entity_type, name, entity_type, type, notes)
VALUES
(1, 'system', 'LOW', 'issues', 'PRIORITY', 'Used to prioritize issues based on urgency or importance'),
(1, 'system', 'MEDIUM', 'issues', 'PRIORITY', 'Used to prioritize issues based on urgency or importance'),
(1, 'system', 'HIGH', 'issues', 'PRIORITY', 'Used to prioritize issues based on urgency or importance'),
(1, 'system', 'OPEN', 'issues', 'STATUS', 'The issue is open and awaiting resolution'),
(1, 'system', 'IN_PROGRESS', 'issues', 'STATUS', 'The issue is actively being worked on'),
(1, 'system', 'CLOSED', 'issues', 'STATUS', 'The issue has been resolved and closed'),
(1, 'system', 'BUG', 'issues', 'TYPE', 'The issue is a bug or defect that needs to be fixed'),
(1, 'system', 'IMPROVEMENT', 'issues', 'TYPE', 'The issue is a request for improvement or enhancement'),
(1, 'system', 'FEATURE_REQUEST', 'issues', 'TYPE', 'The issue is a request for a new feature'),
(1, 'system', 'TASK', 'issues', 'TYPE', 'The issue is a general task or to-do item'),
(1, 'system', 'BLOCKER', 'issues', 'TYPE', 'The issue is blocking progress and requires immediate attention');


INSERT INTO shared_schema.labels (created_by_entity_id, created_by_entity_type, name, entity_type, type, notes)
VALUES
(1, 'system', 'DRAFT', 'materials', 'STATUS', 'Material specification in preliminary draft form'),
(1, 'system', 'ESTIMATED', 'materials', 'STATUS', 'Quantity projected in takeoff but not yet ordered'),
(1, 'system', 'APPROVED', 'materials', 'STATUS', 'Material specification formally approved for procurement'),
(1, 'system', 'ORDERED', 'materials', 'STATUS', 'Purchase order submitted to supplier'),
(1, 'system', 'IN_TRANSIT', 'materials', 'STATUS', 'Shipped from supplier but not yet delivered'),
(1, 'system', 'DELIVERED', 'materials', 'STATUS', 'Received onsite and awaiting inspection'),
(1, 'system', 'INSPECTED', 'materials', 'STATUS', 'Quality checked and ready for use'),
(1, 'system', 'INSTALLED', 'materials', 'STATUS', 'Permanently placed in construction'),
(1, 'system', 'DEFECTIVE', 'materials', 'STATUS', 'Failed quality inspection - requires replacement'),
(1, 'system', 'RETURNED', 'materials', 'STATUS', 'Sent back to supplier for credit/replacement'),
(1, 'system', 'LOW', 'materials', 'PRIORITY', 'Standard material with flexible delivery window'),
(1, 'system', 'MEDIUM', 'materials', 'PRIORITY', 'Material needed for upcoming work package'),
(1, 'system', 'HIGH', 'materials', 'PRIORITY', 'Critical path material - delays would impact schedule');
