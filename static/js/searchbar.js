// updated 2019
const input = document.getElementById("search2-input2");
const searchBtn = document.getElementById("search2-btn");

const expand = () => {
  searchBtn.classList.toggle("close2");
  input.classList.toggle("square2");
};

searchBtn.addEventListener("click", expand);




//  old version / jquery
//
// function expand() {
//   $(".search").toggleClass("close");
//   $(".input").toggleClass("square");
//   if ($('.search').hasClass('close')) {
//     $('input').focus();
//   } else {
//     $('input').blur();
//   }
// }
// $('button').on('click', expand);
//
