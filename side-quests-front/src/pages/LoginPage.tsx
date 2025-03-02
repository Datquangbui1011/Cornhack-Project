import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import '../styles/LoginRegister.css';
import './../index.css'

const Login: React.FC = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = (event: React.FormEvent) => {
        event.preventDefault();
        // Handle the login logic with backend here
        if (username && password) {
            navigate('/home');
        } else {
            alert('Please enter both username and password');
        }
    };

    return (
        <div className="login-register-container">
            <h1>Login</h1>
            <p>Please login with your existing account</p>
            <div className="form-container">
                <form onSubmit={handleLogin}>
                    <div>
                        <label htmlFor="username">Username</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                    </div>
                    <div>
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    <button type="submit">Login</button>
                </form>
            </div>
            <p>If you dont have an account create one</p>
            <Link to="/register">
                <button>Register</button>
            </Link>
        </div>
    );
};

export default Login;
