

export async function searchAddress(query , location={lat: 51.107883, lng: 17.038538}, limit , bbox) {
    const locString = `${location.lng},${location.lat}`
    let url = `http://localhost:3001/api/search?query=${encodeURIComponent(query)}&limit=${limit}&proximity=${encodeURIComponent(locString)}`;
    if(bbox) {
        url += `&bounds=${encodeURIComponent(bbox)}`;
    }
    try {
        if (!query || typeof query !== 'string') {
            throw new Error('Invalid search query');
        }

        console.log(url);

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`API request failed with status ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Search error:', error);

        throw error;
    }
}
export async function retrivePoint(id){
    let url = `http://localhost:3001/api/ret?id=${encodeURIComponent(id)}`;
    console.log(url);
    try{
        if(!id || typeof id !== 'string'){
            throw new Error('Invalid id');
        }

        const response = await fetch(url);
        return await response.json();
    } catch (error){
        console.error('Retrive Point Error:', error);
        throw error;
    }
}