import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/LandingPage.css';

const LandingPage: React.FC = () => {
    return (
        <div className="landing-container">
            <h1>Welcome to sideQuests</h1>
            <p>Your rad roadmap to get to your coding portfolio.</p>
            <Link to="/login">
                <button>Login</button>
            </Link>
            <Link to="/register">
                <button>Register</button>
            </Link>
        </div>
    );
};

export default LandingPage;