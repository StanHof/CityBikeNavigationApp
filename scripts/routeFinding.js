export class pathFindingManager{
    constructor(){}

    async fetchPath(origGeoJSON , destGeoJSON){
        const baseUrl = "http://127.0.0.1:5000/full_navigate"
        const params = new URLSearchParams( {
            start_lat: origGeoJSON.geometry.coordinates[1],
            start_lng: origGeoJSON.geometry.coordinates[0],
            end_lat: destGeoJSON.geometry.coordinates[1],
            end_lng: destGeoJSON.geometry.coordinates[0],
        })
        const url = `${baseUrl}?${params.toString()}`;
        console.log(url);
        try {
            const response = await fetch(url);
            if (!response.ok) {
                const json = await response.json();
                throw new Error(json.message);
            }
            return await response.json();
        }
        catch (e) {
            console.error(e);
            return null;
        }
        }

}