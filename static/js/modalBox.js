function openStep(stepNumber){
  var query = "#"+stepNumber +" > .modal" ;
  var modal = document.querySelector(query);
  modal.style.display = "block";
}

function closeStep(stepNumber){
  var query = "#"+stepNumber +" > .modal" ;
  var modal = document.querySelector(query);
  modal.style.display = "none";
}

function saveParams(dropboxID) {
  console.log("save-" + dropboxID);
  var form = document.getElementById("form-"+dropboxID);
  console.log(form)
  console.log(form.querySelector('[name="operator"]').value)
  var modal = document.getElementById("modal-"+dropboxID);
  modal.className += " " + form.querySelector('[name="operator"]:checked').value;
  modal.className += " " + form.querySelector('[name="action"]').value;
  var attributes = form.querySelectorAll(".attribute");
  attributes.forEach(function(atr) {
    console.log(atr)
    modal.className += " " + atr.value ;
  });
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(e) {
    var modals = document.getElementsByClassName("modal")
    for (var i = 0; i < modals.length; i++) {
      if (e.target == modals[i]) {
          modals[i].style.display = "none";
      }
    }

}
