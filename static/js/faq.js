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
  console.log("here")
  if (panel.style.display === "block") {
    console.log("and there");
    panel.style.display = "none";
  } else {
    panel.style.display = "block";
  }
}

function handleHash() {
  const hash = window.location.hash;
  console.log(hash);
  if (hash) {
    const accr = document.querySelector(hash);
    const absoluteElementTop =
      accr.getBoundingClientRect().top + window.pageYOffset;
    const middle = absoluteElementTop - window.innerHeight / 2;
    window.scrollTo(0, middle + 50);
    const panelg = accr.nextElementSibling;
    accr.classList.toggle("activate");
    checkPanel(panelg);
  }
}

handleHash();
