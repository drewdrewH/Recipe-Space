function addBasket(id) {
        
    var book = document.getElementById(String(id))
    
    console.log(id);
    var data = { recipe: String(id), email: '{{session["email"]}}'};
    fetch("http://localhost/addBasket", {
      method: "POST",
      body: JSON.stringify(data),
      headers: { "Content-type": "application/json; charset=UTF-8" },
    })
      .then(function (response) {
        if (response.status >= 200 && response.status <= 299) {
          window.location.reload();
          return response.json();
        } else {
          throw Error(response.statusText);
        }
      })
      .then()
      .catch((error) => {});
  }