var filterInput = document.getElementById('filter-search-val');
var autocomplete = document.getElementById('search_autocomplete');
var filteredIngredients = [];

autocomplete.addEventListener("click", function(e) {
    if(e.target){
        var searchText = e.target.innerHTML;
        console.log(document.getElementById('hidden').innerHTML);
        filteredIngredients.push(document.getElementById('hidden').innerHTML);
        if(searchText != "" && !filteredIngredients.includes(searchText)){
            filteredIngredients.push(searchText);
        }
        location.href = "/filter_ingredient/"+filteredIngredients;
    }
    else {
        console.log("nothing");
    }
});

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
                    document.getElementById('searchbar').style.borderBottomRightRadius = '0px';
                    document.getElementById('searchbar').style.borderBottomLeftRadius = '0px';
                    document.querySelector('.search_autocomplete').style.borderBottom = '1px solid hsl(120, 100%, 35%)';
                }
                else if(ingredient == 'no search') {
                    console.log("no search");
                    document.getElementById('searchbar').style.borderBottomRightRadius = '20px';
                    document.getElementById('searchbar').style.borderBottomLeftRadius = '20px';
                    document.querySelector('.search_autocomplete').style.borderBottom = 'none';
                }
                else {
                    for (var i = 0; i < 10; i++) {
                        if(ingredient[i] == undefined) {
                            document.getElementById('autocomplete_entry'+String(i+1)).innerHTML = "";
                        }
                        else {
                            document.getElementById('autocomplete_entry'+String(i+1)).innerHTML = ingredient[i];
                        }
                        document.getElementById('searchbar').style.borderBottomRightRadius = '0px';
                        document.getElementById('searchbar').style.borderBottomLeftRadius = '0px';
                        document.querySelector('.search_autocomplete').style.borderBottom = '1px solid hsl(120, 100%, 35%)';
                    }
                }
            })
    }
    else {
        for (var i = 0; i < 10; i++) {
            document.getElementById('autocomplete_entry'+String(i+1)).innerHTML = "";
            document.getElementById('searchbar').style.borderBottomRightRadius = '20px';
            document.getElementById('searchbar').style.borderBottomLeftRadius = '20px';
            document.querySelector('.search_autocomplete').style.borderBottom = 'none';
        }
    }
})