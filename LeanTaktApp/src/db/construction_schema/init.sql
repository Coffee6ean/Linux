-- Call other scripts to generate data tables (Type ORM)
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/construction_schema/projects/db.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/construction_schema/phases/db.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/construction_schema/areas/db.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/construction_schema/zones/db.sql
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/construction_schema/trades/db.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/construction_schema/activities/db.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/construction_schema/materials/db.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/construction_schema/issues/db.sql;

-- Call other scripts to generate relationships
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/construction_schema/projects/relations.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/construction_schema/phases/relations.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/construction_schema/areas/relations.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/construction_schema/zones/relations.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/construction_schema/trades/relations.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/construction_schema/activities/relations.sql;
\i /home/coffee_6ean/Linux/LeanTaktApp/src/db/construction_schema/materials/relations.sql;
