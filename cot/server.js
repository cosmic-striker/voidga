require('dotenv').config();
const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const authRoutes     = require('./routes/auth');
const userRoutes     = require('./routes/user');
const internalRoutes = require('./routes/internal');
const { authorize, token } = require('./utils/oauthProvider');

const app = express();
app.use(session({ secret: process.env.APP_SECRET, resave: false, saveUninitialized: true }));
app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs');

// Mount vulnerable app routes
app.use('/', authRoutes);
app.use('/', userRoutes);
app.use('/', internalRoutes);

// Simulated OAuth2 provider
app.get('/oauth/authorize', authorize);
app.post('/oauth/token', token);

app.listen(3000, ()=> console.log('Server running on http://localhost:3000'));

