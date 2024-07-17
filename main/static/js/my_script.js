const nextLinks = document.querySelectorAll(".pagination .next a");
const previousLinks = document.querySelectorAll(".pagination .previous a");
nextLinks.forEach(link => {link.textContent = "следующая";});
previousLinks.forEach(link => {link.textContent = "предыдущая";});