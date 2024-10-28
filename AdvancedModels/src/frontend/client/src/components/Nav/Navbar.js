import React from 'react';
import {Link} from 'react-router-dom';
import { useTheme } from '@mui/material/styles';
import './Navbar.css'; 

function Navbar() {
    const theme = useTheme();

    return (
        <nav className="Navbar" style={{ fontFamily: theme.typography.fontFamily}}>
            <Link to='/'>Landing Page</Link>
            <Link to='/home'>Home Page</Link>
            <Link to='/project'>Project Page</Link>
            <Link to='/map'>Map Page</Link>
        </nav>
    );
}


export default Navbar;
