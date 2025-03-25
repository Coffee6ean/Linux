-- Create a 'Colors' table
CREATE TABLE shared_schema.colors (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,      -- Type of color (e.g., Primary, Secondary, All)
    category VARCHAR(50) NOT NULL,  -- Category of the color (e.g., Brand, Error, Background)
    notes TEXT,
    color_name VARCHAR(50),         -- Name of the color (e.g., Primary Blue, Error Red)
    hex_code CHAR(7) NOT NULL,      -- HEX code of the color (e.g., #1A73E8)
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
