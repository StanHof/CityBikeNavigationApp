require('dotenv').config();
const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Your Mapbox API access token (store in .env file)
const MAPBOX_ACCESS_TOKEN = process.env.MAPBOX_ACCESS_TOKEN;

// Forward Geocoding API endpoint (search by place name)
app.get('/api/search', async (req, res) => {
    try {
        const { query, proximity, limit = 10 } = req.query;

        if (!query) {
            return res.status(400).json({ error: 'Query parameter is required' });
        }
        console.log(proximity);
        const response = await axios.get(
            `https://api.mapbox.com/search/searchbox/v1/suggest?q=${query}`,
            {
                params: {
                    access_token: MAPBOX_ACCESS_TOKEN,
                    proximity: proximity, // "longitude,latitude" format
                    limit: limit,
                    session_token: '18ec1019-4371-4321-a0e0-8445e611047d',
                    types: "address,poi"
                }
            }
        );

        res.json(response.data);
    } catch (error) {
        console.error('Mapbox API error:', error.message);
        res.status(500).json({ error: 'Failed to fetch location data' });
    }
});
app.listen(PORT, () => {
    console.log(`Listening on port ${PORT}`);
})