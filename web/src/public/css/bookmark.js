
      // var id = '{{recipe[1]}}';
      // var bm = document.getElementById(id);
      //['{{session["email"]}}','{{recipe[1]}}', {{recipe[2]}}, '{{recipe[3]}}', '{{recipe[4]}}', '{{recipe[5]}}', '{{recipe[6]}}', '{{recipe[7]}}', '{{recipe[8]}}', {{recipe[9]}}, {{recipe[10]}}, {{recipe[11]}}

      function bookData(id) {
        
        var book = document.getElementById(String(id))
        if(book.src == 'http://localhost/css/img/bookmarked.svg' ){
          book.src = "https://img.icons8.com/cute-clipart/64/000000/bookmark-ribbon.png"
        }
        else{
          book.src = 'css/img/bookmarked.svg'
        }
        console.log(id);
        var data = { recipe: String(id), email: '{{session["email"]}}', book_src:book.src };
        fetch("http://localhost/bookmark", {
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
 