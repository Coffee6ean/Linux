-- Connect to the Database
\c cpm_processor_db;

-- Call other scripts to generate data tables (Type ORM)
\i /home/coffee_6ean/Linux/CpmProcessor/db/shared_schema/versions/db.sql;
\i /home/coffee_6ean/Linux/CpmProcessor/db/shared_schema/labels/db.sql;
\i /home/coffee_6ean/Linux/CpmProcessor/db/shared_schema/colors/db.sql;
\i /home/coffee_6ean/Linux/CpmProcessor/db/shared_schema/locations/db.sql;
\i /home/coffee_6ean/Linux/CpmProcessor/db/shared_schema/tags/db.sql;

-- Call other scripts to generate data pool for 'auth_schema'
\i /home/coffee_6ean/Linux/CpmProcessor/db/shared_schema/versions/seed.sql;
\i /home/coffee_6ean/Linux/CpmProcessor/db/shared_schema/labels/seed.sql;
