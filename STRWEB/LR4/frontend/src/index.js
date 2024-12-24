import React from 'react';
import ReactDOM from 'react-dom/client'; // импортируем из react-dom/client
import App from './App';
import axios from 'axios';
import './index.css';

// Устанавливаем базовый URL для Axios
axios.defaults.baseURL = 'http://localhost:5000';

// Создаем корень и рендерим приложение
const root = ReactDOM.createRoot(document.getElementById('root')); // создаем корень

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
