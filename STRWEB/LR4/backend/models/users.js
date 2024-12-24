const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true },
    password: { type: String },
    facebookId: { type: String },
    name: { type: String },
});

module.exports = mongoose.model('users', userSchema);