function func(c) {let x, i;
    x = document.getElementsByClassName("hide_filt");
    for (i = 0; i < x.length; i++) {
        RemoveClass(x[i]);
        if (x[i].className.indexOf(c) > -1) AddClass(x[i]);}}

function AddClass(element) {if (element.className.split(" ").indexOf("show") == -1) {element.className += " " + "show";}}
  
function RemoveClass(element) {let arr1;
      arr1 = element.className.split(" ");
      while (arr1.indexOf("show") > -1) {arr1.splice(arr1.indexOf("show"), 1);}
      element.className = arr1.join(" ");}


function func_card(filter) {let i, cards, req, cl_card;
    cards = document.getElementsByClassName("card");
    req = document.getElementById(filter).value;
    for (i = 0; i < cards; i++) { cl_card = cards[i].className
        if (cards[i].value.includes(req) && cl_card.includes(' show ')) {
    }   else if (cards[i].value.includes(req) && !cl_card.includes(' show ')) {
        cl_card += ' show';
    }   else if (!cards[i].value.includes(req) && cl_card.includes(' show ')) {
        cl_card.replace(' show', '');
    }   else {};
    }
}