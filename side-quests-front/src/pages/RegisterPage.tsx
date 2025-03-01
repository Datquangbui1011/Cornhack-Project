import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom'; 
import { useState } from 'react';
import '../styles/LoginRegister.css';

// const Register: React.FC = () => {
//     const navigate = useNavigate();

//     const handleRegister = () => {
//         // Handle the login logic with backend here
//         navigate('/login');
//     };

//     return (
//         <div className="login-register-container">
//             <h1>Register</h1>
//             <p>Please create an account.</p>
//             {/* Add form elements here */}
//             <button onClick={handleRegister}>Register</button>
//         </div>
//     );
// };

const Register: React.FC = () => {
    const navigate = useNavigate();
    const [name, setName] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');

    const handleRegister = (event: React.FormEvent) => {
        event.preventDefault();
        // Handle the registration logic with backend here
        if (name && username && password && email) {
            navigate('/home');
        } else {
            alert('Please fill out all fields');
        }
    };

    return (
        <div className="login-register-container">
            <h1>Register</h1>
            <p>Please fill in the details to create an account.</p>
            <form onSubmit={handleRegister}>
                <div>
                    <label htmlFor="name">Name</label>
                    <input
                        type="text"
                        id="name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                </div>
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
                    <label htmlFor="email">Email</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
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
                <button type="submit">Register</button>
            </form>
            <p>If you already have an account, log in here.</p>
            <Link to="/login">
                <button>Login</button>
            </Link>
        </div>
    );
};

export default Register;