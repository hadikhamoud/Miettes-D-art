var acc = document.getElementsByClassName("accordion-faq");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function () {
    this.classList.toggle("activate");
    var panel = this.nextElementSibling;
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }
  });
}

function checkPanel(panel) {
  if (panel.style.display === "block") {
    panel.style.display = "none";
  } else {
    panel.style.display = "block";
  }
}

function handleHash() {
  var hash = window.location.hash;
  console.log(hash);
  if (hash) {
    var acc = document.querySelector(hash);
    acc.scrollIntoView({ behavior: "smooth", block: "center" });
    var panel = acc.nextElementSibling;
    acc.classList.toggle("activate");
    checkPanel(panel);
  }
}

handleHash();
