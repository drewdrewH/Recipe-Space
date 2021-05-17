var filterInput = document.getElementById('filter-search-val');


filterInput.addEventListener('input', (event) =>{
    var searchText = filterInput.value;
    if(searchText != ""){
        fetch('/search_autocomplete/'+searchText)
            .then(response => response.json())
            .then(function(data) {
                console.log(data);
                var ingredient = data['ingredients']
                if(ingredient == 'no records') {
                    document.getElementById('autocomplete_entry'+String(1)).innerHTML = "no matching ingredients";
                    for (var i = 1; i < 10; i++) {
                        document.getElementById('autocomplete_entry'+String(i+1)).innerHTML = "";
                    }
                }
                else if(ingredient == 'no search') {
                    console.log("no search");
                }
                else {
                    for (var i = 0; i < 10; i++) {
                        if(ingredient[i] == undefined) {
                            document.getElementById('autocomplete_entry'+String(i+1)).innerHTML = "";
                        }
                        else {
                            document.getElementById('autocomplete_entry'+String(i+1)).innerHTML = ingredient[i];
                        }
                    }
                }
            })
    }
    else {
        for (var i = 0; i < 10; i++) {
            document.getElementById('autocomplete_entry'+String(i+1)).innerHTML = "";
        }
    }
})