require('dotenv').config();
const express = require('express');
const cors = require('cors'); 
const session = require('express-session')
const db = require('./config/db');
const parkingRoutes = require('./routes/parking');
const authRoutes = require('./routes/auth');
const carsRoutes = require('./routes/cars');
const rentalRoutes = require('./routes/rentals');
const funRoutes = require('./routes/fun');
const passport = require('passport');
require('./config/passport'); 


const app = express();

app.use(express.json());

app.use(cors({
    origin: 'http://localhost:3000',
    methods: 'GET,POST,PUT,DELETE',
}));

// удалить если не нужны 
app.use(session({
    secret: 'secretkey', 
    resave: false,
    saveUninitialized: false,
    cookie: { secure: false }
}));


app.use(passport.initialize());
app.use(passport.session());


app.use('/api/parking', parkingRoutes);
app.use('/api/auth', authRoutes);
app.use('/api/cars', carsRoutes);
app.use('/api/rentals', rentalRoutes);
app.use('/api', funRoutes);


const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});