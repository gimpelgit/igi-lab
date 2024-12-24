const mongoose = require('mongoose');

const rentalSchema = new mongoose.Schema({
    parkingSpaceId: { type: mongoose.Schema.Types.ObjectId, ref: 'parking_spaces', required: true },
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'users', required: true },
    carId: { type: mongoose.Schema.Types.ObjectId, ref: 'cars', required: true },
    endDate: { type: Date, required: true },
    totalPrice: { type: Number, required: true },
    status: { type: String, enum: ['active', 'completed', 'cancelled'], default: 'active' },
});

module.exports = mongoose.model('rentals', rentalSchema);