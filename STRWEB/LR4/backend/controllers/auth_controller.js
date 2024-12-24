const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const User = require('../models/users');

// Регистрация пользователя
exports.register = async (req, res) => {
    try {
        const { username, password, name } = req.body;

        // Проверка, существует ли пользователь
        const existingUser = await User.findOne({ username });
        
        if (existingUser) {
            return res.status(400).json({ message: 'Пользователь уже существует' });
        }

        // Хеширование пароля
        const hashedPassword = await bcrypt.hash(password, 10);
        
        // Создание нового пользователя
        const user = new User({ username: username, password: hashedPassword, name: name });

        await user.save();

        res.status(201).json({ message: 'Пользователь зарегистрирован' });
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

// Логин пользователя
exports.login = async (req, res) => {
    try {
        const { username, password } = req.body;

        // Поиск пользователя
        const user = await User.findOne({ username });
        
        if (!user) {
            return res.status(400).json({ message: 'Пользователь не найден' });
        }

        // Проверка пароля
        const isPasswordValid = await bcrypt.compare(password, user.password);

        if (!isPasswordValid) {
            return res.status(400).json({ message: 'Неверный пароль' });
        }

        // Создание JWT токена
        const token = jwt.sign({ userId: user._id }, process.env.JWT_SECRET, { expiresIn: '1h' });

        // Отправляем данные пользователя вместе с токеном
        res.json({
            token,
            user: {
                username: user.username,
                name: user.name,
            },
        });
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};