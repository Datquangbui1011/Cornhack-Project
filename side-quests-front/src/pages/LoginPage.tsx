import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import '../styles/LoginRegister.css';

const Login: React.FC = () => {
    const navigate = useNavigate();

    const handleLogin = () => {
        // Handle the login logic with backend here
        navigate('/home');
    };

    return (
        <div className="login-register-container">
            <h1>Login</h1>
            <p>Please login with your existing account.</p>
            {/* Add form elements here */}
            <button onClick={handleLogin}>Login</button>
            <p>If you don't have one, create it.</p>
            <Link to="/register">
                <button onClick={handleLogin}>Register</button>
            </Link>
        </div>
    );
};

export default Login;