import React, { useState } from "react";
import Cell from "./Cell";
import Row from "./Row";

const Grid = ({ numOfRows = 20, numOfCells = 30 }) => {
    const [grid, setGrid] = useState(
        Array.from({ length: numOfRows }, (_, rowIndex) => ({
            id: rowIndex, // Unique identifier for each row
            cells: Array.from({ length: numOfCells }, (_, cellIndex) => ({
                id: `cell-${rowIndex}-${cellIndex}`, // Unique identifier for each cell
                color: 'red', // Default color for cells
                sizeX: 75, // Default width
                sizeY: 40, // Default height
            })),
        }))
    );

    function addRow() {
        const newRow = {
            id: grid.length, // Unique identifier for the new row
            cells: Array.from({ length: numOfCells }, (_, cellIndex) => ({
                id: `cell-${grid.length}-${cellIndex}`, // Unique identifier for each cell
                color: 'blue', // Example color for new cells
                sizeX: 75,
                sizeY: 40,
            })),
        };
        setGrid([...grid, newRow]); // Add new row to the grid
    }

    function removeLastRow() {
        if (grid.length > 0) {
            setGrid(grid.slice(0, grid.length - 1)); // Remove the last row
        }
    }

    return (
        <div>
            {grid.map(row => (
                <Row
                    key={row.id} // Unique key for each row
                    id={row.id} // Pass the row id as a prop
                    cells={row.cells} // Pass the cells array as a prop
                />
            ))}
            <button onClick={addRow}>Add Row</button>
            <button onClick={removeLastRow}>Remove Last Row</button>
        </div>
    );
};

export default Grid;
