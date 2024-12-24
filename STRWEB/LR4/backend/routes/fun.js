const express = require('express');
const router = express.Router();
const axios = require('axios');
const authMiddleware = require('../middleware/authMiddleware');

router.use(authMiddleware);

router.get('/ip', async (req, res) => {
    try {
        const response = await axios.get('https://api.ipify.org?format=json');
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Ошибка при получении IP-адреса' });
    }
});

router.get('/random-dog', async (req, res) => {
    try {
        const response = await axios.get('https://dog.ceo/api/breeds/image/random');
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Ошибка при получении IP-адреса' });
    }
});

module.exports = router;