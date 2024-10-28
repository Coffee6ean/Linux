CREATE TABLE construction_plans (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    priority INT,
    start_date DATETIME,
    end_date DATETIME,
    budget DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2),
    total_phases INT,

    --Entities associeted with this table
    project_id INT FOREIGN KEY,
    contact_person_id INT FOREIGN KEY,
    tag_id INT FOREIGN KEY,
    created_by INT FOREIGN KEY,
    updated_by INT FOREIGN KEY,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)