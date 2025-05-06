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