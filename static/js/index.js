var preloader = document.getElementById("pre-loader");
function loaderEnd() {
  preloader.style.display = "none";
}
window.addEventListener("load", loaderEnd);
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

function changeNavBarColor() {
  var topper = window.pageYOffset || document.documentElement.scrollTop;
  var navbar = document.getElementById("navbar");
  var v = document.querySelector(":root");
  if (topper > 200) {
    navbar.setAttribute("style", "background-color: white;");
    v.style.setProperty("--color_fill", "#444c57");
    v.style.setProperty("--second_color_fill", "#91aabf");
  } else {
    navbar.removeAttribute("style", "background-color: white;");
    v.style.setProperty("--color_fill", "white");
    v.style.setProperty("--second_color_fill", "white");
  }
}
addEventListener("scroll", (event) => {
  changeNavBarColor();
});
window.addEventListener("scroll", reveal);
changeNavBarColor();
window.addEventListener("scroll", reveal);
reveal();

function openForm() {
  document.getElementById("newsletter-Form").style.display = "flex";
}

function closeForm() {
  document.getElementById("newsletter-Form").style.display = "none";
}

function delayOpenForm() {
  if (sessionStorage.getItem("newsletter") !== "shown") {
    setTimeout(openForm, 5000);
    sessionStorage.setItem("newsletter", "shown");
  }
}

window.addEventListener("load", delayOpenForm);
