import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/LoginRegister.css';

const Register: React.FC = () => {
    const navigate = useNavigate();

    const handleRegister = () => {
        // Handle the login logic with backend here
        navigate('/login');
    };

    return (
        <div className="login-register-container">
            <h1>Register</h1>
            <p>Please create an account.</p>
            {/* Add form elements here */}
            <button onClick={handleRegister}>Register</button>
        </div>
    );
};

export default Register;