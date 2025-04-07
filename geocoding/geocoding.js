require('dotenv').config();
const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Places API Text Search Endpoint
app.get('/api/places/search', async (req, res) => {
    try {
        const { query, radius = 5000, location, maxResults = 5 } = req.query;

        if (!query) {
            return res.status(400).json({ error: 'Search query parameter is required' });
        }

        const params = {
            query: query,
            key: process.env.GOOGLE_API_KEY,
            radius: radius
        };

        // Add location bias if provided (format: "lat,lng")
        if (location) {
            params.location = location;
        }

        const response = await axios.get(
            'https://maps.googleapis.com/maps/api/place/textsearch/json',
            { params }
        );

        if (response.data.status !== 'OK') {
            return res.status(400).json({
                error: 'Places search failed',
                status: response.data.status,
                message: response.data.error_message || 'No additional error details'
            });
        }

        const formattedResults = response.data.results.map(place => ({
            name: place.name,
            address: place.formatted_address,
            location: place.geometry?.location,
            place_id: place.place_id,
            types: place.types,
            rating: place.rating,

        }));

        res.json({
            count: formattedResults.length,
            results: formattedResults
        });

    } catch (error) {
        console.error('Places search error:', error);
        res.status(500).json({
            error: 'Internal server error',
            details: error.message
        });
    }
});

// Place Details Endpoint (optional but recommended)
app.get('/api/places/details', async (req, res) => {
    try {
        const { place_id } = req.query;

        if (!place_id) {
            return res.status(400).json({ error: 'Place ID parameter is required' });
        }

        const response = await axios.get(
            'https://maps.googleapis.com/maps/api/place/details/json',
            {
                params: {
                    place_id: place_id,
                    key: process.env.GOOGLE_API_KEY,
                    fields: 'name,formatted_address,geometry,photo,type,rating,user_ratings_total,website,opening_hours'
                }
            }
        );

        if (response.data.status !== 'OK') {
            return res.status(400).json({
                error: 'Place details fetch failed',
                status: response.data.status
            });
        }

        res.json(response.data.result);

    } catch (error) {
        console.error('Place details error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.listen(port, () => {
    console.log(`Places API service running on port ${port}`);
});