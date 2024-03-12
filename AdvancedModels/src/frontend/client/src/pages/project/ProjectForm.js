import React, { useState } from "react";
import { Container, FormLabel, TextField } from "@mui/material";
import { Typography, Button } from "@mui/material";
import { RadioGroup, Radio, FormControlLabel } from '@mui/material';
import { createTheme, ThemeProvider } from "@mui/material";
import { useTheme } from "@mui/material/styles"
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';

// Import Components
import DropdownButton from "../../components/Dropdown/DropdownButton";

const formTheme = createTheme({
    components: {
        MuiTextField: {
            styleOverrides: {
                root: {
                    marginTop: 20,
                    marginBottom: 20,
                    display: 'block'
                }
            }
        }
    }
});

function ProjectForm () {
    const appTheme = useTheme();
    const [title, setTitle] = useState('');
    const [details, setDetails] = useState('');
    const [titleError, setTitleError] = useState(false);
    const [detailsError, setDetailsError] = useState(false);
    const [category, setCategory] = useState('todos');

    const handleSubmit = (e) => {
        e.preventDefault();
        setTitleError(false);
        setDetailsError(false);

        if(title == '') {
            setTitleError(true);
        }

        if(details == '') {
            setDetailsError(true);
        }

        if(title && details) {
            console.log(title, details, category);
        }
    };

    return (
        <Container sx={{marginBottom:'15px'}}>
            {/* 'Create Project' anchor */}
            <Typography 
                variant="h6" 
                color="textSecondary" 
                component="h2"
                gutterBottom
                sx={{
                    textDecoration: 'underline',
                    marginBottom: '10px'
                }}
            >
                Create a New Project
            </Typography>
            {/* Form Block */}
            <ThemeProvider theme={formTheme}>
                <form noValidate autoComplete="off" onSubmit={handleSubmit}>
                    {/* Title Text Block */}
                    <TextField 
                        onChange={(e) => setTitle(e.target.value)} 
                        label="Project Title" 
                        variant="outlined" 
                        fullWidth 
                        required
                        error={titleError}
                    />
                    {/* Details Text Block */}
                    <TextField 
                        onChange={(e) => setDetails(e.target.value)} 
                        label="Details" 
                        variant="outlined" 
                        multiline 
                        rows={4} 
                        fullWidth 
                        required
                        error={detailsError}
                    />
                    {/* Radio Buttons */}
                    <FormLabel>Project Category</FormLabel>
                    <RadioGroup value={category} onChange={(e) => setCategory(e.target.value)}>
                        <FormControlLabel control={<Radio/>} value="money" label="Money"/>
                        <FormControlLabel control={<Radio/>} value="todos" label="Todo"/>
                        <FormControlLabel control={<Radio/>} value="reminders" label="Reminders"/>
                        <FormControlLabel control={<Radio/>} value="work" label="Work"/>
                    </RadioGroup>
                    {/* Dropdown Button */}
                    <DropdownButton/>
                    {/* Submit Button */}
                    <Button
                        type="submit"
                        sx={{
                            backgroundColor:appTheme.palette.primary.main,
                            fontFamily: appTheme.typography.fontFamily
                        }}
                        variant="contained"
                        endIcon={<KeyboardArrowRightIcon/>}
                    >
                        Submit
                    </Button>
                </form> 
            </ThemeProvider>
        </Container>
    );
}

export default ProjectForm;
