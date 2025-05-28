
import {SearchListManager} from './searchListManager.js'
import {cityContext} from "./cityContext.js";
import {MapBoxMapManager} from "./mapBoxMapManager.js";

mapboxgl.accessToken = "pk.eyJ1Ijoic3RhaHUiLCJhIjoiY205YmRqY21oMGVodjJrc2pqOWN1M3pwbiJ9.xmIz28dJw9jhXGEMS27Nug"

const fromElement = document.getElementById('fromInput');
const toElement = document.getElementById('toInput');
const listElement = document.getElementById("suggestionListParent");
const wroLoc = [ 51.107883, 17.038538]
const wroBbox = [[16.85 , 51.02],[17.18 , 51.2]];
const city = new cityContext("Wrocław" , wroLoc , wroBbox , 148 );

const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v12',
    center: [city.latitude, city.longitude],
    zoom: 12
})

let mapVisualManager = new MapBoxMapManager(map ,city);

let searchListManager = new SearchListManager(mapVisualManager , city ,listElement , toElement , fromElement );
