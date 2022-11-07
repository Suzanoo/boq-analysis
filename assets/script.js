const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".sidebar");

// document.querySelectorAll(".nav-link").forEach(n => n.addEventListener("click", () => {

//   hamburger.classList.remove("active");
//   navMenu.classList.remove("active");
// }))

hamburger.addEventListener('click', function(){
  navMenu.classList.toggle('sidebar')
})