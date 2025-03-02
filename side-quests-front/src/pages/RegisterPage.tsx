import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import axios from "axios";
import "../styles/LoginRegister.css";

const BASE_URL = process.env.REACT_APP_BASE_URL;

const Register: React.FC = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [registered, setRegistered] = useState(false);

    const clearForm = () => {
        setEmail("");
        setPassword("");
        setConfirmPassword("");
    };

    const handleRegister = async (event: React.FormEvent) => {
        event.preventDefault();

        if (!email || !password || !confirmPassword) {
            alert("Please fill out all fields");
            return;
        }

        if (password !== confirmPassword) {
            alert("Passwords do not match");
            return;
        }

        try {
            const response = await axios.post(`${BASE_URL}/users/`, {
                email,
                role: "user",
                password,
            });

            if (response.status === 200) {
                if (response.data?.id) {
                    setRegistered(true);
                } else {
                    alert("Unexpected response format.");
                }
            }
        } catch (error: any) {
            if (error.response) {
                if (error.response.status === 404) {
                    alert("Error: The requested resource was not found.");
                } else if (error.response.data?.detail) {
                    alert(error.response.data.detail);
                } else {
                    alert("An error occurred during registration.");
                }
            } else {
                alert("Network error. Please try again.");
            }
        } finally {
            clearForm();
        }
    };

    return (
        <div className="login-register-container">
            {!registered && <h1>Register</h1>}
            {registered ? (
                <p>Registration successful!</p>
            ) : (
                <p>Please fill in the details to create an account</p>
            )}
            {!registered && (
                <form onSubmit={handleRegister} className="form-container">
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
                    <div>
                        <label htmlFor="confirmPassword">
                            Confirm Password
                        </label>
                        <input
                            type="password"
                            id="confirmPassword"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                        />
                    </div>
                    <button type="submit">Register</button>
                </form>
            )}
            {registered ? (
                <p>Login to continue</p>
            ) : (
                <p>If you already have an account, log in here.</p>
            )}
            <Link to="/login">
                <button>Login</button>
            </Link>
        </div>
    );
};

export default Register;
