CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,

    --Entities associeted with this table
    project_manager_id INT FOREIGN KEY,
    lead_engineer_id INT FOREIGN KEY,
    created_by INT FOREIGN KEY,
    updated_by INT FOREIGN KEY,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)