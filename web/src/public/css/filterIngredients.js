window.addEventListener('DOMContentLoaded', (event) => {
    var ingredientTags = document.getElementById('ingredient_tags');

    ingredientTags.addEventListener("click", function(e) {
        if(e.target && e.target.classList.contains("ingredient_tag")){
            var ingredient = e.target.innerHTML;
            console.log(ingredient);
            var filteredIngredientsTemp = [];
            document.getElementById('hidden').innerHTML.split(',').forEach(element => filteredIngredientsTemp.push(element));
            const index = filteredIngredientsTemp.indexOf(ingredient);
            filteredIngredientsTemp.splice(index, 1);
            if(filteredIngredientsTemp.length == 1) {
                location.href = "/browse";
            }
            else {
                location.href = "/filter_ingredient/"+filteredIngredientsTemp;
            }
        }
        else {
            console.log("nothing");
        }
    });

});

var filterInput = document.getElementById('filter-search-val');
var autocomplete = document.getElementById('search_autocomplete');
var filteredIngredients = [];

autocomplete.addEventListener("click", function(e) {
    if(e.target){
        var searchText = e.target.innerHTML;
        console.log(document.getElementById('hidden').innerHTML);
        document.getElementById('hidden').innerHTML.split(',').forEach(element => filteredIngredients.push(element))
        if(searchText != "" && !filteredIngredients.includes(searchText)){
            filteredIngredients.push(searchText);
        }
        filteredIngredients = filteredIngredients.filter(String);
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