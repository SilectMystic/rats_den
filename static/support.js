//define button and form//
const popUpForm = document.getElementById("posts_maker");
var button = document.getElementById("post_button");
//Form Pop-Up//
//button.onclick = () => {window.open('hello!')};//

//button function//
button.addEventListener("click", function() {
  document.getElementById("posts_maker").style.display = "block";
 
});