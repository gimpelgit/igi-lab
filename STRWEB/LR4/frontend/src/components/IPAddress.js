import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const IPAddress = () => {
    const [ipAddress, setIpAddress] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
            return;
        }

        axios.get('/api/ip')
            .then((response) => {
                setIpAddress(response.data.ip);
            })
            .catch((error) => {
                console.error('Ошибка при получении IP-адреса:', error);
            });
    }, [navigate]);

    return (
        <div>
            <h2>Ваш IP-адрес</h2>
            <p>{ipAddress || 'Загрузка...'}</p>
        </div>
    );
};

export default IPAddress;