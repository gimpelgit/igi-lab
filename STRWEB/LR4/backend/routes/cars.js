const express = require('express');
const router = express.Router();
const carsController = require('../controllers/cars_controller');
const authMiddleware = require('../middleware/authMiddleware');

router.use(authMiddleware);

router.get('/', carsController.getCars);
router.post('/', carsController.createCar);
router.get('/available', carsController.getAvailableCars);
router.put('/:id', carsController.updateCar);
router.delete('/:id', carsController.deleteCar);

module.exports = router;