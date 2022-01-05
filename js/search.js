(function () {
  function displaySearchResults(results, store) {
    var searchResults = document.getElementById('search-results');

    if (results.length) { // Are there any results?
      var appendString = '';

      for (var i = 0; i < results.length; i++) {  // Iterate over the results
        var item = store[results[i].ref];
        appendString += '<li><h3><a href="' + item.url + '">' + item.title + '</a></h3>';
        appendString += '<p>' + item.description.substring(0, 150) + '...</p></li>';
      }

      searchResults.innerHTML = appendString;
    } else {
      searchResults.innerHTML = '<li>Geen resultaten gevonden.</li>';
    }
  }

  function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split('&');

    for (var i = 0; i < vars.length; i++) {
      var pair = vars[i].split('=');

      if (pair[0] === variable) {
        return decodeURIComponent(pair[1].replace(/\+/g, '%20'));
      }
      
    }
  }

  
  function search(searchTerm) {
    var results = idx.search(searchTerm); // Get lunr to perform a search
    displaySearchResults(results, window.store); // We'll write this in the next section

    var queryParams = new URLSearchParams(window.location.search);
    queryParams.set("query", searchTerm);
    history.replaceState(null, null, "?" + queryParams.toString());
  }

  // Initalize lunr with the fields it will be searching on. I've given title
  // a boost of 10 to indicate matches on this field are more important.
  var idx = lunr(function () {
    this.field('id');
    this.field('title', { boost: 10 });
    this.field('author');
    this.field('tags');
    this.field('category');
    this.field('description');

    for (var key in window.store) { // Add the data to lunr
      this.add({
        'id': key,
        'title': window.store[key].title,
        'author': window.store[key].author,
        'tags': window.store[key].tags,
        'category': window.store[key].category,
        'description': window.store[key].description,
      });
    }

  });

  document.getElementById('search-box').addEventListener('keyup', function (e) {
    var searchTerm = document.getElementById('search-box').value;
    if (searchTerm) {
      search(searchTerm);
    } else {
      displaySearchResults([], window.store);
      var queryParams = new URLSearchParams(window.location.search);
      queryParams.delete("query");
      history.replaceState(null, null, "?" + queryParams.toString());
    }
  });

  var searchTerm = getQueryVariable('query');
  if (searchTerm) {
    document.getElementById('search-box').setAttribute("value", searchTerm);
    search(searchTerm);
  }
})();