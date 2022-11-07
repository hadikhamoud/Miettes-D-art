function getQuerystring(key) {
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i = 0; i < vars.length; i++) {
    var pair = vars[i].split("=");
    if (pair[0] == key) {
      return pair[1];
    }
  }
}

function preserveFilter(key, defaultIn) {
  var filter = getQuerystring(key);
  if (filter !== undefined) {
    document.getElementById(key).value = filter;
  } else {
    document.getElementById(key).value = defaultIn;
  }
}

preserveFilter("Category", "Category");
preserveFilter("sort_by", "Sort");
preserveFilter("Color", "Color");

function handleFilters() {
  var url = "/products/?";
  var category = document.getElementById("Category").value;
  var sort_by = document.getElementById("sort_by").value;
  var color = document.getElementById("Color").value;
  if (category !== "Category") url += "Category=" + category + "&";
  if (sort_by !== "Sort") url += "sort_by=" + sort_by + "&";
  if (color !== "Color") url += "Color=" + color;

  window.location.href = url;
}
