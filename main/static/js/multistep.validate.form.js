let currentTab = 0;
showTab(currentTab);

function showTab(n) {

    let x = document.getElementsByClassName("step");

    x[n].style.display = "block";

    let progress = (n / (x.length - 1)) * 100;

    document.querySelector(".progress-bar").style.width = progress + "%";
    document.querySelector(".progress-bar").setAttribute("aria-valuenow", progress);
    document.getElementById("prevBtn").style.display = n == 0 ? "none" : "inline";
    document.getElementById("nextBtn").innerHTML = n == x.length - 1 ? "Сохранить" : "Далее";

}




function nextPrev(n) {

    let x = document.getElementsByClassName("step");

    if (n == 1 && !validateForm()) return false;
    x[currentTab].style.display = "none";
    currentTab += n;

    if (currentTab >= x.length) {
        if (confirm("Сохранить тест?")) {

            currentTab = x.length - 1;
            showTab(currentTab);
            document.getElementById("myForm").submit();
            return false;

        }

        else {

            // Вернуться к текущему шагу

            currentTab = x.length - 1;
            showTab(currentTab);
            return false;
        }
    }

    showTab(currentTab);
}





function validateForm() {

    let valid = true;
    let x = document.getElementsByClassName("step");
    let y = x[currentTab].getElementsByTagName("input");
    let selects = x[currentTab].getElementsByTagName("select");
    let radios = x[currentTab].querySelectorAll("input.form-check-input[type='radio']");
    console.log("Количество радиокнопок на текущем шаге: ", radios.length);



    for (var i = 0; i < y.length; i++) {
        if (y[i].value == "") {
            y[i].className += " invalid";
            valid = false;
        }
        }



for (var i = 0; i < selects.length; i++) {
if (selects[i].value === "Выберите из выпадающего списка") {
selects[i].className += " invalid";
valid = false;
} else {
selects[i].className = selects[i].className.replace(" invalid", "");
}
}



// Проходим по всем радиокнопкам
for (var i = 0; i < radios.length; i++) {
// Если ни одна радиокнопка не выбрана
if (!radios[i].checked) {
// Добавляем класс "invalid" к неверно заполненному полю
radios[i].classList.add("invalid");
valid = false;
} else {

// Если радиокнопка выбрана, удаляем класс "invalid"
for (var j = 0; j < radios.length; j++) {
radios[j].classList.remove("invalid");
}
valid = true;
break;
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