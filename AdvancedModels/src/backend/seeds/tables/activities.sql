CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    status VARCHAR(10),
    priority VARCHAR(10),
    start_date DATETIME,
    end_date DATETIME,

    --Entities associeted with this table
    trade_id INT FOREIGN KEY,
    created_by INT FOREIGN KEY,
    updated_by INT FOREIGN KEY,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)