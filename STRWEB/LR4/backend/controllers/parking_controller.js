const ParkingSpaces = require('../models/parking_spaces');
// const Reservation = require('../models/Reservation');

exports.getParkingSpaces = async (req, res) => {
    try {
        const parkingSpaces = await ParkingSpaces.find();
        res.send(parkingSpaces);
    } catch (error) {
        res.status(400).send(error.message);
    }
};


exports.getParkingSpace = async (req, res) => {
    try {
        const parkingSpace = await ParkingSpaces.findById(req.params.id);
        res.send(parkingSpace);
    } catch (error) {
        res.status(400).send(error.message);
    }
};