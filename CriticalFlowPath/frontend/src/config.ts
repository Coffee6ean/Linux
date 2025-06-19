const config = {
    // config.js
    API_BASE_URL: process.env.NODE_ENV === "development"
        ? "http://localhost:5000/api"
        : "/api",
    appVersion: '1.0.0',
    theme: 'light',
    featureFlags: {
        newDashboard: true,
        analyticsEnabled: false
    }
};

export default config;