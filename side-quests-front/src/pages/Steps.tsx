import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import axios from "axios";
import "./../styles/Steps.css";

const BASE_URL = process.env.REACT_APP_BASE_URL;

interface Step {
    id: number;
    title: string;
    description: string;
    stepbreakdown: { id: number; description: string }[];
    completed: boolean;
}

const Steps: React.FC = () => {
    const [stepsData, setStepsData] = useState<Step[]>([]);
    const [showWellDone, setShowWellDone] = useState(false);
    const [selectedDetail, setSelectedDetail] = useState<string[] | null>(null);
    const navigate = useNavigate();
    const location = useLocation();

    // Extract project ID from the navigation state
    const project = location.state?.project;
    const projectId = project?.id;
    const projectCompleted = project?.completed;

    useEffect(() => {
        const fetchSteps = async () => {
            try {
                const token = localStorage.getItem("authToken"); // Get the auth token
                if (!token) {
                    alert("No authentication token found. Please log in.");
                    navigate("/login");
                    return;
                }

                if (!projectId) {
                    alert("Project ID not found.");
                    navigate("/roadmap");
                    return;
                }

                const response = await axios.get(`${BASE_URL}/steps/user`, {
                    params: { project_id: projectId },
                    headers: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "application/json",
                    },
                });

                if (response.status === 200) {
                    setStepsData(response.data);
                }

                console.log(response.data);
            } catch (error) {
                console.error("Error fetching steps:", error);
                alert("Failed to load steps. Please try again.");
            }
        };

        fetchSteps();
    }, [projectId, navigate]);

    useEffect(() => {
        const allCompleted = stepsData.every((step) => step.completed);
        if (allCompleted && stepsData.length > 0) {
            setShowWellDone(true);
            updateProjectCompletion(projectId, !projectCompleted);
        }
    }, [stepsData, projectId, projectCompleted]);

    const handleTaskCompletion = async (id: number) => {
        const updatedSteps = stepsData.map((step) =>
            step.id === id ? { ...step, completed: !step.completed } : step
        );

        // Find the step being updated to determine its new completion status
        const updatedStep = updatedSteps.find((step) => step.id === id);
        const newCompletionStatus = updatedStep ? updatedStep.completed : false;

        setStepsData(updatedSteps);

        // Send the updated completion status to the backend
        try {
            const token = localStorage.getItem("authToken");
            if (!token) {
                alert("No authentication token found. Please log in.");
                navigate("/login");
                return;
            }

            await axios.put(`${BASE_URL}/steps/complete/${id}`, null, {
                params: {
                    project_id: projectId,
                    completed: newCompletionStatus, // Set the new completion status
                },
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
            });
            console.log(`Step ${id} completion status updated in the backend.`);
        } catch (error) {
            console.error(
                "Error updating task completion in the backend:",
                error
            );
            alert("Failed to update task completion. Please try again.");
        }
    };

    const updateProjectCompletion = async (
        projectId: number,
        completed: boolean
    ) => {
        try {
            const token = localStorage.getItem("authToken");
            if (!token) {
                alert("No authentication token found. Please log in.");
                navigate("/login");
                return;
            }

            await axios.put(`${BASE_URL}/projects/complete`, null, {
                params: {
                    project_id: projectId,
                    completed: completed,
                },
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
            });

            console.log(
                `Project ${projectId} completion status updated to ${completed}`
            );
        } catch (error) {
            console.error("Error updating project completion:", error);
            alert("Failed to update project completion. Please try again.");
        }
    };

    return (
        <div className="steps-container">
            {/* Back Button */}
            <button
                className="back-button"
                onClick={() => navigate("/roadmap")}
            >
                ⬅ Back
            </button>

            {stepsData.map((step) => (
                <div
                    key={step.id}
                    className={`step ${step.completed ? "completed" : ""}`}
                >
                    <div className="step-content">
                        <div className="step-info">
                            <input
                                type="checkbox"
                                checked={step.completed}
                                onChange={() => handleTaskCompletion(step.id)}
                            />
                            <div>
                                <h3>{step.title}</h3>
                                <p>{step.description}</p>
                            </div>
                        </div>
                        <button
                            className="detail-button"
                            onClick={() =>
                                setSelectedDetail(
                                    step.stepbreakdown.map((b) => b.description)
                                )
                            }
                        >
                            Detail
                        </button>
                    </div>
                </div>
            ))}

            {showWellDone && (
                <>
                    <div
                        className="popup-overlay"
                        onClick={() => setShowWellDone(false)}
                    ></div>
                    <div className="well-done-popup">
                        <button
                            className="close-button"
                            onClick={() => setShowWellDone(false)}
                        >
                            ✖
                        </button>
                        <h1>WELL DONE</h1>
                        <p>You completed all tasks with amazing energy</p>
                    </div>
                </>
            )}

            {selectedDetail && (
                <>
                    <div
                        className="popup-overlay"
                        onClick={() => setSelectedDetail(null)}
                    ></div>
                    <div
                        className={`detail-popup ${
                            selectedDetail ? "" : "hidden"
                        }`}
                    >
                        <button
                            className="close-button"
                            onClick={() => setSelectedDetail(null)}
                        >
                            ✖
                        </button>
                        <div className="detail-content">
                            <h3>Step Details:</h3>
                            <ul>
                                {selectedDetail.map((detail, index) => (
                                    <li key={index}>{detail}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
};

export default Steps;
