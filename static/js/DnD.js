function handleDragStart(e) {
  // Target (this) element is the source node.
  this.style.opacity = '0.4';
  e.dataTransfer.effectAllowed = 'copy';
  e.dataTransfer.setData("text", e.target.className);
}

function handleDragEnter(e){
  this.style.border = "dashed";
}

function handleDragOver(e) {
    e.preventDefault();
}

function handleDragLeave(e){
  this.style.border = "solid";
}

function handleDrop(e) {
  // this/e.target is current target element.
  e.preventDefault();
  this.style.border = "solid";
  var data = e.dataTransfer.getData('text');
  e.target.className = data ;
  e.target.classList.add("active")
  e.target.classList.remove("inactive")
  addNewTaskSlot(e.target) ;
  return false;
}

function handleDragEnd(e){
  this.style.opacity = '1';
}

function attachListeners(elem){
  elem.addEventListener('dragenter', handleDragEnter, false);
  elem.addEventListener('dragover', handleDragOver, false);
  elem.addEventListener('dragleave', handleDragLeave, false);
  elem.addEventListener('drop', handleDrop, false);

}

function addNewTaskSlot(referenceNode){
  var li = document.createElement("li");
  li.setAttribute("class", "action inactive")
  li.setAttribute("draggable", "true")
  referenceNode.parentNode.insertBefore(li, referenceNode.nextSibling);
  attachListeners(li);
}

var addStepButton = document.getElementById("addStepButton");

addStepButton.addEventListener('click', function(e){
    addStep(e);
  }, false);

function addStep(e){
  e.stopPropagation();
  e.preventDefault();

  var steps = document.querySelectorAll("#steps > li") ;
  if (steps) {
      var numberSteps = steps.length + 1;
  } else {
    var numberSteps = 1
  }
  var newId = "step"+numberSteps ;

  const some_html = `
    <!-- Step parameters -->
    <div class="modal">
      <div class="modal-content">
        <span class="close">&times;</span>
        <!-- Name of the step -->
        <input class="text-input" name="step`+numberSteps+`-name" type="text" placeholder="Name of the step"></input>

        <!-- List of the tasks to perform for this step -->
        <ul class="tasks"><li class="action" draggable="true"/></ul>
        <!-- Name of the step -->
        <div id="task_store">
          <p>Tasks:</p>
          <ul id="drags">
            <li class="action PickingTask" draggable="true"/>
            <li class="action PlacingTask" draggable="true"/>
            <li class="action PouringLiquidTask" draggable="true"/>
          </ul>
        </div>
        <button class="save">Save</button>
      </div>
    </div>
    <!-- End of step parameters -->
  `;

  var li = document.createElement("li");
  li.setAttribute("class", "action");
  li.setAttribute("id", newId) ;
  li.innerHTML = some_html ;
  var saveButton = li.querySelector("#"+newId +" .save");
  var closeBtn = li.querySelector("#"+newId +" .close");
  closeBtn.addEventListener('click', function(e){
      e.stopPropagation();
      closeStep(newId);
    }, false);
  saveButton.addEventListener('click', function(e){
      e.stopPropagation();
      saveParams(newId);
    }, false);
  li.addEventListener('click', function(e){
      openStep(e.target.id);
    }, false);

  var cols = li.querySelectorAll('.action');
  [].forEach.call(cols, function(col) {
      col.addEventListener('dragstart', handleDragStart, false);
      col.addEventListener('dragend', handleDragEnd, false);
  });

  var cols = li.querySelectorAll('.action');
  [].forEach.call(cols, function(col) {
      attachListeners(col);
  });

  document.getElementById("steps").appendChild(li);
}
