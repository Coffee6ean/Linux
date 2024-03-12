import React, { useState } from "react";
import { Typography, Container, Grid } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import CardBlock from "../../components/Card/CardBlock";

import ProjectForm from "./ProjectForm";

function ProjectPage () {
    const theme = useTheme();

    const project1 = {
        title: 'Project Example 1',
        category: 'Extreme'
    }
    const project2 = {
        title: 'Project Example 2',
        category: 'Hard'
    }
    const project3 = {
        title: 'Project Example 3',
        category: 'Easy'
    }
    const [blockProject, setBlockProject] = useState([project1, project2, project3]);

    return (
        <div>
            <Typography variant="h1" sx={{fontFamily: theme.typography.fontFamily}}>Project Page</Typography>
            <ProjectForm/>
            <Container>
                <Grid container>
                    {blockProject.map(project => (
                        <Grid item xs={12} md={6} lg={4}>
                            <CardBlock card={project}/>
                        </Grid>
                    ))}
                </Grid>
            </Container>
        </div>
    );
}

export default ProjectPage;
