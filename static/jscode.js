let button_start = document.querySelector("#button-start")

button_start.addEventListener('mouseover', function(){
    button_start.style.color = "dodgerblue";
    button_start.style.background = "white";
})

button_start.addEventListener('mouseout', function(){
    button_start.style.background = "red";
    button_start.style.color = "white";
})