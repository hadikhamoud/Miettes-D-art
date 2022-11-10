var counter = 1;
addEventListener("click", (event) => {
  var thumbnails = document.getElementById("thumbnails");
  console.log(event.target.id);
  if (thumbnails.contains(event.target)) {
    // thumbnails.getElementByTagName("img")[0].removeAttribute("style", "border-style: solid;")
    // event.target.setAttribute("style", "border-style: solid;")
    document
      .getElementById("slide" + event.target.id)
      .setAttribute("style", `z-index: ${counter + 3};`);
    counter += 1;
  }
});

var acc = document.getElementsByClassName("accordionDetails");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function () {
    this.classList.toggle("activate");
    var panel = this.nextElementSibling;
    if (panel.style.display === "flex") {
      panel.style.display = "none";
    } else {
      panel.style.display = "flex";
    }
  });
}

const slider = document.querySelector(".wrapper-container-mobile"),
  slides = Array.from(document.querySelectorAll(".slide-mobile")),
  dots = Array.from(document.querySelectorAll(".dot"));

let isDragging = false,
  startPos = 0,
  currentTranslate = 0,
  prevTranslate = 0,
  animationID = 0,
  currentIndex = 0;

dots[0].classList.add("dot-selected");

slides.forEach((slide, index) => {
  const slideImage = slide.querySelector("img");
  slideImage.addEventListener("dragstart", (e) => e.preventDefault());

  // Touch events
  slide.addEventListener("touchstart", touchStart(index));
  slide.addEventListener("touchend", touchEnd);
  slide.addEventListener("touchmove", touchMove);

  // Mouse events
  slide.addEventListener("mousedown", touchStart(index));
  slide.addEventListener("mouseup", touchEnd);
  slide.addEventListener("mouseleave", touchEnd);
  slide.addEventListener("mousemove", touchMove);
});

// Disable context menu
window.oncontextmenu = function (event) {
  event.preventDefault();
  event.stopPropagation();
  return false;
};

function touchStart(index) {
  return function (event) {
    currentIndex = index;
    startPos = getPositionX(event);
    isDragging = true;

    // https://css-tricks.com/using-requestanimationframe/
    animationID = requestAnimationFrame(animation);
    slider.classList.add("grabbing");
  };
}

function touchEnd() {
  isDragging = false;
  cancelAnimationFrame(animationID);

  const movedBy = currentTranslate - prevTranslate;

  if (movedBy < -100 && currentIndex < slides.length - 1) {
    dots[currentIndex].classList.remove("dot-selected");
    currentIndex += 1;
    dots[currentIndex].classList.add("dot-selected");
  }

  if (movedBy > 100 && currentIndex > 0) {
    dots[currentIndex].classList.remove("dot-selected");
    currentIndex -= 1;
    dots[currentIndex].classList.add("dot-selected");
  }

  setPositionByIndex();

  slider.classList.remove("grabbing");
}

function touchMove(event) {
  event.preventDefault();
  if (isDragging) {
    const currentPosition = getPositionX(event);
    currentTranslate = prevTranslate + currentPosition - startPos;
  }
}

function getPositionX(event) {
  return event.type.includes("mouse") ? event.pageX : event.touches[0].clientX;
}

function animation() {
  setSliderPosition();
  if (isDragging) requestAnimationFrame(animation);
}

function setSliderPosition() {
  slider.style.transform = `translateX(${currentTranslate}px)`;
}

function setPositionByIndex() {
  currentTranslate = currentIndex * -window.innerWidth;
  prevTranslate = currentTranslate;
  setSliderPosition();
}

// window.addEventListener("resize", function (event) {
//   currentTranslate = 0;
//   setSliderPosition();
// });
