export class pathFindingManager{
    constructor(){}

    async fetchPath(origGeoJSON , destGeoJSON){
        const baseUrl = "http://127.0.0.1:5000/navigate"
        const params = new URLSearchParams( {
            start_lat: origGeoJSON.geometry.coordinates[0],
            start_lng: origGeoJSON.geometry.coordinates[1],
            end_lat: destGeoJSON.geometry.coordinates[0],
            end_lng: destGeoJSON.geometry.coordinates[1],
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

    findClosestStations(stations , location , n , bboxSize){
    //@todo find n closest stations to a point
    }
    findPath(){
        //todo find walking path between start/end and bike station , find bike path between stations to do this for N combinations of bike stations and choose the shortest one
    }
}