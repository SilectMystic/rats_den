//define button and form//
const popUpForm = document.getElementById("posts_maker");
var button = document.getElementById("post_button");
var button2 = document.getElementById('pclose_button');
//Form Pop-Up//
//button.onclick = () => {window.open('hello!')};//

//button function//
button.addEventListener("click", function() {
  document.getElementById("posts_maker").style.display = "block";
 
});

button2.addEventListener('click', function() {
  document.getElementById('posts_maker').style.display = 'none';
});