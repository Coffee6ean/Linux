CREATE TABLE crews (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    start_date DATETIME,
    end_date DATETIME,
    is_available BOOLEAN DEFAULT true,
    member_count INT,
    activities_completed INT,
    activities_assigned INT,

    --Entities associeted with this table
    activity_id INT FOREIGN KEY,
    created_by INT FOREIGN KEY,
    updated_by INT FOREIGN KEY,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)