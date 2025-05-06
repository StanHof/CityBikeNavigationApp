require('dotenv').config();
const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;
const rateLimit = require ('express-rate-limit');
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100
})

app.use(cors());
app.use(express.json());
app.use('/api/', limiter);

const MAPBOX_ACCESS_TOKEN = process.env.MAPBOX_ACCESS_TOKEN;

// Forward Geocoding API endpoint (search by place name)
app.get('/api/search', async (req, res) => {
    try {
        const { query, proximity, limit = 10 , bounds} = req.query;
        if (!query) {
            return res.status(400).json({ error: 'Query parameter is required' });
        }
        console.log(bounds);
        const response = await axios.get(
            `https://api.mapbox.com/search/searchbox/v1/suggest?q=${query}`,
            {
                params: {
                    access_token: MAPBOX_ACCESS_TOKEN,
                    proximity: proximity, // "longitude,latitude" format
                    limit: limit,
                    session_token: '18ec1019-4371-4321-a0e0-8445e611047d',
                    types: "address,poi",
                    bbox: bounds
                }
            }
        );

        res.json(response.data);
    } catch (error) {
        console.error('Mapbox Suggest API error:', error.message);
        res.status(500).json({ error: 'Failed to fetch location data' });
    }
});

app.get('/api/ret' , async (req, res) => {
    try {
        const {id} = req.query;
        const response = await axios.get(`https://api.mapbox.com/search/searchbox/v1/retrieve/${encodeURIComponent(id)}`
            ,{params: {
                    session_token: '18ec1019-4371-4321-a0e0-8445e611047d',
                    access_token: MAPBOX_ACCESS_TOKEN
                }
            })
        res.json(response.data);
    } catch (error) {
        console.error('Mapbox Retrive API error:', error.message);
        res.status(500).json({ error: 'Failed to retrive place '});
    }
})
app.listen(PORT, () => {
    console.log(`Listening on port ${PORT}`);
})