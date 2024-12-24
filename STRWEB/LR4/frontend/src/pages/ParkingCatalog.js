import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './ParkingCatalog.css';

const ParkingCatalog = () => {
    const [parkingSpaces, setParkingSpaces] = useState([]);
    const [filteredSpaces, setFilteredSpaces] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [sortBy, setSortBy] = useState('number');

    useEffect(() => {
        // Загружаем список парковочных мест с сервера
        axios.get('/api/parking/parking-spaces')
            .then((response) => {
                setParkingSpaces(response.data);
                setFilteredSpaces(response.data);
            })
            .catch((error) => {
                console.error('Ошибка при загрузке данных:', error);
            });
    }, []);

    useEffect(() => {
        handleFilter();
    }, [parkingSpaces, searchTerm, sortBy]);

    const handleFilter = () => {
        let filtered = [...parkingSpaces]; 

        if (searchTerm) {
            filtered = filtered.filter(space => 
                space.number.toString().includes(searchTerm) ||
                space.price.toString().includes(searchTerm)
            );
        }

        if (sortBy === 'number') {
            filtered.sort((a, b) => a.number - b.number);
        } else if (sortBy === 'price') {
            filtered.sort((a, b) => a.price - b.price);
        }

        setFilteredSpaces(filtered);
    }
    

    return (
        <div className="container">
            <h1>Парковочные места</h1>
            <div className="filter-section">
                <input
                    type="text"
                    placeholder="Поиск по номеру или цене"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="search-input"
                />
                <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value)}
                    className="sort-select"
                >
                    <option value="number">Сортировать по номеру</option>
                    <option value="price">Сортировать по цене</option>
                </select>
            </div>
            <div className="parking-list">
                {filteredSpaces.map((space) => (
                    <div 
                        key={space._id} 
                        className={`parking-item ${space.category === 'premium' ? 'premium' : ''}`}
                    >
                        <h3>Парковочное место #{space.number}</h3>
                        <p>Цена: {space.price} руб./день</p>
                        <p>Статус: <span className={`status ${space.isOccupied ? 'occupied' : 'free'}`}>
                            {space.isOccupied ? 'Занято' : 'Свободно'}
                        </span></p>
                        <Link to={`/parking/${space._id}`}>Подробнее</Link>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ParkingCatalog;