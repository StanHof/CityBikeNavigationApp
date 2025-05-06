
import {SearchListManager} from './searchListManager.js'
import {cityContext} from "./cityContext.js";
import {MapManager} from "./mapManager.js";
import {getCitybikeContext} from "./utilis.js";

const fromElement = document.getElementById('fromInput');
const toElement = document.getElementById('toInput');
const listElement = document.getElementById("suggestionListParent");
const wroLoc = [ 51.107883, 17.038538]
const wroBbox = [[16.85 , 51.02],[17.18 , 51.2]];
const city = new cityContext("Wrocław" , wroLoc , wroBbox , 148 );
let map = L.map('map', {
    maxZoom: 20,
    minZoom: 6,
    zoomControl: false}).setView(wroLoc, 13);
L.control.zoom({position: 'bottomright'}).addTo(map);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);


let mapVisualManager = new MapManager(map, city);

let searchListManager = new SearchListManager(mapVisualManager , city ,listElement , toElement , fromElement );
