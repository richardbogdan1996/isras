let currentTab = 0;
showTab(currentTab);


function showTab(n) {

let x = document.getElementsByClassName("step");
x[n].style.display = "block";
let progress = (n / (x.length - 1)) * 100;
document.querySelector(".progress-bar")
.style.width = progress + "%";
document.querySelector(".progress-bar")
.setAttribute("aria-valuenow", progress);
document.getElementById("prevBtn")
.style.display = n == 0 ? "none" : "inline";
document.getElementById("nextBtn")
.innerHTML = n == x.length - 1 ? "Submit" : "Далее";

}

function nextPrev(n) {
let x = document.getElementsByClassName("step");
if (n == 1 && !validateForm()) return false;
x[currentTab].style.display = "none";
currentTab += n;
if (currentTab >= x.length) {
resetForm();
return false;
}
showTab(currentTab);
}




function validateForm() {

let valid = true;
let x = document.getElementsByClassName("step");
let y = x[currentTab].getElementsByTagName("input");
let selects = x[currentTab].getElementsByTagName("select");



// Проверяем поля ввода

for (var i = 0; i < y.length; i++) {
if (y[i].value == "") {
y[i].className += " invalid";
valid = false;
} else {
y[i].className = y[i].className.replace(" invalid", "");
}
}

// Проверяем выпадающий список

for (var i = 0; i < selects.length; i++) {
    if (selects[i].value === "Выберите из выпадающего списка") {
      selects[i].className += " invalid";
      valid = false;
    } else {
      selects[i].className = selects[i].className.replace(" invalid", "");
    }
  }

return valid;
}


function resetForm() {

let x = document.getElementsByClassName("step");
for (var i = 0; i < x.length; i++) {
x[i].style.display = "none";
}


let inputs = document.querySelectorAll("input");
inputs.forEach(input => {
input.value = "";
input.className = "";
});


currentTab = 0;
showTab(currentTab);
document.querySelector(".progress-bar")
.style.width = "0%";
document.querySelector(".progress-bar")
.setAttribute("aria-valuenow", 0);
document.getElementById("prevBtn")
.style.display = "none";

}



const dateInput = document.getElementById('child_birthday');
dateInput.addEventListener('click', () => {
    dateInput.showPicker();
  });




