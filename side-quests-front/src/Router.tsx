import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import LoginRegister from './pages/LoginRegister';
// Import other page components as needed

const AppRouter: React.FC = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/login" element={<LoginRegister />} />
                {/* Add more routes here */}
            </Routes>
        </Router>
    );
};

export default AppRouter;