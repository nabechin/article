document.addEventListener('DOMContentLoaded', function() {
    Array.from(document.getElementsByClassName('article')).forEach(function(e) {
    e.addEventListener('mouseover', function(){
        e.style.backgroundColor  = "#f4f4f5";
        e.style.cursor = "pointer";
    },false);
    e.addEventListener('mouseout', function() {
        e.style.backgroundColor = "";
    }, false);
},false);
},false);



