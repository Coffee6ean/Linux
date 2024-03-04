/* Hasing and JWT's with Node */
const express = require("express");
const morgan = require("morgan");
const ExpressError = require("./utils/expressError");

const app = express();

/* MIDDLEWARE */
app.use(express.json());
app.use(morgan("dev"));

// 404 Handler
app.use(function(req, res, next) {
    const err = new ExpressError("Not found", 404);
    return next(err);
});

// Generic error handler
app.use(function(err, req, res, next) {
    // the default status is 500: Internal Server Error
    let status = err.status || 500;

    // set the status and alert teh user
    return res.status(status).json({
        error: {
            message: err.message || err.msg,
            status: status
        }
    });
});

module.exports = app;
