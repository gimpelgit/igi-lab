import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import './ParkingDetailPage.css';

const ParkingDetailPage = ({ isAuthenticated }) => {
    const { id } = useParams();
    const [parkingSpace, setParkingSpace] = useState(null);
    const [endDate, setEndDate] = useState('');
    const [cars, setCars] = useState([]);
    const [selectedCar, setSelectedCar] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        axios.get(`/api/parking/parking-spaces/${id}`)
            .then((response) => {
                setParkingSpace(response.data);
            })
            .catch((error) => {
                console.error('Ошибка при загрузке данных:', error);
            });

        if (isAuthenticated) {
            axios.get('/api/cars/available')
                .then((response) => {
                    setCars(response.data);
                })
                .catch((error) => {
                    console.error('Ошибка при загрузке доступных машин:', error);
                });
        }
    }, [id, isAuthenticated]);

    const handleRent = async () => {
        if (!validateForm()) {
            return;
        }

        try {
            await axios.post('/api/rentals', {
                parkingSpaceId: id,
                endDate,
                carId: selectedCar, 
            });
            alert('Аренда успешно создана!');
            navigate('/parking');
        } catch (error) {
            alert('Ошибка при аренде: ' + error.response?.data?.message);
        }
    };

    const validateForm = () => {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        const oneYearFromToday = new Date();
        oneYearFromToday.setFullYear(today.getFullYear() + 1);

        if (!endDate) {
            setErrorMessage('Выберите дату окончания аренды.');
            return false;
        }

        const selectedDate = new Date(endDate);
        selectedDate.setHours(0, 0, 0, 0);
        console.log(selectedDate)
        console.log(today)

        if (selectedDate < today) {
            setErrorMessage('Не живите прошлым днем, смотрите только вперед!');
            return false;
        }
        if (selectedDate > oneYearFromToday) {
            setErrorMessage('Вы не можете арендовать больше чем на 1 год.');
            return false;
        }

        if (!selectedCar) {
            setErrorMessage('Пожалуйста, выберите машину.');
            return false;
        }

        setErrorMessage('');
        return true;
    };

    if (!parkingSpace) {
        return <div>Загрузка...</div>;
    }

    return (
        <div className={`container parking-detail ${parkingSpace.category === 'premium' ? 'premium' : ''}`}>
            <h1>Парковочное место #{parkingSpace.number}</h1>
            <p>Цена: {parkingSpace.price} руб./день</p>
            <p>Статус: <span className={`status ${parkingSpace.isOccupied ? 'occupied' : 'free'}`}>
                {parkingSpace.isOccupied ? 'Занято' : 'Свободно'}
            </span></p>

            {isAuthenticated && !parkingSpace.isOccupied && (
                <div className="rental-form">
                    <h2>Арендовать до</h2>
                    <input
                        type="date"
                        value={endDate}
                        onChange={(e) => setEndDate(e.target.value)}
                        placeholder="Дата окончания"
                    />
                    <select
                        value={selectedCar}
                        onChange={(e) => setSelectedCar(e.target.value)}
                    >
                        <option value="">Выберите машину</option>
                        {cars.map((car) => (
                            <option key={car._id} value={car._id}>
                                {car.brand} {car.model} ({car.year})
                            </option>
                        ))}
                    </select>
                    {errorMessage && <p className="error-message">{errorMessage}</p>}
                    <button onClick={handleRent}>Арендовать</button>
                </div>
            )}
        </div>
    );
};

export default ParkingDetailPage;