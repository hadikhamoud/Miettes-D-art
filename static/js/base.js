function openNav() {
  document
    .getElementById("mobile-navbar")
    .setAttribute(
      "style",
      "width:60%; box-shadow: 0 0 0 100vmax rgba(0,0,0,.7);"
    );
  // document.getElementsByTagName("BODY")[0].setAttribute("style", "background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7));")
}

function closeNav() {
  document.getElementById("mobile-navbar").setAttribute("style", "width:0");
  document
    .getElementById("mobile-navbar")
    .removeAttribute("style", "box-shadow: 0 0 0 100vmax rgba(0,0,0,.7);");

  // document.getElementsByTagName("BODY")[0].removeAttribute("style", "background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7));")
}

function openCart() {
  const width = window.innerWidth;
  if (width > 769) {
    document
      .getElementById("shopping-cart")
      .setAttribute(
        "style",
        "width:40%; box-shadow: 0 0 0 100vmax rgba(0,0,0,.7);"
      );
  } else {
    document
      .getElementById("shopping-cart")
      .setAttribute(
        "style",
        "width:80%; box-shadow: 0 0 0 100vmax rgba(0,0,0,.7);"
      );
  }
  // document.getElementById("shopping-cart").setAttribute("style", ");
  // document.getElementsByTagName("BODY")[0].setAttribute("style", "background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7));")
}

function closeCart() {
  document
    .getElementById("shopping-cart")
    .removeAttribute("style", "box-shadow: 0 0 0 100vmax rgba(0,0,0,.7);");
  document.getElementById("shopping-cart").setAttribute("style", "width:0;");
  // document.getElementsByTagName("BODY")[0].removeAttribute("style", "background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7));")
}

addEventListener("resize", (event) => {
  const width = window.innerWidth;

  if (width > 890) {
    closeNav();
  }
});

addEventListener("click", (event) => {
  var sidebar = document.getElementById("mobile-navbar");
  var sidebarPos = sidebar.getBoundingClientRect();
  var cart = document.getElementById("shopping-cart");
  var cartPos = cart.getBoundingClientRect();

  if (cartPos.width > 0 && !cart.contains(event.target)) {
    closeCart();
  }

  if (sidebarPos.width > 0 && !sidebar.contains(event.target)) {
    closeNav();
  }
});

function checkTyping() {
  var input = document.getElementById("searchright");
  if (input.value != "") {
    document.getElementById("search-button").disabled = false;
  } else {
    document.getElementById("search-button").disabled = true;
  }
}

function checkTypingMobile() {
  var input = document.getElementById("searchright-mobile");
  if (input.value != "") {
    document.getElementById("search-button-mobile").disabled = false;
  } else {
    document.getElementById("search-button-mobile").disabled = true;
  }
}
function handle(event) {
  event.preventDefault();
}
