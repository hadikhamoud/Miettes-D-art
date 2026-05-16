var country = document.getElementById("id_Phone_number_0");
country.options[country.selectedIndex].text = country.value;

country.addEventListener("change", function () {
  this.options[this.selectedIndex].text = this.value;
});
