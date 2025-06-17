export async function getCitybikeContext(cityId) {
try{
    const response = await fetch(`https://api.nextbike.net/maps/nextbike-live.json?city=${cityId}`);
    if (!response.ok) {
        throw new Error(`Failed to get city bike context: ${response.status}`);
    }
    const dataJSON = await response.json();
    return dataJSON.countries[0].cities[0];
}
catch(error) {
    console.error(error);
    return null;
}
}

export function convertToGeoJSON(placesArray) {
    return {
        type: "FeatureCollection",
        features: placesArray.map(place => {
            const { lat , lng, number, name , bikes_available_to_rent, bike , bike_numbers} = place;

            return {
                type: "Feature",
                geometry: {
                    type: "Point",
                    coordinates: [parseFloat(lng), parseFloat(lat)]
                },
                properties: {
                    number: number || parseInt(bike_numbers[0]),
                    name: name,
                    bikesAvailable: bikes_available_to_rent,
                    isBike: bike,
                    imageId: bike ? 'bike-image' : 'station-image'
                }
            }
    })}
}


