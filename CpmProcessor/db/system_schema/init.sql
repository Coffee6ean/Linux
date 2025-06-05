-- Connect to the Database
\c cpm_processor_db;

-- Call other scripts to generate data tables (Type ORM)
\i /home/coffee_6ean/Linux/CpmProcessor/db/system_schema/system/db.sql;

-- Call other scripts to generate data pool for 'system_schema'
\i /home/coffee_6ean/Linux/CpmProcessor/db/system_schema/system/seed.sql;
