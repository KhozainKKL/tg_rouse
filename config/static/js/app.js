let tg = window.Telegram.WebApp;
tg.expand();

let btn1 = document.getElementById("item-1");
let btn2 = document.getElementById("btn2");
let btn3 = document.getElementById("btn3");
let btn4 = document.getElementById("btn4");
let btn5 = document.getElementById("btn5");
let btn6 = document.getElementById("btn6");

btn1.addEventListener("click", function(){
    document.getElementById("inner").style.display = "none";
    document.getElementById("inner-2").style.display = "block";

});


