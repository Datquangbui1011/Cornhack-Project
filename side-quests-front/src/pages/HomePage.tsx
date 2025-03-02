import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/HomePage.css';

const HomePage: React.FC = () => {
    const navigate = useNavigate();

    // Dummy state variable to simulate if the user has chosen a path
    const [hasChosenPath] = useState(false);

    const handleStart = () => {

        if (hasChosenPath) {
            navigate('/roadmap')
        } else {
            navigate('/path-choice');
        }
    };

    return (
        <div className="home-container">
            <h1 className="home-title">Hello Adventurer</h1>
            <p className="home-text">
                {hasChosenPath ? "Let's continue fighting" : "Are you ready to embark on this odyssey"}
            </p>
            <button className="start-button" onClick={handleStart}>
                Start
            </button>
        </div>
    );
};

export default HomePage;
