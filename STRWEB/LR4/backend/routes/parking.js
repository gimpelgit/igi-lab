const express = require('express');
const router = express.Router();
const parkingController = require('../controllers/parking_controller');

router.get('/parking-spaces', parkingController.getParkingSpaces);
router.get('/parking-spaces/:id', parkingController.getParkingSpace);
// router.post('/reservations', parkingController.createReservation);

module.exports = router;