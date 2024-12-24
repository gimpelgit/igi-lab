const Car = require('../models/cars');
const Rental = require('../models/rentals');

exports.getCars = async (req, res) => {
    try {
        const cars = await Car.find({ userId: req.user.userId });
        res.send(cars);
    } catch (error) {
        res.status(400).send(error.message);
    }
};

exports.getAvailableCars = async (req, res) => {
    try {
        const userId = req.user.userId;
        const cars = await Car.find({ userId });

        const activeRentals = await Rental.find({ userId, status: 'active' });
        const availableCars = cars.filter((car) => {
            return !activeRentals.some((rental) => rental.carId.toString() === car._id.toString());
        });

        res.send(availableCars);
    } catch (error) {
        res.status(500).send(error.message);
    }
};


exports.createCar = async (req, res) => {
    try {
        const { brand, model, year } = req.body;
        const car = new Car({ brand, model, year, userId: req.user.userId });
        await car.save();
        res.status(201).send(car);
    } catch (error) {
        res.status(400).send(error.message);
    }
};


exports.updateCar = async (req, res) => {
    try {
        const { id } = req.params;
        const { brand, model, year } = req.body;
        const car = await Car.findOneAndUpdate(
            { _id: id, userId: req.user.userId },
            { brand, model, year },
            { new: true }
        );
        if (!car) {
            return res.status(404).send('Машина не найдена');
        }
        res.send(car);
    } catch (error) {
        res.status(400).send(error.message);
    }
};


exports.deleteCar = async (req, res) => {
    try {
        const { id } = req.params;
        const car = await Car.findOneAndDelete({ _id: id, userId: req.user.userId });
        if (!car) {
            return res.status(404).send('Машина не найдена');
        }
        res.send({ message: 'Машина удалена' });
    } catch (error) {
        res.status(400).send(error.message);
    }
};