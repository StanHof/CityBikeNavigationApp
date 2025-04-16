
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

export async function fetchPlaces(address, location=null, radius=70000) {
try{
    let url = `http://localhost:3001/api/places/search?query=${encodeURI(address)}`;
    if (location) {
        url += `&location=${location.lng},${location.lat}&radius=${radius}`;
    }
    console.log(url);
    const response = await fetch(url);
    const data = await response.json();

    if(data.status === 'OK') {
        return data;
    }
    else{
        throw new Error(data.error || "Failed to fetch places.");
    }
}
catch(error) {
    console.error("FetchPlaces:",error);
    throw error;
}
}


export async function searchAddress(query , location={lat: 51.107883, lng: 17.038538}, limit) {
    const locString = `${location.lng},${location.lat}`
    try {

        if (!query || typeof query !== 'string') {
            throw new Error('Invalid search query');
        }
        const url = `http://localhost:3001/api/search?query=${encodeURIComponent(query)}&limit=${limit}&proximity=${encodeURIComponent(locString)}`;
        console.log(url);

        const response = await fetch(
            `http://localhost:3001/api/search?query=${encodeURIComponent(query)}&limit=${limit}&proximity=${encodeURIComponent(locString)}`,
        );

        if (!response.ok) {
            throw new Error(`API request failed with status ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Search error:', error);

        throw error;
    }
}
export function listSuggestions(suggestionsPromise , containerID){
    const container = document.getElementById(containerID);
    container.innerHTML = '<div class="loading">Loading...</div>';

    suggestionsPromise.then(suggestionsJSON => {
        const suggestions = suggestionsJSON['suggestions'];
        console.log(suggestions);
        container.innerHTML = '';
        const listDiv = document.createElement('div');
        listDiv.className = 'suggestions-list';

        suggestions.forEach((suggestion) => {
            const suggestionDiv = document.createElement('div');
            suggestionDiv.className = 'suggestion-item';

            switch (suggestion.feature_type) {
                case 'poi':
                    suggestionDiv.innerHTML = `<div>${suggestion.name} |
                                                ${suggestion.poi_category[1]}  <br> ${suggestion.address}</div>`;
                break;
                case 'address':
                    suggestionDiv.innerHTML = `<div>${suggestion.full_address}</div>`;
            }


            listDiv.append(suggestionDiv);
        });
        container.appendChild(listDiv);
    })
}