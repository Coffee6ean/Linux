-- Drop Database 
DROP DATABASE IF EXISTS adopt_animal_db;

-- Create Database
CREATE DATABASE adopt_animal_db;

-- Connect to the Database
\c adopt_animal_db

-- Create a new table with a serial (auto-increment) id column
CREATE TABLE pet (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    species TEXT NOT NULL,
    photo_url TEXT,
    age INTEGER,
    notes TEXT,
    available BOOLEAN DEFAULT true
);

-- Insert your data
INSERT INTO pet(name, species, photo_url, age, notes) VALUES
('Ragu', 'Dog', 'pug_img.com', 4, 'Very chunky and a beautiful girl'),
('Carlotita', 'Dog', 'pug2_img.com', 2, 'Her royal highness pug version'),
('Albondiga', 'Dog', 'pug3_img.com', 'Fat, cute and kinda of a pig', false),
('Kireina', 'Dog', 'schnauzer_img.com', 15, 'The most beautiful, intelligent and loveliest lady ever...I miss you', false);