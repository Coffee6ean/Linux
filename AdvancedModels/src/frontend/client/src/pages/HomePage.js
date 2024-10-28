import React, { useEffect, useState } from "react";
import { Typography, Grid, Container } from "@mui/material";
import { useTheme } from "@mui/material/styles";

function HomePage() {
    const theme = useTheme();

    const [projects, setProjects] = useState([]);
    useEffect(() => {
        fetch('http://localhost:8000/projects')
            .then(res => res.json())
            .then(data => setProjects(data));
    }, []);

    return (
        <div>
            {projects.map(project => (
                <p id={project.id}>{project.title}</p>
            ))}
        </div>
    );
}

export default HomePage;
