import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import './../styles/Steps.css';

const initialStepsData = [
    { id: 1, title: 'Step 1', description: 'Description for step 1', details: ["Details about Step 1", "Step 1 information"], completed: false },
    { id: 2, title: 'Step 2', description: 'Description for step 2', details: ["Details about Step 2", "Step 2 information"], completed: false },
    { id: 3, title: 'Step 3', description: 'Description for step 3', details: ["Details about Step 3", "Step 3 information"], completed: false },
    { id: 4, title: 'Step 4', description: 'Description for step 4', details: ["Details about Step 4", "Step 4 information"], completed: false },
    { id: 5, title: 'Step 5', description: 'Description for step 5', details: ["Details about Step 5", "Step 5 information"], completed: false },
    { id: 6, title: 'Step 6', description: 'Description for step 6', details: ["Details about Step 6", "Step 6 information"], completed: false },
];

const Steps: React.FC = () => {
    const [stepsData, setStepsData] = useState(initialStepsData);
    const [showConfirmation, setShowConfirmation] = useState(false);
    const [showWellDone, setShowWellDone] = useState(false);
    const [selectedDetail, setSelectedDetail] = useState<string[] | null>(null); // Changed to handle array of details
    const [slideAway, setSlideAway] = useState(false);
    const [isReturningToRoadmap, setIsReturningToRoadmap] = useState(false); // New state for returning
    const navigate = useNavigate(); // Hook to navigate programmatically

    useEffect(() => {
        const allCompleted = stepsData.every(step => step.completed);
        if (allCompleted) {
            setShowConfirmation(true);
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
            setShowWellDone(false);
        }
        setShowConfirmation(false);
        if (choice === 'No') {
            setShowWellDone(true);
            setSlideAway(true);
            setTimeout(() => {
                setIsReturningToRoadmap(true); // Show returning message
                setTimeout(() => {
                    // After a delay, navigate to the roadmap page
                    navigate('/roadmap');
                }, 2000); // Delay navigation for 2 seconds (adjust as needed)
            }, 1000); // Wait for slide-away animation to finish
        }
    };

    return (
        <div className={`steps-container ${slideAway ? 'slide-away' : ''}`}>
            {stepsData.map((step) => (
                <div
                    key={step.id}
                    className={`step ${step.completed ? 'completed' : ''} ${slideAway ? 'slide-out' : ''}`}
                >
                    <input
                        type="checkbox"
                        checked={step.completed}
                        onChange={() => handleTaskCompletion(step.id)}
                    />
                    <div className="step-content">
                        <h3>{step.title}</h3>
                        <p>{step.description}</p>
                        <button onClick={() => setSelectedDetail(step.details)}>Detail</button>
                    </div>
                </div>
            ))}

            {showConfirmation && (
                <div className="confirmation-box">
                    <p>All tasks are complete! Do you want to check again?</p>
                    <button onClick={() => handleConfirmationChoice('No')}>No</button>
                    <button onClick={() => handleConfirmationChoice('yes')}>Yes</button>
                </div>
            )}

            {selectedDetail && (
                <div className="detail-popup">
                    <div className="detail-content">
                        <h3>Step Details:</h3>
                        <ul>
                            {selectedDetail.map((detail, index) => (
                                <li key={index}>{detail}</li>
                            ))}
                        </ul>
                        <button onClick={() => setSelectedDetail(null)}>Close</button>
                    </div>
                </div>
            )}

            {showWellDone && (
                <div className="well-done-box">
                    WELL DONE
                </div>
            )}

            {isReturningToRoadmap && (
                <div className="roadmap-container">
                    <p>Returning to the roadmap...</p>
                </div>
            )}
        </div>
    );
};

export default Steps;
