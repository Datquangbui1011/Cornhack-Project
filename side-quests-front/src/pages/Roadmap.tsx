import React from 'react';
import { useNavigate } from 'react-router-dom';
import { VerticalTimeline, VerticalTimelineElement } from 'react-vertical-timeline-component';
import 'react-vertical-timeline-component/style.min.css';
import '../styles/Roadmap.css';

interface Project {
    id: number;
    title: string;
    completed: boolean;
}

const projects: Project[] = [
    { id: 1, title: 'Project Alpha', completed: true },
    { id: 2, title: 'Project Beta', completed: false },
    { id: 3, title: 'Project Gamma', completed: false },
    { id: 4, title: 'Project Delta', completed: false },
];

const Roadmap: React.FC = () => {
    const navigate = useNavigate();

    const handleViewDetails = (project: Project) => {
        navigate('/project-details', { state: { project } });
    };

    return (
        <div className="roadmap-container">
            <VerticalTimeline lineColor="#e0e0e0">
                {projects.map((project) => (
                    <VerticalTimelineElement
                        key={project.id}
                        iconStyle={{
                            background: project.completed ? '#4caf50' : '#f44336',
                            color: '#fff',
                        }}
                        contentStyle={{
                            background: 'rgba(255, 255, 255, 0.6)', // Keep the background
                            color: 'black',
                            borderRadius: '6px', // Reduced border radius for a smaller box
                            padding: '8px 12px', // Reduced padding for a smaller box
                            fontSize: '0.9rem', // Smaller font size for the content,
                            

                        }}
                    >
                        <h3 className="project-title">{project.title}</h3>
                        <button
                            className="view-button"
                            onClick={() => handleViewDetails(project)}
                        >
                            View Details
                        </button>
                    </VerticalTimelineElement>
                ))}
            </VerticalTimeline>
        </div>
    );
};

export default Roadmap;
