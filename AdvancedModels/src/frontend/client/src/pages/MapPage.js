import React from "react";
import { Typography } from "@mui/material";
import Cell from "../components/GridSystem/Cell"; 
import Row from "../components/GridSystem/Row";
import Grid from "../components/GridSystem/Grid";

function MapPage () {
    return (
        <div>
            <Typography variant="h1">Map Page</Typography>
            <Grid/>
        </div>
    );
}

export default MapPage;
