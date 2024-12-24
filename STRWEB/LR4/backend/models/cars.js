const mongoose = require('mongoose');

const carSchema = new mongoose.Schema({
    brand: { type: String, required: true },
    model: { type: String, required: true },
    year: { type: Number, required: true, min: 1900, max: new Date().getFullYear() },
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'users', required: true },
});

module.exports = mongoose.model('cars', carSchema);