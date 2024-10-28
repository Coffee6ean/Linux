CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_recovered BOOLEAN DEFAULT false,
    website TEXT,
    priority INT,
    location VARCHAR(100)
    color VARCHAR(25),
    planned_start DATETIME NOT NULL,
    planned_finish DATETIME NOT NULL,
    actual_start DATETIME,
    actual_finish DATETIME,
    budget DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2),
    total_construction_plans INT,

    --Entities associeted with this table
    client_project_manager_id INT FOREIGN KEY,
    client_superintendent_id INT FOREIGN KEY,
    project_manager_id INT FOREIGN KEY,
    lead_engineer_id INT FOREIGN KEY,
    tag_id INT FOREIGN KEY,
    created_by INT FOREIGN KEY,
    updated_by INT FOREIGN KEY,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
)