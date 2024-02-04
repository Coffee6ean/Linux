-- projects.sql
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    description TEXT,
    link TEXT,
    topic TEXT,
    board TEXT,
    user_id INTEGER REFERENCES users(id)
);
