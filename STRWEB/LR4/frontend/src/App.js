import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import ParkingCatalog from './pages/ParkingCatalog';
import ParkingDetailPage from './pages/ParkingDetailPage';
import Cars from './pages/Cars';
import Login from './components/Login';
import Register from './components/Register';
import FunPage from './pages/FunPage';


function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [username, setUsername] = useState('');
    const [name, setName] = useState('');

    useEffect(() => {
        const token = localStorage.getItem('token');
        const storedUsername = localStorage.getItem('username');
        const storedName = localStorage.getItem('name');

        if (token) {
            setIsAuthenticated(true);
            setUsername(storedUsername);
            setName(storedName);
        }
    }, []);

    const handleLogout = () => {
        // Удаляем токен и данные пользователя из localStorage
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        localStorage.removeItem('name');

        // Обновляем состояние
        setIsAuthenticated(false);
        setUsername('');
        setName('');
    };


    return (
        <Router>
            <Navbar 
                isAuthenticated={isAuthenticated}
                username={username}
                name={name}
                onLogout={handleLogout}
            />
            <Routes>
                <Route path="/parking" element={<ParkingCatalog />} />
                <Route path="/parking/:id" element={<ParkingDetailPage isAuthenticated={isAuthenticated} />} />
                <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} setNameApp={setName} setUsernameApp={setUsername}/>} />
                <Route path="/register" element={<Register />} />
                <Route path="/cars" element={<Cars />} />
                <Route path="/fun" element={<FunPage />} />
            </Routes>
        </Router>
    );
}

export default App;