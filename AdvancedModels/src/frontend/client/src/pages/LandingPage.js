import React from "react";
import { useTheme } from "@mui/material/styles";
import { Typography } from "@mui/material";

function LandingPage () {
    const theme = useTheme();

    return (
        <div>
            <Typography variant="h1">Landing Page</Typography>
        </div>
    );
}

export default LandingPage;
