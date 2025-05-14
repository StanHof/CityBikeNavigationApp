export class cityContext {
    get nextbikeId() {
        return this._nextbikeId;
    }
    constructor(cityName , coordinates, bbox, nextbikeId){
        /**
         * @param {string} cityName - name
         * @param {[number , number]} - coordinates - [longitude , latitude]
         * @param {[[number , number],[number, number]]} - bbox [[min lat , min lng] , [max lat, max lat]]
         * */
        this._cityName = cityName;
        this._coordinates = coordinates;
        this._bbox = bbox;
        this._nextbikeId = nextbikeId;

    }
    get center(){
        return this._coordinates;
    }
    get centerString(){
        return `${this._coordinates[0]},${this._coordinates[1]}`;
    }

    get latitude(){
        return this._coordinates[1];
    }
    get longitude(){
        return this._coordinates[0];
    }
    get boundingBox(){
        return this._bbox;
    }
    get boundingBoxString(){
        return `${this._bbox[0][0]},${this._bbox[0][1]},${this._bbox[1][0]},${this._bbox[1][1]}`;
    }
    get name(){
        return this._cityName;
    }
    get nextBikeId(){
        return this._nextbikeId;
    }
}