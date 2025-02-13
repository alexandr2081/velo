function func(value, tf) {let x, i
    x = document.getElementsByClassName("hide")
    for (i = 0; i < x.length; i++) {RemoveClass(x[i])
      if (x[i].className.indexOf(value) > -1 && x[i].className.indexOf("show") == -1) {
        x[i].className += " show"}}
    if (tf){func_card('type', 'char')}}

function lol() {console.log('wt')}
function RemoveClass(element) {let i, arr1
    arr1 = element.className.split(" ")
    while (arr1.indexOf("show") > -1) {arr1.splice(arr1.indexOf("show"), 1)}
    element.className = arr1.join(" ")}

//   func_card('', '', tf=false)
  function func_card(filter, how, tf=true) {let i, cards, cl_card, dict, when, prefil
    cards = document.getElementsByClassName('card_hide')
    if (tf) {
      prefil = JSON.parse(document.getElementById('filters').value.replaceAll('&#39;', '"'))
      prefil[filter] = [document.getElementById(filter).value, how]
      document.getElementById('filters').value = JSON.stringify(prefil)
      console.log(prefil, JSON.stringify(prefil), document.getElementById('filters').value)
      for (let filt of Object.keys(prefil)) {
        for (i = 0; i < cards.length; i++) {dict = JSON.parse(cards[i].value.replaceAll('&#39;', '"'))

          if (prefil[filt][1] == 'comp') {
            if (filt.split('_')[1] == 'less') {when = parseInt(dict[filt.split('_')[0]]) <= parseInt(prefil[filt][0])} 
            else {when = parseInt(dict[filt.split('_')[0]]) >= parseInt(prefil[filt][0])}
          } else if (prefil[filt][1] == 'char') {when = dict[filt] == prefil[filt][0]
          } else if (prefil[filt][1] == 'param') {when = dict['param'].includes(prefil[filt][0])}

          if (prefil[filt][0] == 'all') {when = true}
          if (when && !cards[i].className.includes('show')) {
            cards[i].className += ' show'
          } else if (!when && cards[i].className.includes('show')) {
            cards[i].className = cards[i].className.replace(' show', '')}}}}
    else {for (i = 0; i < cards.length; i++) {cards[i].className += ' show'}}

    if (document.getElementsByClassName('show').length == 0 && !document.getElementById("no_details").className.includes("show_no")) {
      document.getElementById("no_details").className += ' show_no'
    } else if (!document.getElementsByClassName('show').length == 0 && document.getElementById("no_details").className.includes("show_no")) {
      document.getElementById("no_details").className = document.getElementById("no_details").className.replace(' show_no', '')}}