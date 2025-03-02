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
                <div className="card-container" onClick={() => handleChoice('crewmember')}>
                    <div className="card">
                        <div className="card-front path-button-crew">
                            <span className="button-text">Crew Member</span>
                        </div>
                        <div className="card-back">
                            <p>Be part of the crew and support the mission</p>
                        </div>
                    </div>
                </div>

                <div className="card-container" onClick={() => handleChoice('pilot')}>
                    <div className="card">
                        <div className="card-front path-button-pilot">
                            <span className="button-text">Pilot</span>
                        </div>
                        <div className="card-back">
                            <p>Take control and navigate the journey</p>
                        </div>
                    </div>
                </div>

                <div className="card-container" onClick={() => handleChoice('commander')}>
                    <div className="card">
                        <div className="card-front path-button-commander">
                            <span className="button-text">Commander</span>
                        </div>
                        <div className="card-back">
                            <p>Lead the mission and make critical decisions</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PathChoice;
