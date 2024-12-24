const express = require('express');
const router = express.Router();
const authController = require('../controllers/auth_controller');
const passport = require('passport');
const jwt = require('jsonwebtoken');

// Регистрация
router.post('/register', authController.register);

// Логин
router.post('/login', authController.login);

// Facebook аутентификация
router.get('/facebook', passport.authenticate('facebook', { scope: ['email'] }));

router.get('/facebook/callback',
    passport.authenticate('facebook', { failureRedirect: '/login' }),
    (req, res) => {
        const token = jwt.sign({ userId: req.user._id }, process.env.JWT_SECRET, { expiresIn: '1h' });

        res.redirect(`http://localhost:3000?token=${token}&username=${req.user.username}&name=${req.user.name}`);
    }
);

module.exports = router;