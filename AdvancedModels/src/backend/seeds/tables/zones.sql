CREATE TABLE zones (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    order INT,
    status VARCHAR(10),
    color VARCHAR(25),
    start_date DATETIME,
    end_date DATETIME,
    total_ssus INT,

    --Entities associeted with this table
    area_id INT FOREIGN KEY,
    created_by INT FOREIGN KEY,
    updated_by INT FOREIGN KEY,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)