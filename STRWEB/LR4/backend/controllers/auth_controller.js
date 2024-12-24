const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const User = require('../models/users');

exports.register = async (req, res) => {
    try {
        const { username, password, name } = req.body;

        const existingUser = await User.findOne({ username });
        
        if (existingUser) {
            return res.status(400).json({ message: 'Пользователь уже существует' });
        }

        const hashedPassword = await bcrypt.hash(password, 10);
        const user = new User({ username: username, password: hashedPassword, name: name });

        await user.save();

        res.status(201).json({ message: 'Пользователь зарегистрирован' });
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

exports.login = async (req, res) => {
    try {
        const { username, password } = req.body;

        const user = await User.findOne({ username });
        
        if (!user) {
            return res.status(400).json({ message: 'Пользователь не найден' });
        }

        const isPasswordValid = await bcrypt.compare(password, user.password);

        if (!isPasswordValid) {
            return res.status(400).json({ message: 'Неверный пароль' });
        }

        const token = jwt.sign({ userId: user._id }, process.env.JWT_SECRET, { expiresIn: '1h' });

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