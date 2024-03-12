import React from "react";
import { Typography, Grid, Container } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import "./HomePage.css";

function HomePage() {
    const theme = useTheme();

    return (
        <Container maxWidth="lg" className="full-height">
            <div className="home-page-body">
                <Typography variant="h1">Home Page</Typography>
                <Grid container spacing={0} className="grid-container" sx={{ backgroundColor:'#FCB5A5', margin: '10px' }}>
                    <Grid item xs={12} md={6} className="grid-item" sx={{ margin: '10px' }}>
                        <img className="grid-image" src="https://images.unsplash.com/photo-1591696205602-2f950c417cb9?q=80&w=1770&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="Image" />
                    </Grid>
                    <Grid item xs={12} md={6} className="grid-item" sx={{ margin: '10px' }}>
                        <Typography>Hello World</Typography>
                    </Grid>
                </Grid>
                <Grid container spacing={0} sx={{ backgroundColor:'#FCB5A5', margin: '10px' }}> 
                    <Grid item sx={{ margin: '10px' }}>
                        <Typography>Hello World</Typography>
                    </Grid>
                </Grid>
            </div>
        </Container>
    );
}

export default HomePage;
