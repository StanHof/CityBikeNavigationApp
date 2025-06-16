
import {SearchListManager} from './searchListManager.js'
import {cityContext} from "./cityContext.js";
import {MapBoxMapManager} from "./mapBoxMapManager.js";
import {pathFindingManager} from "./routeFinding.js";

mapboxgl.accessToken = "pk.eyJ1Ijoic3RhaHUiLCJhIjoiY205YmRqY21oMGVodjJrc2pqOWN1M3pwbiJ9.xmIz28dJw9jhXGEMS27Nug"

const fromElement = document.getElementById('fromInput');
const toElement = document.getElementById('toInput');
const listElement = document.getElementById("listParent");
const wroLoc = [ 51.107883, 17.038538]
const wroBbox = [[16.85 , 51.02],[17.18 , 51.2]];
const city = new cityContext("Wrocław" , wroLoc , wroBbox , 148 );

const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v11',
    center: [city.latitude, city.longitude],
    zoom: 12
})

let mapVisualManager = new MapBoxMapManager(map ,city);

let searchListManager = new SearchListManager(mapVisualManager , city ,listElement , toElement , fromElement );
let pathmanager = new pathFindingManager()
let sepa =  {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "coordinates": [
            17.052404990026247,
            51.11801761202622
        ],
        "type": "Point"
    }
}
let piekna = {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "coordinates": [
            17.05135677397479,
            51.08435837981736
        ],
        "type": "Point"
    }}
let path = pathmanager.fetchPath(piekna , sepa).then((pathJSON) => mapVisualManager.displayPath(pathJSON));
