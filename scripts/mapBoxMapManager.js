import {convertToGeoJSON, getCitybikeContext} from "./utilis.js";

export class MapBoxMapManager {
    constructor(map, city) {
        this._map = map;
        this._city = city;
        this._cityBikeGEOJSONarray = null;
        this._intializeBikeData()
        this._bikeMarkers = new Map();


    }
    async _intializeBikeData() {

        const citybikepromise = await getCitybikeContext(this._city.nextBikeId)
        this._cityBikeGEOJSONarray = convertToGeoJSON(citybikepromise.places);
        console.log(this._cityBikeGEOJSONarray)
        this._addBikeMarkers()
    }

    _addBikeMarkers(){
        console.log(this._cityBikeGEOJSONarray);
        this._cityBikeGEOJSONarray.features.forEach(feature => {
            const el = document.createElement("div");
            const popup = new mapboxgl.Popup({offset: 25})
            el.className = "marker";
            if(feature.properties.isBike){
                el.classList.add('bike')
                popup.setText(
                    `Rower Wolnostojący: ${feature.properties.name}`
                )
            }
            else {
                el.classList.add('station')
                popup.setHTML(
                    `Stacja: ${feature.properties.number} ${feature.properties.name} <br>
                    Dostępne Rowery: ${feature.properties.bikesAvailable}`
                )
            }
            const marker = new mapboxgl.Marker(el ,{anchor: 'bottom'}).setLngLat(feature.geometry.coordinates)
            marker.setPopup(popup)
            marker.addTo(this._map)
            this._bikeMarkers.set(feature.properties.number  , marker)
        })

    }



}