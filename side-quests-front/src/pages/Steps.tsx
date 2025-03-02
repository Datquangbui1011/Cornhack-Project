import React, { useState } from 'react';
import './../styles/Steps.css';

const initialStepsData = [
    { id: 1, title: 'Step 1', description: 'Description for step 1.', completed: false },
    { id: 2, title: 'Step 2', description: 'Description for step 2.', completed: false },
    { id: 3, title: 'Step 3', description: 'Description for step 3.', completed: false },
    { id: 4, title: 'Step 5', description: 'Description for step 1.', completed: false },
    { id: 5, title: 'Step 3', description: 'Description for step 2.', completed: false },
    { id: 6, title: 'Step 2', description: 'Description for step 3.', completed: false },
    // Add more steps as needed
];

const Steps: React.FC = () => {
    const [stepsData, setStepsData] = useState(initialStepsData);

    const handleTaskCompletion = (id: number) => {
        const updatedSteps = stepsData.map(step =>
            step.id === id ? { ...step, completed: !step.completed } : step
        );
        setStepsData(updatedSteps);
        // Additional logic can be implemented here
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
        </div>
    );
};

export default Steps;
