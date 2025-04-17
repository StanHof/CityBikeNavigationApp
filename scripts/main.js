import {loadStationsFromJSON, addStationMarkers, listSuggestions, chooseSuggestion} from './visual.js'
import {retrivePoint, searchAddress} from './searchList.js'
let inputTimeout
const fromElement = document.getElementById('fromInput');
const toElement = document.getElementById('toInput');
const wroLoc = {lat: 51.107883, lng: 17.038538};
const wroBbox = '16.85,51.02,17.18,51.2';
const stations = loadStationsFromJSON('stations.json');
//const opoLoc = {lat: 50.671062 , lng: 17.926126};
let suggestions = [];
let map = L.map('map', {
    maxZoom: 20,
    minZoom: 6,
    zoomControl: false}).setView([wroLoc.lat, wroLoc.lng], 13);
L.control.zoom({position: 'bottomright'}).addTo(map);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

//addStationMarkers(stations , map);

fromElement.addEventListener('input', function(event) {
    let queryText = event.target.value.trim();
    if(queryText) {
        clearTimeout(inputTimeout);
        inputTimeout = setTimeout(() => {
            suggestions = searchAddress(queryText, wroLoc, 10 , wroBbox);
            listSuggestions(suggestions, "suggestionListParent");
        }, 300)
    }
});
toElement.addEventListener('input', function(event) {
    let queryText = event.target.value.trim();
    if(queryText) {
        clearTimeout(inputTimeout);
        inputTimeout = setTimeout(() => {
            suggestions = searchAddress(queryText, wroLoc, 10 , wroBbox);
            listSuggestions(suggestions, "suggestionListParent");
        }, 300)
    }
});
chooseSuggestion('dXJuOm1ieHBvaTplOGE1N2MyNy02OGYyLTQyY2EtYjZjMS0yY2RiZGM0NjQ0NDQ' , map)
