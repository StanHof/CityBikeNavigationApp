

export class MapManager {
    constructor(map , listContainer) {
        this.map = map;
        this.stationMarkers = [];
        this.placesMarkers = [];
        this.listContainer = listContainer;
    }

    addStationMarkers(stationsPromise) {
        stationsPromise.then(stations =>{
            stations.forEach(station => {
                L.marker([station.latitude, station.longitude])
                    .bindPopup(station.Name + '<br>' + station.ID)
                    .addTo(map);
            })

        })
            .catch(error => {
                console.log("Failed to load markers",error);
            })
    }

    async loadStationsFromJSON(stringJSON) {
        const response = await fetch(stringJSON);
        const stationsData = await response.json();
        const stations = [];
        stationsData.forEach(station => {
            stations.push(station);
        });
        return stations;
    }


}