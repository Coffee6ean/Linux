-- Call other scripts to generate data tables (Type ORM)
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/shared_schema/versions/db.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/shared_schema/labels/db.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/shared_schema/colors/db.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/shared_schema/locations/db.sql;

-- Call other scripts to generate data pool for 'auth_schema'
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/shared_schema/versions/seed.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/shared_schema/labels/seed.sql;
