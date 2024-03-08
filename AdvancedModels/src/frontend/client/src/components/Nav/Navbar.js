import React from 'react';
import {Link} from 'react-router-dom';
import './Navbar.css'; 

function Navbar () {
    return (
        <nav className="Navbar">
            <Link to='/'>Landing Page</Link>
            <Link to='/home'>Home Page</Link>
            <Link to='/project'>Project Page</Link>
            <Link to='/map'>Map Page</Link>
        </nav>
    );
}

export default Navbar;
