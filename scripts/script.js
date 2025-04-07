
const wroLAT = 51.107883;
const wroLNG = 17.038538;
let stations = [];

function loadStationsFromJSON(stringJSON) {
    fetch(stringJSON)
        .then(res => res.json())
        .then(stations => {
            stations.forEach(station => {
                L.marker([station.latitude, station.longitude])
                    .bindPopup(station.Name + '<br>' + station.ID)
                    .addTo(map);
                stations.push(station);
            });
        });
}

async function geocodeAddress(address) {
    try {
        const response = await fetch(`http://localhost:3001/api/geocode?address=${encodeURIComponent(address)}`);
        const data = await response.json();

        if (response.ok) {
            console.log('Geocoding results:', data.results);
            return data.results;
        } else {
            throw new Error(data.error || 'Geocoding failed');
        }
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

let map = L.map('map', {
    maxZoom: 20,
    minZoom: 6,
    zoomControl: false}).setView([wroLAT, wroLNG], 13);

L.control.zoom({position: 'bottomright'}).addTo(map);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
loadStationsFromJSON('stations.json');

