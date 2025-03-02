import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import axios from 'axios'; // Use axios without curly braces
import '../styles/LoginRegister.css';
import './../index.css';

const BASE_URL = 'YOUR_BASE_URL_HERE'; // Replace with your actual base URL

const Login: React.FC = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = async (event: React.FormEvent) => {
        event.preventDefault();

        if (username && password) {
            try {
                const response = await axios.post(`${BASE_URL}/token`, {
                    email: username,
                    password: password,
                });

                if (response.status === 200) {
                    const token = response.data.token;
                    localStorage.setItem('authToken', token);
                    navigate('/home');
                }
            } catch (error: any) {
                if (error.response && error.response.status === 401) {
                    alert('Invalid authentication');
                } else {
                    alert('An error occurred. Please try again.');
                }
            }
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
                        <label htmlFor="username">Email</label>
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
            <p>If you don't have an account, create one</p>
            <Link to="/register">
                <button>Register</button>
            </Link>
        </div>
    );
};

export default Login;
