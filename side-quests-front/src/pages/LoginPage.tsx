import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import axios from "axios";
import "../styles/LoginRegister.css";
import "./../index.css";

const BASE_URL = process.env.REACT_APP_BASE_URL;

const Login: React.FC = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = async (event: React.FormEvent) => {
        event.preventDefault();

        if (username && password) {
            try {
                const params = new URLSearchParams();
                params.append("username", username);
                params.append("password", password);

                console.log("Payload being sent:", params.toString());

                const response = await axios.post(`${BASE_URL}/token`, params, {
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                });

                if (response.status === 200) {
                    console.log(response.data);
                    const token = response.data.access_token;
                    localStorage.setItem("authToken", token);

                    const response_2 = await axios.get(
                        `${BASE_URL}/projects/user`,
                        {
                            headers: {
                                Authorization: `Bearer ${token}`,
                            },
                        }
                    );
                    console.log(response_2.data <= 0);
                    if (response_2.data.length <= 0) {
                        const projects: [] = (
                            await axios.get(`${BASE_URL}/projects`)
                        ).data;
                        let i = 1;
                        projects.forEach(async (project: any) => {
                            console.log(project);
                            try {
                                await axios.post(
                                    `${BASE_URL}/projects/user`,
                                    {},
                                    {
                                        params: { project_id: project.id },
                                        headers: {
                                            Authorization: `Bearer ${token}`,
                                        },
                                    }
                                );

                                // Prepare the data for step creation
                                const data = {
                                    project_id: project.id,
                                    step_ids: [] as number[],
                                };

                                for (let j = i; j < i + 10; j++) {
                                    data.step_ids.push(j);
                                }
                                console.log(data, i);
                                i += 10;
                                // Post to the steps creation endpoint
                                await axios.post(
                                    `${BASE_URL}/steps/create/user`,
                                    data,
                                    {
                                        headers: {
                                            Authorization: `Bearer ${token}`,
                                            "Content-Type": "application/json",
                                        },
                                    }
                                );
                            } catch (error: any) {
                                console.error(
                                    "Error posting steps:",
                                    error.response?.data || error.message
                                );
                            }
                        });
                    }
                    navigate("/home");
                }
            } catch (error: any) {
                console.log("Error response:", error.response?.data);

                if (error.response && error.response.status === 401) {
                    alert("Invalid authentication");
                } else if (error.response && error.response.status === 422) {
                    alert(
                        "Invalid input. Please check your username and password."
                    );
                } else {
                    alert("An error occurred. Please try again.");
                }
            }
        } else {
            alert("Please enter both username and password");
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
