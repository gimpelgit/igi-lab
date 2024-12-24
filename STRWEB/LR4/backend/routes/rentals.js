const express = require('express');
const router = express.Router();
const rentalController = require('../controllers/rental_controller');
const authMiddleware = require('../middleware/authMiddleware');

router.use(authMiddleware);

router.post('/', rentalController.createRental);
router.get('/', rentalController.getUserRentals);
router.put('/:id/cancel', rentalController.cancelRental);

module.exports = router;