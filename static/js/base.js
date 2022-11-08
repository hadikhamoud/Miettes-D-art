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

function reveal() {
  var reveals = document.querySelectorAll(
    ".reveal-horizontal, .reveal-vertical"
  );
  for (var i = 0; i < reveals.length; i++) {
    var windowHeight = window.innerHeight;
    var elementTop = reveals[i].getBoundingClientRect().top;
    var elementVisible = 150;
    if (elementTop < windowHeight - elementVisible) {
      reveals[i].classList.add("active");
    } else {
      reveals[i].classList.remove("active");
    }
  }
}

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

var images = document.querySelectorAll(".product_image");
images.forEach(function (image) {
  image.addEventListener("load", (event) => {
    var img = event.target;
    var parent = img.parentElement;

    parent.classList.add("loaded");
  });

  if (image.complete) {
    var parent = image.parentElement;
    parent.classList.add("loaded");
  }
});
