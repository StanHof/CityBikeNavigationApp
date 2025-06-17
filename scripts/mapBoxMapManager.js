import {convertToGeoJSON, getCitybikeContext} from "./utilis.js";

export class MapBoxMapManager {
    constructor(map, city) {
        this._map = map;
        this._city = city;
        this._cityBikeGEOJSONarray = null;
        this._intializeBikeData()
        this._bikeMarkers = new Map();
        this._markers = new Map();

    }
    async _intializeBikeData() {

        const citybikepromise = await getCitybikeContext(this._city.nextBikeId)
        this._cityBikeGEOJSONarray = convertToGeoJSON(citybikepromise.places);
        console.log(this._cityBikeGEOJSONarray)
        this._addBikeMarkers()
    }

    /*_addBikeMarkers(){
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
        })*/
    _addBikeMarkers() {
        this._map.on('load', () =>{
            this._map.loadImage('../styles/BikeMarker.png' , (error , image) => {
                if (error) throw error;
                this._map.addImage('bike-icon' , image);
            })
            this._map.addSource('stations' , {
                type: 'geojson',
                data: this._cityBikeGEOJSONarray
            })
            this._map.addLayer({
                id: 'bike-stations',
                type: 'circle',
                source: 'stations',
                paint: {
                    'circle-radius': [
                        'interpolate', ['linear'], ['zoom'],
                        10, 5,  // 5px at zoom 10
                        24, 25  // 10px at zoom 16
                    ],
                    'circle-color': [
                        'case',
                        ['==', ['get', 'isBike'] , true] ,'#92023f',
                        ['==', ['get', 'bikesAvailable'], 0], '#4e4e4e',

                        '#ff66a3'

                    ],
                    'circle-stroke-color': '#92023f',
                    'circle-stroke-width': 1.5,

                }
            });
            this._map.addLayer({
                id: 'bike-count',
                type: 'symbol',
                source: 'stations',
                layout: {
                    'icon-image': 'bike-icon', // Using built-in Maki icon as background
                    'icon-size': [
                        'interpolate', ['linear'], ['zoom'],
                        14, 0.4,
                        16, 0.4
                    ],
                    'text-field': ['get', 'bikesAvailable'],
                    'text-size': 20,
                    'text-offset': [0.98, -0.13],
                    'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
                    'text-allow-overlap': true,
                    'visibility': 'none' // Initially hidden
                },
                paint: {
                    'icon-opacity': [
                        'interpolate', ['linear'], ['zoom'],
                        13, 0,
                        14, 1
                    ],
                    'text-opacity': [
                        'interpolate', ['linear'], ['zoom'],
                        13, 0,
                        14, 1
                    ],

                    'text-color': '#000000',
                    'text-halo-color': 'rgb(147,2,63)',
                    'text-halo-width': 1
                }
            });
        })
        this._map.on('click', 'bike-stations', (e) => {
            // Get the clicked feature's properties
            const properties = e.features[0].properties;
            const coordinates = e.features[0].geometry.coordinates.slice();

            // Create HTML content for the popup
            const popupContent = `
                <div>
                    <p>${properties.name}</p>
                    <p>Bikes available: ${properties.bikesAvailable}</p>
                    <p>Station number: ${properties.number}</p>
                </div>
            `;


            // Create and show the popup
            new mapboxgl.Popup({className: 'mapboxgl-Popup-content'})
                .setLngLat(coordinates)
                .setHTML(popupContent)
                .addTo(this._map);
        });
        this._map.on('zoom', () => {
            const zoom = this._map.getZoom();
            if (zoom > 14) {
                this._map.setLayoutProperty('bike-stations', 'visibility' , 'none')
                this._map.setLayoutProperty('bike-count', 'visibility', 'visible');
            } else {
                this._map.setLayoutProperty('bike-stations', 'visibility' , 'visible')
                this._map.setLayoutProperty('bike-count', 'visibility', 'none');
            }
        });

    }

    addMarker(geoJSON , markerid){
        const el = document.createElement("div");
        const popup = new mapboxgl.Popup({offset: 25})
        el.className = "marker"
        el.classList.add(markerid);
        const marker = new mapboxgl.Marker(el , {anchor: 'bottom'}).setLngLat(geoJSON.geometry.coordinates)
        marker.addTo(this._map);
        this._markers.set(markerid, marker)
    }
    removeMarker(markerid){
        if(this._markers.has(markerid)) {
            this._markers.get(markerid).remove();
            this._markers.delete(markerid);
        }
    }
    displayPath(path) {
        this._map.addSource('path' , {
            type: 'geojson',
            data: path,
        })

        this._map.addLayer({
            'id': 'route',
            'type': 'line',
            'source': 'path',
            'layout': {
                'line-join': 'round',
                'line-cap': 'round'
            },
            'paint': {
                'line-color': '#fd65a2',
                'line-width': 5,
                'line-opacity': 1
            }
        });
    }
}