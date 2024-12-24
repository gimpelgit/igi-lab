import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import axios from 'axios';
import './index.css';

// Базовый URL для Axios
axios.defaults.baseURL = 'http://localhost:5000';

const root = ReactDOM.createRoot(document.getElementById('root'));

const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get('token');
const username = urlParams.get('username');
const name = urlParams.get('name');

if (token) {
    localStorage.setItem('token', token);
    localStorage.setItem('username', username);
    localStorage.setItem('name', name);
    window.history.replaceState({}, document.title, '/');
}

axios.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});


root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
