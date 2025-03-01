import React from 'react';
import { useNavigate } from 'react-router-dom';
import './../styles/PathChoice.css';

const PathChoice: React.FC = () => {
    const navigate = useNavigate();

    const handleChoice = (choice: string) => {
        navigate(`/roadmap?path=${choice}`);
    };

    return (
        <div className="path-choice-container">
            <h1>Choose Your Path</h1>
            <div className="buttons-container">
                <button className="path-button path-button-crew" onClick={() => handleChoice('crewmember')}>
                    <span className="button-text">Crew Member</span>
                </button>
                <button className="path-button path-button-pilot" onClick={() => handleChoice('pilot')}>
                    <span className="button-text">Pilot</span>
                </button>
                <button className="path-button path-button-commander" onClick={() => handleChoice('commander')}>
                    <span className="button-text">Commander</span>
                </button>
            </div>
        </div>
    );
};

export default PathChoice;
