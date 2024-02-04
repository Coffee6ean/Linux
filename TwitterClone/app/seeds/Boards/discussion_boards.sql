-- discussion_boards.sql
CREATE TABLE boards (
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    description TEXT,
    topic TEXT,
    board TEXT,
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    picture TEXT,
    topic VARCHAR(255),
    user_id INTEGER REFERENCES users(id),
    board_id INTEGER REFERENCES boards(id)
);
