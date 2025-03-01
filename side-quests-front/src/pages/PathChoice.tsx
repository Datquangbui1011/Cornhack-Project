import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/PathChoice.css';

const PathChoice: React.FC = () => {
    const navigate = useNavigate();

    const handleChoice = (choice: string) => {
        navigate(`/roadmap?path=${choice}`);
    };

    return (
        <div className="path-choice-container">
            <h1>Choose Your Path</h1>
            <div className="buttons-container">
                <button className="path-button-com" onClick={() => handleChoice('comander')}>
                    The Comander
                </button>
                <button className="path-button-tank" onClick={() => handleChoice('tanker')}>
                    The Tanker
                </button>
                <button className="path-button-flank" onClick={() => handleChoice('flanker')}>
                    The Flanker
                </button>
            </div>
        </div>
    );
};

export default PathChoice;
