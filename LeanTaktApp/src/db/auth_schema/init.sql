-- Call other scripts to generate data tables (Type ORM)
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/auth_schema/roles/db.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/auth_schema/permissions/db.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/auth_schema/users/db.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/auth_schema/teams/db.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/auth_schema/tenants/db.sql;

-- Build relationships
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/auth_schema/permissions/relations.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/auth_schema/users/relations.sql;

-- Call other scripts to generate data pool for 'auth_schema'
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/auth_schema/roles/seed.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/auth_schema/permissions/seed.sql;
