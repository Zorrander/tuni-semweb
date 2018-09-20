var utterance_btn = document.getElementById("new-utterance");
var slot_btn = document.getElementById("new-slot");


function addUtterance(){
  var utterances = document.getElementsByClassName("utterance");
  var current_last_utterance = utterances[utterances.length - 1];
  var ul = document.createElement("ul");
  ul.setAttribute("class","utterance");
  var li = document.createElement("li");
  li.setAttribute("class","slot");
  var input = document.createElement("input");
  input.setAttribute("name","utterance"+utterances.length+"-slot0");
  input.setAttribute("type","text");
  input.setAttribute("value", document.querySelector('[name="skill_name"]').value);
  li.appendChild(input)
  ul.appendChild(li);
  current_last_utterance.insertAdjacentElement("afterend", ul);
}

function addSlot(){
  var utterances = document.getElementsByClassName("utterance");
  var current_last_utterance = utterances[utterances.length - 1];
  var li = document.createElement("li");
  li.setAttribute("class","slot");
  var input = document.createElement("input");
  input.setAttribute("name","utterance"+(utterances.length - 1) +"-slot"+current_last_utterance.getElementsByClassName("slot").length);
  input.setAttribute("type","text");
  li.appendChild(input)
  current_last_utterance.appendChild(li);
}

utterance_btn.addEventListener('click', function(e){
    e.stopPropagation();
    e.preventDefault();
    addUtterance();
  }, false);

slot_btn.addEventListener('click', function(e){
      e.stopPropagation();
      e.preventDefault();
      addSlot();
  }, false);
