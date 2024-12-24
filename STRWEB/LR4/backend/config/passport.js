const passport = require('passport');
const FacebookStrategy = require('passport-facebook').Strategy;
const User = require('../models/users');
const axios = require('axios');
const { v4: uuidv4 } = require('uuid');

passport.use(
    new FacebookStrategy(
        {
            clientID: process.env.FACEBOOK_APP_ID,
            clientSecret: process.env.FACEBOOK_APP_SECRET,
            callbackURL: 'http://localhost:5000/api/auth/facebook/callback',
            profileFields: ['id', 'email', 'name'],
        },
        async (accessToken, refreshToken, profile, done) => {
            try {
                let username = generateUniqueUsername();

                while (await User.findOne({ username })) {
                    username = generateUniqueUsername();
                }

                let user = await User.findOne({ facebookId: profile.id });
                if (!user) {
                    user = new User({
                        facebookId: profile.id,
                        name: profile.name.givenName,
                        username: username,
                    });
                    await user.save();
                }

                return done(null, user);
            } catch (error) {
                return done(error);
            }
        }
    )
);

passport.serializeUser((user, done) => {
    done(null, user.id);
});

passport.deserializeUser(async (id, done) => {
    try {
        const user = await User.findById(id);
        done(null, user);
    } catch (error) {
        done(error);
    }
});


function generateUniqueUsername() {
    return `user_${uuidv4().substring(0, 8)}`;
}


module.exports = passport;


