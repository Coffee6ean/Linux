CREATE TABLE materials (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    status VARCHAR(10),
    priority VARCHAR(10),
    total_units INT,
    unit_price DECIMAL(10,2),
    total_cost DECIMA(10,2),
    delivery_date DATETIME
    is_ready BOOLEAN DEFAULT true,

    --Entities associeted with this table
    crew_id INT FOREIGN KEY,
    supplier_id INT FOREIGN KEY,
    created_by INT FOREIGN KEY,
    updated_by INT FOREIGN KEY,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)