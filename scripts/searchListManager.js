


export class SearchListManager {
    constructor(mapManager , cityContext, listContainer , toElement , fromElement) {
            this.mapManager = mapManager;
            this.cityContext = cityContext;
            this.listContainer = listContainer;
            this.toElement = toElement;
            this.fromElement = fromElement;
            this.currentFocus = null;
            this.inputTimeout = null;
            this.currentSuggestions = null;
            this.chosenFrom = null;
            this.chosenTo = null;
            this._setupInput();
    }

    _setupInput() {
        const handleInput = async (event) => {
            const inputElement = event.target;
            const query = inputElement.value.trim();
            clearTimeout(this.inputTimeout);
            this.inputTimeout = setTimeout(async () => {
                try {
                    if(query) {
                        const results = await this.searchAddress(query, this.cityContext.center, 10);
                        this.currentSuggestions = results;
                        this.clearSuggestions();
                        this.displaySuggestions();
                        console.log(results);
                    }
                    else {
                        this.clearSuggestions();
                        this.currentSuggestions = null;
                    }
                } catch (error) {
                    console.error("Input failed",error);
                }

            }, 300);
        }
        this.toElement.addEventListener('input', handleInput);
        this.toElement.addEventListener('focus', () => this.currentFocus = this.toElement);
        this.fromElement.addEventListener('input', handleInput);
        this.fromElement.addEventListener('focus', () => this.currentFocus = this.fromElement);
    }

    async searchAddress(query , location , limit ) {
        /**
         * @param {string} query - query
         * @param {number} limit - Limit the search to n results
         * @param {[number , number]} location - Bias the search to this location [latitude , longitude]
         */
        let url = `http://localhost:3001/api/search?query=${encodeURIComponent(query)}&limit=${limit}&bounds=${encodeURIComponent(this.cityContext.boundingBoxString)}`;

        try {
            if (!query || typeof query !== 'string') {
                throw new Error('Invalid search query');
            }

            console.log(url);

            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`API request failed with status ${response.status}`);
            }

            const data = await response.json();
            return {
                query, location,
                results: data.suggestions.map(suggestion => ({
                    id: suggestion.mapbox_id,
                    name: suggestion.name,
                    address: suggestion.address,
                    addressContext: suggestion.context.address,
                    type: suggestion.feature_type,
                    categories: suggestion.poi_category
                }))
            }


        } catch (error) {
            console.error('Search error:', error);

            throw error;
        }
    }
    displaySuggestions(){
        if(!this.currentSuggestions){
            return;
        }
        this.currentSuggestions.results.forEach((suggestion) => {
            const suggestionItem = this.getSuggestionItem(suggestion);
            suggestionItem.addEventListener('click', () => {
                            this.currentFocus.value = suggestion.name;
                            if(this.currentFocus === this.fromElement){
                                this.updateChosen(suggestion , "from");
                            }
                            if(this.currentFocus === this.toElement){
                                this.updateChosen(suggestion , "to");
                            }
                            //@todo more on click suggestion logic that will come

            });
            this.listContainer.append(suggestionItem);
        })
    }
    getSuggestionItem(suggestion){
        const suggestionItem = document.createElement('div');
        suggestionItem.className = 'suggestion-item';

    switch(suggestion.type){
        case 'poi':
            suggestionItem.innerHTML = `<strong>${suggestion.name}</strong><br>
                                        <small>${suggestion.address || ""}</small>`;
            return suggestionItem;

        case 'address':
            suggestionItem.innerHTML = `<strong>${suggestion.address}</strong><br>
                                        <small>Address </small>`;
            return suggestionItem;

    }
    }
    async updateChosen(suggestion , id){
        this.mapManager.removeMarker(id)
        this.chosenFrom = await this.retrivePoint(suggestion.id);
        this.mapManager.addMarker(this.chosenFrom.features[0] , id)
    }



    clearSuggestions(){
        this.listContainer.innerHTML = '';

    }
    async retrivePoint(id){
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

}