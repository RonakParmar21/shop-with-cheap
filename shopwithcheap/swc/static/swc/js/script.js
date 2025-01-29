const bar = document.getElementById("bar");
const cross = document.getElementById("cross");
const menu = document.querySelector("nav ul");

bar.addEventListener("click", () => {
  menu.classList.add("show-menu");
  cross.style.display = "block";
  bar.style.display = "none";
});

cross.addEventListener("click", () => {
  menu.classList.remove("show-menu");
  cross.style.display = "none";
  bar.style.display = "block";
});
