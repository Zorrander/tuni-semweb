$('.tab-content').hide();
$('#tabs a:first').addClass('active');
$('.tab-content:first').show();

$('#tabs a').click(function(event) {
  $('#tabs a').removeClass('active');
  $(this).addClass('active');
  $('.tab-content').hide();

  var selectTab = $(this).attr("href");

  $(selectTab).fadeIn();
});

var numberSteps = 1 ;

function addPickTask(listTask) {
  var li = document.createElement("li");
  li.className = 'list-group-item list-group-item-primary';
  li.innerHTML = "Pick";
  listTask.appendChild(li);
}

function addPlaceTask(listTask) {
  var li = document.createElement("li");
  li.className = 'list-group-item list-group-item-warning';
  li.innerHTML = "Place";
  listTask.appendChild(li);
}

function addPourTask(listTask) {
  var li = document.createElement("li");
  li.className = 'list-group-item list-group-item-info';
  li.innerHTML = "Pour";
  listTask.appendChild(li);
}

$(".btn-outline-primary").click(function() {
  addPickTask($(".list-group")[0]);
});
$(".btn-outline-warning").click(function() {
  addPlaceTask($(".list-group")[0]);
});
$(".btn-outline-info").click(function() {
  addPourTask($(".list-group")[0]);
});

function initializeStep(step) {
  numberSteps+=1;
  var headingId = 'heading' + numberSteps.toString();
  var collapseId = 'collapse' + numberSteps.toString();

  step.querySelector(".card-header").id = headingId;
  step.querySelector(".btn-link").setAttribute("data-target", "#"+collapseId);
  step.querySelector(".btn-link").setAttribute("aria-controls", collapseId);
  step.querySelector(".btn-link").innerHTML = "Step " + numberSteps;
  step.querySelector(".collapse").id = collapseId;
  step.querySelector(".collapse").setAttribute("aria-labelledby", headingId);
  var list = step.querySelector(".list-group");
  while (list.firstChild) {
      list.removeChild(list.firstChild);
  }
}

$('#addStepButton').bind('click', function() {
  var cln = document.querySelector(".step").cloneNode(true);
  initializeStep(cln);
  document.getElementById("accordion").appendChild(cln);

  var listTasks = cln.querySelector(".list-group");
  cln.querySelector(".btn-outline-primary").onclick = function() {
    console.log("clicked");
    addPickTask(listTasks);
  };
  cln.querySelector(".btn-outline-warning").onclick = function() {
    addPlaceTask(listTasks);
  };
  cln.querySelector(".btn-outline-info").onclick = function() {

    addPourTask(listTasks);
  };

});

$('#create').bind('click', function() {
  var steps = [];
  var tasks = [];
  $('#accordion').children('.step').each(function () {
      steps.push($(this).children().find(".btn-link")[0].innerText);
      var sequence = [];
      $(this).children().find("ul > li").each(function () {
        sequence.push(this.innerText);
      });
      tasks.push(sequence);
  });
  console.log(JSON.stringify(steps));
  $.getJSON($SCRIPT_ROOT + '/skills/create/payload', {
    skill_name: $('input[name="skill_name"]').val(),
    action: $('input[name="action"]').val(),
    target: $('input[name="target"]').val(),
    step: JSON.stringify(steps),
    task: JSON.stringify(tasks),
  }, function(data) {
    $('.alert')[0].classList.add('show');
  })
});
