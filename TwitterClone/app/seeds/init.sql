-- Drop Database
DROP DATABASE IF EXISTS twitter_clone_db;

-- Create Database
CREATE DATABASE twitter_clone_db;

-- Connect to the Database
\c twitter_clone_db;

-- Call other scripts for table creation with correct paths
\i /home/coffee_6ean/Linux/TwitterClone/app/seeds/Users/users.sql
\i /home/coffee_6ean/Linux/TwitterClone/app/seeds/Projects/projects.sql
\i /home/coffee_6ean/Linux/TwitterClone/app/seeds/Boards/discussion_boards.sql
