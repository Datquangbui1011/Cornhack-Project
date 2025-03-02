import React, { useState, useEffect } from 'react';
import './../styles/Steps.css';

const initialStepsData = [
    { id: 1, title: 'Step 1', description: 'Description for step 1.', details: ["detail1", "detail2"], completed: false },
    { id: 2, title: 'Step 2', description: 'Description for step 2.', details: ["detail1", "detail2", "detail3"], completed: false },
    { id: 3, title: 'Step 3', description: 'Description for step 3.', details: ["detail1"], completed: false },
    { id: 4, title: 'Step 5', description: 'Description for step 1.', details: ["detail1", "detail2"], completed: false },
    { id: 5, title: 'Step 3', description: 'Description for step 2.', details: ["detail1", "detail2"], completed: false },
    { id: 6, title: 'Step 2', description: 'Description for step 3.', details: ["detail1", "detail2"], completed: false },
];

const Steps: React.FC = () => {
    const [stepsData, setStepsData] = useState(initialStepsData);
    const [showConfirmation, setShowConfirmation] = useState(false);
    const [showWellDone, setShowWellDone] = useState(false);

    useEffect(() => {
        const allCompleted = stepsData.every(step => step.completed);
        if (allCompleted) {
            setShowConfirmation(true); // Show the Yes/No confirmation when all steps are complete
        }
    }, [stepsData]);

    const handleTaskCompletion = (id: number) => {
        const updatedSteps = stepsData.map(step =>
            step.id === id ? { ...step, completed: !step.completed } : step
        );
        setStepsData(updatedSteps);
    };

    const handleConfirmationChoice = (choice: string) => {
        if (choice === 'yes') {
            setShowWellDone(true);
        }
        setShowConfirmation(false);
    };

    return (
        <div className="steps-container">
            {stepsData.map((step) => (
                <div key={step.id} className={`step ${step.completed ? 'completed' : ''}`}>
                    <input
                        type="checkbox"
                        checked={step.completed}
                        onChange={() => handleTaskCompletion(step.id)}
                    />
                    <div className="step-content">
                        <h3>{step.title}</h3>
                        <p>{step.description}</p>
                    </div>
                </div>
            ))}

            {showConfirmation && (
                <div className="confirmation-box">
                    <p>All tasks are complete Do you want to see them again</p>
                    <button onClick={() => handleConfirmationChoice('yes')}>Yes</button>
                    <button onClick={() => handleConfirmationChoice('no')}>No</button>
                </div>
            )}

            {showWellDone && (
                <div className="well-done-box">
                    WELL DONE
                </div>
            )}
        </div>
    );
};

export default Steps;
