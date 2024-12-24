import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Cars.css';

const Cars = () => {
    const [cars, setCars] = useState([]);
    const [newBrand, setNewBrand] = useState('');
    const [newModel, setNewModel] = useState('');
    const [newYear, setNewYear] = useState('');
    const [editBrand, setEditBrand] = useState('');
    const [editModel, setEditModel] = useState('');
    const [editYear, setEditYear] = useState('');
    const [editingCarId, setEditingCarId] = useState(null);
    const [addErrors, setAddErrors] = useState({});
    const [editErrors, setEditErrors] = useState({});
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
        } else {
            fetchCars();
        }
    }, [navigate]);

    const fetchCars = async () => {
        try {
            const response = await axios.get('/api/cars');
            setCars(response.data);
        } catch (error) {
            console.error('Ошибка при загрузке машин:', error);
        }
    };

    const validateForm = (brand, model, year) => {
        const errors = {};
        if (!brand) errors.brand = 'Марка не может быть пустой';
        if (!model) errors.model = 'Модель не может быть пустой';
        if (!year) {
            errors.year = 'Год не может быть пустым';
        } else if (isNaN(year) || !Number.isInteger(Number(year))) {
            errors.year = 'Год должен быть целым числом';
        } else if (year < 1900 || year > new Date().getFullYear()) {
            errors.year = 'Год должен быть в диапазоне от 1900 до текущего года';
        }
        return errors;
    };

    const handleCreateCar = async () => {
        const validationErrors = validateForm(newBrand, newModel, newYear);
        if (Object.keys(validationErrors).length > 0) {
            setAddErrors(validationErrors);
            return;
        }

        try {
            const response = await axios.post('/api/cars', {
                brand: newBrand,
                model: newModel,
                year: Number(newYear),
            });
            setCars([...cars, response.data]);
            setNewBrand('');
            setNewModel('');
            setNewYear('');
            setAddErrors({});
        } catch (error) {
            console.error('Ошибка при создании машины:', error);
        }
    };

    const handleEditCar = (car) => {
        setEditingCarId(car._id); 
        setEditBrand(car.brand); 
        setEditModel(car.model);
        setEditYear(car.year.toString());
        setEditErrors({}); 
    };

    const handleUpdateCar = async (id) => {
        const validationErrors = validateForm(editBrand, editModel, editYear);
        if (Object.keys(validationErrors).length > 0) {
            setEditErrors(validationErrors);
            return;
        }

        try {
            const response = await axios.put(`/api/cars/${id}`, {
                brand: editBrand,
                model: editModel,
                year: Number(editYear),
            });
            setCars(cars.map(car => car._id === id ? response.data : car));
            setEditingCarId(null); // Завершаем режим редактирования
            setEditBrand('');
            setEditModel('');
            setEditYear('');
            setEditErrors({});
        } catch (error) {
            console.error('Ошибка при обновлении машины:', error);
        }
    };

    const handleDeleteCar = async (id) => {
        try {
            await axios.delete(`/api/cars/${id}`);
            setCars(cars.filter(car => car._id !== id));
        } catch (error) {
            console.error('Ошибка при удалении машины:', error);
        }
    };

    return (
        <div className="container">
            <h1>Мои машины</h1>
            <div className="car-form">
                <input
                    type="text"
                    placeholder="Марка"
                    value={newBrand}
                    onChange={(e) => setNewBrand(e.target.value)}
                />
                {addErrors.brand && <span className="error">{addErrors.brand}</span>}
                <input
                    type="text"
                    placeholder="Модель"
                    value={newModel}
                    onChange={(e) => setNewModel(e.target.value)}
                />
                {addErrors.model && <span className="error">{addErrors.model}</span>}
                <input
                    type="number"
                    placeholder="Год"
                    value={newYear}
                    onChange={(e) => setNewYear(e.target.value)}
                />
                {addErrors.year && <span className="error">{addErrors.year}</span>}
                <button onClick={handleCreateCar}>Добавить машину</button>
            </div>
            <div className="car-list">
                {cars.map(car => (
                    <div key={car._id} className="car-item">
                        {editingCarId === car._id ? (
                            // Форма редактирования
                            <div className="edit-form">
                                <input
                                    type="text"
                                    value={editBrand}
                                    onChange={(e) => setEditBrand(e.target.value)}
                                />
                                {editErrors.brand && <span className="error">{editErrors.brand}</span>}
                                <input
                                    type="text"
                                    value={editModel}
                                    onChange={(e) => setEditModel(e.target.value)}
                                />
                                {editErrors.model && <span className="error">{editErrors.model}</span>}
                                <input
                                    type="number"
                                    value={editYear}
                                    onChange={(e) => setEditYear(e.target.value)}
                                />
                                {editErrors.year && <span className="error">{editErrors.year}</span>}
                                <button onClick={() => handleUpdateCar(car._id)}>Сохранить</button>
                            </div>
                        ) : (
                            // Информация о машине
                            <>
                                <h3>{car.brand} {car.model}</h3>
                                <p>Год: {car.year}</p>
                                <button onClick={() => handleEditCar(car)}>Редактировать</button>
                                <button onClick={() => handleDeleteCar(car._id)}>Удалить</button>
                            </>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Cars;