import React from 'react';
import { Routes, Route } from 'react-router-dom';

// Website Pages
import LandingPage from '../pages/LandingPage';
import HomePage from '../pages/HomePage';
import ProjectPage from '../pages/project/ProjectPage';
import MapPage from '../pages/MapPage';

function AppRouter() {
    return (
        <div>
            <Routes>
                <Route path="/" element={<LandingPage/>}/>
                <Route path="/home" element={<HomePage/>}/>
                <Route path="/project" element={<ProjectPage/>}/>
                <Route path="/map" element={<MapPage/>}/>
            </Routes>
        </div>
    );
}

export default AppRouter;
 