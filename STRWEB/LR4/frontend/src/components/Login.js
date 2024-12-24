import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Auth.css';
import { useNavigate } from 'react-router-dom';

const Login = ({ setIsAuthenticated, setNameApp, setUsernameApp }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errors, setErrors] = useState({});
    const navigate = useNavigate();

    // Проверяем, есть ли уже токен в localStorage
    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            setIsAuthenticated(true);
            navigate('/');
        }
    }, [setIsAuthenticated, navigate]);


    const validateForm = () => {
        const newErrors = {};

        if (!username.trim()) {
            newErrors.username = 'Логин не может быть пустым';
        }

        if (!password.trim()) {
            newErrors.password = 'Пароль не может быть пустым';
        }

        return newErrors;
    };

    const handleLogin = async () => {
        const validationErrors = validateForm();

        if (Object.keys(validationErrors).length > 0) {
            setErrors(validationErrors);
            return;
        }

        try {
            const response = await axios.post('/api/auth/login', { username, password });
            const { token, user } = response.data;

            localStorage.setItem('token', token);
            localStorage.setItem('username', user.username);
            localStorage.setItem('name', user.name);
            setIsAuthenticated(true);
            setNameApp(user.name);
            setUsernameApp(user.username);

            navigate('/');
        } catch (error) {
            const errorMessage = error?.response?.data?.message || 'Произошла ошибка при входе';
            setErrors({password: errorMessage});
        }
    };

    const handleFacebookLogin = () => {
        window.location.href = 'http://localhost:5000/api/auth/facebook';
    };

    return (
        <div className="auth-form">
            <h1>Вход</h1>
            <input
                type="text"
                placeholder="Логин"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            {errors.username && <span className="error">{errors.username}</span>}
            <input
                type="password"
                placeholder="Пароль"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            {errors.password && <span className="error">{errors.password}</span>}
            <button onClick={handleLogin}>Войти</button>
            <button onClick={handleFacebookLogin}>Войти через Facebook</button>
        </div>
    );
};

export default Login;