import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const DogImage = () => {
    const [imageUrl, setImageUrl] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
            return;
        } else {
            fetchDog();
        }

    }, [navigate]);

    const fetchDog = async () => {
        try {
            const response = await axios.get('/api/random-dog');
            setImageUrl(response.data.message);
        } catch (error) {
            console.error('Ошибка при загрузке машин:', error);
        }
    }

    return (
        <div>
            <h2>Случайное изображение собаки</h2>
            {imageUrl ? (
                <img src={imageUrl} alt="Случайная собака" style={{ maxWidth: '500px' }} />
            ) : (
                <p>Загрузка...</p>
            )}
        </div>
    );
};

export default DogImage;