import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = ({ isAuthenticated = false, username, name, onLogout  }) => {
    return (
        <nav>
            <Link to="/parking">Парковочные места</Link>
            {isAuthenticated ? (
                <>
                    <Link to="/cars">Машины</Link>
                    <Link to="/fun">Веселые штуки</Link>
                    <span style={{ color: 'white', margin: '0 20px' }}>Привет, {name}!</span>
                    <a href="/" onClick={onLogout} className="logout-link">Выйти</a>
                </>
            ) : (
                <>
                    <Link to="/login">Вход</Link>
                    <Link to="/register">Регистрация</Link>
                </>
            )}
        </nav>
    );
};

export default Navbar;