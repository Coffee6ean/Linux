import React, { useState } from "react";
import Cell from "./Cell";

const Row = ({ numOfCells = 30 }) => {
    const [row, setRow] = useState(
        Array.from({ length: numOfCells }, (_, idx) => ({
            id: idx, // Unique identifier for each cell
            //color: 'red', // Default color for cells
            sizeX: 75, // Default width
            sizeY: 40, // Default height
        }))
    );

    function addCell() {
        const newCell = {
            id: row.length, // Unique identifier for the new cell
            color: 'blue', // Example color for new cells
            sizeX: 75,
            sizeY: 40,
        };
        setRow([...row, newCell]); // Add new cell to the row
    }

    function removeLastCell() {
        if (row.length > 0) {
            setRow(row.slice(0, row.length - 1)); // Remove the last cell
        }
    }

    return (
        <div className="container-row" style={{ display: 'flex' }}>
            {row.map(cell => (
                <Cell 
                    key={cell.id} // Unique key for each cell
                    id={cell.id}  // Pass the id as a prop
                    color={cell.color} // Pass the color as a prop
                    sizeX={cell.sizeX} // Pass the width as a prop
                    sizeY={cell.sizeY} // Pass the height as a prop
                />
            ))}
        </div>
    );
}

export default Row;
