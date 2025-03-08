module.exports = {
    server: 'localhost\\SQLEXPRESS', // Localhost or Server address
    database: 'DemlandData',
    options: {
        encrypt: false, // Use encryption for Azure or set to false for local
        trustServerCertificate: true // For local development, can be set to true
    }
};
