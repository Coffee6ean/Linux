CREATE TABLE ssus (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    surface_area DECIMAL(10,2) NOT NULL,
    work_density INT NOT NULL,
    status VARCHAR(10),
    color VARCHAR(25),
    start_date DATETIME,
    end_date DATETIME,
    is_vertical_area BOOLEAN DEFAULT false,
    is_ssu BOOLEAN DEFAULT false,
    total_trades INT,

    --Entities associeted with this table
    section_id INT FOREIGN KEY,
    previous_trade_id INT FOREIGN KEY,
    current_trade_id INT FOREIGN KEY,
    next_trade_id INT FOREIGN KEY,
    created_by INT FOREIGN KEY,
    updated_by INT FOREIGN KEY,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)