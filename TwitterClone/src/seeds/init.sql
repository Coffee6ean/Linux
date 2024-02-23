-- Drop Database
DROP DATABASE IF EXISTS twitter_clone_db;

-- Create Database
CREATE DATABASE twitter_clone_db;

-- Connect to the Database
\c twitter_clone_db;

-- Create Entities Table
\i /home/coffee_6ean/Linux/TwitterClone/app/seeds/entities.sql;

-- Call other scripts for table creation with correct paths
\i /home/coffee_6ean/Linux/TwitterClone/app/seeds/users.sql;
\i /home/coffee_6ean/Linux/TwitterClone/app/seeds/projects.sql;
\i /home/coffee_6ean/Linux/TwitterClone/app/seeds/boards.sql;
