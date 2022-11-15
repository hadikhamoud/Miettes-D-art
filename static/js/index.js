var preloader = document.getElementById("pre-loader");
function loaderEnd() {
  preloader.style.display = "none";
}
window.addEventListener("load", loaderEnd);
var reveals = document.querySelectorAll(
  ".reveal-horizontal"
);

console.log(reveals);

function reveal() {

  for (var i = 0; i < reveals.length; i++) {
    var windowHeight = window.innerHeight;
    var elementTop = reveals[i].getBoundingClientRect().top;
    var elementVisible = 150;
    if (elementTop < windowHeight - elementVisible) {
      reveals[i].classList.add("active");
    } 
  }
}


const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry)=> {
    console.log(entry);
    if (entry.isIntersecting){
      entry.target.classList.add("activeV");
    
    }
    else{
      entry.target.classList.remove("activeV");
    }
    
  })
})

const hiddenElements = document.querySelectorAll('.reveal-vertical');
hiddenElements.forEach((el)=> observer.observe(el));






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
document.addEventListener("scroll", (event) => {
  changeNavBarColor();
});
document.addEventListener("scroll", reveal,false);
changeNavBarColor();
document.addEventListener("touchmove",reveal,false);

reveal();
function openForm() {
  document.getElementById("newsletter-Form").style.display = "flex";
}

function closeForm() {
  document.getElementById("newsletter-Form").style.display = "none";
}

function delayOpenForm() {
  if (localStorage.getItem("newsletter") !== "shown") {
    setTimeout(openForm, 5000);
    localStorage.setItem("newsletter", "shown");
  }
}

window.addEventListener("load", delayOpenForm);
