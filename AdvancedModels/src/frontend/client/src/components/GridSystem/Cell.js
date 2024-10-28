import React from "react";

const Cell = ({ id, color = "#353535", background_color = '#FFFFFF', sizeX = 75, sizeY = 40 }) => {
    return (
        <div
            className="container-cell"
            id={`cell-${id}`} // Set the id as an attribute
            style={{
                color: color,
                backgroundColor: background_color,
                border: '1px solid #E0E0E0',
                width: `${sizeX}px`, // Use sizeX directly
                height: `${sizeY}px`, // Use sizeY directly
                fontFamily: 'rubik',
                fontSize: '16px', // Set a fixed font size
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
            }}
        >
            <div className='child' style={{ padding: '5px' }}>
            </div>
        </div>
    );
}

export default Cell;
