import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/LoginRegister.css';

const LoginRegister: React.FC = () => {
    const navigate = useNavigate();

    const handleLogin = () => {
        // Your login logic here
        navigate('/dashboard'); // or another route after login
    };

    return (
        <div className="login-register-container">
            <h1>Login / Register</h1>
            <p>Please login or create an account to continue.</p>
            {/* Add your form elements here */}
            <button onClick={handleLogin}>Submit</button>
        </div>
    );
};

export default LoginRegister;