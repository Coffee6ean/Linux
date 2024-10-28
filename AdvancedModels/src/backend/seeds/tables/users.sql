CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(50) NOT NULL,
    first_name TEXT NOT NULL,
    middle_name TEXT,
    last_name TEXT NOT NULL,
    birth_date DATE NOT NULL,
    about TEXT, 
    pronouns VARCHAR(10),
    website TEXT,
    linked_in TEXT,                 
    role VARCHAR(50),
    profession(50),
                        
    --Entities associeted with this table
    team_id FOREIGN KEY,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP                                                                            
)                                                                                   
