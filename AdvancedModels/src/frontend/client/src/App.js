import React from "react";
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Navbar from "./components/Nav/Navbar";
import AppRouter from "./routes/AppRouter";

const theme = createTheme({
  palette: {
    primary: {
      main: '#C294CB'
    },
    secondary: {
      main: '#fefefe'
    }
  },
  typography: {
    fontFamily: 'Rubik'
  }
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <div className="App">
        <Navbar/>
        <AppRouter/> 
      </div>
    </ThemeProvider>
  );
}

export default App;
