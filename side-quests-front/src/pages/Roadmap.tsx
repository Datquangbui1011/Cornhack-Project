import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { VerticalTimeline, VerticalTimelineElement } from 'react-vertical-timeline-component';
import 'react-vertical-timeline-component/style.min.css';
import '../styles/Roadmap.css';
import { motion } from 'framer-motion';

const BASE_URL = 'http://127.0.0.1:8000';

interface Project {
    id: number;
    project_name: string;
    completed: boolean;
}

const Roadmap: React.FC = () => {
    const navigate = useNavigate();
    const [projects, setProjects] = useState<Project[]>([]);

    useEffect(() => {
        const fetchProjects = async () => {
            const token = localStorage.getItem('authToken');
            if (!token) {
                alert('No authentication token found. Please log in.');
                navigate('/login');
                return;
            }

            try {

                console.log(token)

                const response = await axios.get(`${BASE_URL}/projects/user`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                if (response.status === 200) {
                    setProjects(response.data);
                } else {
                    alert('Failed to load projects. Please try again later.');
                }
            } catch (error: any) {
                if (error.response && error.response.status === 401) {
                    alert('Authentication failed. Please log in again.');
                    localStorage.removeItem('authToken');
                    navigate('/login');
                } else {
                    alert('An error occurred while loading projects.');
                }
            }
        };

        fetchProjects();
    }, [navigate]);

    const handleViewDetails = (project: Project) => {
        navigate('/project-details', { state: { project } });
    };

    return (
        <motion.div className="roadmap-container"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
        >
            <motion.p className="roadmap-intro"
                initial={{ y: -50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 1, delay: 0.5 }}
            >
                Explore Your Journey!
            </motion.p>
            <VerticalTimeline lineColor="#e0e0e0">
                {projects.map((project, index) => (
                    <VerticalTimelineElement
                        key={project.id}
                        iconStyle={{
                            background: project.completed ? 'linear-gradient(45deg, #4caf50, #81c784)' : 'linear-gradient(45deg, #f44336, #e57373)',
                            color: '#fff',
                            boxShadow: '0px 0px 15px rgba(0, 0, 0, 0.5)',
                        }}
                        contentStyle={{
                            background: 'rgba(100, 100, 100, 0.8)',
                            color: 'black',
                            borderRadius: '15px',
                            padding: '20px',
                            boxShadow: '0px 8px 15px rgba(0, 0, 0, 0.2)',
                        }}
                        position={index % 2 === 0 ? 'left' : 'right'}
                        className={
                            index === 0 ? 'first-element' :
                                index === projects.length - 1 ? 'last-element' : ''
                        }
                        icon={<motion.div
                            initial={{ scale: 0.5 }}
                            animate={{ scale: 1 }}
                            transition={{ duration: 0.5 }}
                            style={{
                                background: project.completed ? '#4caf50' : '#f44336',
                                borderRadius: '50%',
                                width: '100%',
                                height: '100%',
                            }}
                        />}
                    >
                        <motion.h3 className="project-title"
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            {project.project_name}
                        </motion.h3>
                        <motion.button
                            className="view-button"
                            onClick={() => handleViewDetails(project)}
                            whileHover={{ scale: 1.1, boxShadow: '0px 8px 20px rgba(255, 255, 255, 0.7)' }}
                            whileTap={{ scale: 0.95 }}
                        >
                            View Details
                        </motion.button>
                    </VerticalTimelineElement>
                ))}
            </VerticalTimeline>
        </motion.div>
    );
};

export default Roadmap;
