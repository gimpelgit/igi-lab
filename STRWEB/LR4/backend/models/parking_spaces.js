const mongoose = require('mongoose');

const parkingSpaceSchema = new mongoose.Schema({
    number: { type: Number, required: true },
    category: { type: String, enum: ['standard', 'premium'], default: 'standard' },
    isOccupied: { type: Boolean, default: false },
    price: {type: Number, required: true}
});

module.exports = mongoose.model('parking_spaces', parkingSpaceSchema);