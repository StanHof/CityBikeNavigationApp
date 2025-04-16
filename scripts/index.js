import {loadStationsFromJSON, addStationMarkers, searchAddress, listSuggestions} from './script.js'


const wroLoc = {lat: 51.107883, lng: 17.038538};
//const opoLoc = {lat: 50.671062 , lng: 17.926126};
let map = L.map('map', {
    maxZoom: 20,
    minZoom: 6,
    zoomControl: false}).setView([wroLoc.lat, wroLoc.lng], 13);

L.control.zoom({position: 'bottomright'}).addTo(map);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

const stations = loadStationsFromJSON('stations.json');
addStationMarkers(stations , map);
let suggestionsList = searchAddress("pizza", wroLoc, 10);
listSuggestions(suggestionsList , "suggestionListParent");
