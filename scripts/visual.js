import {retrivePoint, searchAddress} from './searchList.js'

export function addStationMarkers(stationsPromise , map) {
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

export async function loadStationsFromJSON(stringJSON) {
    const response = await fetch(stringJSON);
    const stationsData = await response.json();
    const stations = [];
    stationsData.forEach(station => {
        stations.push(station);
    });
    return stations; // This returns the stations array
}





export function listSuggestions(suggestionsPromise , containerID){
    const container = document.getElementById(containerID);
    container.innerHTML = '<div class="loading">Loading...</div>';

    suggestionsPromise.then(suggestionsJSON => {
        if (!suggestionsJSON || !suggestionsJSON.suggestions) {
            throw new Error('suggestionjson bad');
        }
        const suggestions = suggestionsJSON['suggestions'];
        if(suggestions.length === 0){
            container.innerHTML = '<div>No Results</div>';
            return;
        }
        container.innerHTML = '';
        const listDiv = document.createElement('div');
        listDiv.className = 'suggestions-list';

        suggestions.forEach(suggestion => {
            const suggestionDiv = document.createElement('div');
            suggestionDiv.className = 'suggestion-item';
            let divcontent = '';
            switch (suggestion.feature_type) {
                case 'poi':
                    let cat = 2;
                    while(!suggestion.poi_category[cat] && cat >= 0)
                    {
                        cat--;
                    }

                    divcontent = `${suggestion.name} |
                                  ${suggestion.poi_category[cat]}  <br> ${suggestion.address}`;

                break;

                case 'address':
                    divcontent = `${suggestion.full_address}`;

            }
            suggestionDiv.innerHTML = `<div>${divcontent}</div>`;
            //todo add listner event that will add markers based on chosen location and store those locations
            listDiv.append(suggestionDiv);
        });
        container.appendChild(listDiv);
    })
}

export function chooseSuggestion(id , map){
retrivePoint(id)
    .then(locationJSON => {
        console.log(locationJSON);
        const location = locationJSON['features'];
        location.forEach(location => {
            L.marker([location.geometry.coordinates[1], location.geometry.coordinates[0]])
                .bindPopup(location.properties.name +" "+ location.properties.address).addTo(map);
        })
    })
}