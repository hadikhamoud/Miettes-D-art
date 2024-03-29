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
  const hash = window.location.hash;
  console.log(hash);
  if (hash) {
    const acc = document.querySelector(hash);
    const absoluteElementTop =
      acc.getBoundingClientRect().top + window.pageYOffset;
    const middle = absoluteElementTop - window.innerHeight / 2;
    window.scrollTo(0, middle + 50);
    const panel = acc.nextElementSibling;
    acc.classList.toggle("activate");
    checkPanel(panel);
  }
}

handleHash();
