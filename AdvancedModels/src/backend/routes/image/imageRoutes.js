const express = require('express');
const router = new express.Router();
const ExpressError = require('../backend/expressError');

router.get('/', (req, res, next) => {
    res.send('App is working');
});

module.exports = router;