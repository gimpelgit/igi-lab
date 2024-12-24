const Rental = require('../models/rentals');
const ParkingSpace = require('../models/parking_spaces');
const Car = require('../models/cars');

exports.createRental = async (req, res) => {
    try {
        const { parkingSpaceId, endDate, carId } = req.body;
        const userId = req.user.userId;

        
        const existingCarRental = await Rental.findOne({
            carId,
            endDate: {
                $gte: new Date()
            }
        });

        if (existingCarRental) {
            return res.status(400).json({ message: 'Машина уже используется в другой аренде' });
        }

        // Получаем стоимость парковочного места
        const parkingSpace = await ParkingSpace.findById(parkingSpaceId);
        if (!parkingSpace) {
            return res.status(404).json({ message: 'Парковочное место не найдено' });
        }

        // Вычисляем общую стоимость аренды
        const end = new Date(endDate);
        const days = Math.ceil((end - new Date()) / (1000 * 60 * 60 * 24)) + 1;
        const totalPrice = parkingSpace.price * days;


        // Создаем новую аренду
        const rental = new Rental({
            parkingSpaceId,
            userId,
            carId,
            endDate: new Date(endDate),
            totalPrice,
        });

        await rental.save();

        // Обновляем статус парковочного места на "занято"
        await ParkingSpace.findByIdAndUpdate(parkingSpaceId, { isOccupied: true });

        res.status(201).json({ message: 'Аренда успешно создана', rental });
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};


exports.getUserRentals = async (req, res) => {
    try {
        const userId = req.user.userId;
        const rentals = await Rental.find({ userId }).populate('parkingSpaceId');
        res.json(rentals);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};


exports.cancelRental = async (req, res) => {
    try {
        const { id } = req.params;
        const userId = req.user.userId;

        const rental = await Rental.findOneAndUpdate(
            { _id: id, userId },
            { status: 'cancelled' },
            { new: true }
        );

        if (!rental) {
            return res.status(404).json({ message: 'Аренда не найдена' });
        }

        // Обновляем статус парковочного места на "свободно"
        await ParkingSpace.findByIdAndUpdate(rental.parkingSpaceId, { isOccupied: false });

        res.json({ message: 'Аренда отменена', rental });
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};