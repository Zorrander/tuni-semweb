var ros;
var speechTopic ;
var listeners = [];



/* ##########################################################################
        CONNECTION TO ROS
########################################################################## */

//var ros = new ROSLIB.Ros({
//  url : 'ws://localhost:9090'
//});


function connectToROS(webserverUrl){
  console.log("Trying to connect...")
  ros = new ROSLIB.Ros({
    url : webserverUrl
  });
}

function alert_success(){
  $(".alert")[0].innerHTML = "Connection successful !";
  $(".alert")[0].classList = ["alert alert-success show"];
  dismiss_alert();
}

function alert_failure(){
  $(".alert")[0].innerHTML = "Unable to connect...";
  $(".alert")[0].classList = ["alert alert-danger show"];
  dismiss_alert();
}

function updateStateIndicator(state) {
  $('#indicator_state .badge')[0].innerHTML = state;
}

function updateIndicator() {
  $('#indicator_connection .badge')[0].classList = "badge badge-success float-right";
  $('#indicator_connection .badge')[0].innerHTML = "Robot connected";
  $('#indicator_state .badge').show();
}

function cancelIndicator() {
  $('#indicator_connection .badge')[0].classList = "badge badge-warning float-right";
  $('#indicator_connection .badge')[0].innerHTML = "Robot not connected";
}


function updateRobotState(new_state){
  document.querySelector(".bg-info").classList.remove('bg-info');
  document.getElementById(new_state).classList.add('bg-info');
  updateStateIndicator(new_state);
}

function connected_callback(){
  alert_success();
  /*$.getJSON($SCRIPT_ROOT + '/robot/connect', {
    url: ros.socket.url }, function(data) {
      updateIndicator();
  });

  speechTopic = new ROSLIB.Topic({
      ros : ros,
      name : '/speech_output',
      messageType : 'std_msgs/String'
  });

  var listener = new ROSLIB.Topic({
    ros : ros,
    name : '/speech_to_text',
    messageType : 'std_msgs/String'
  });

  listener.subscribe(function(message) {
    console.log(message.data);
    var msg = message.data ;
    processRequest(msg) ;
  });

  listeners.push(listener);
  // say("Robot connected");
  */
}

function error_callback(){
    alert_failure();
    console.log('Error connecting to websocket server: ', error);
}

function disconnected_callback() {
  cancelIndicator();
  listeners.forEach(function(listener) {
    listener.unsubscribe();
  });
}

$('#connect').bind('click', function(e) {
  e.preventDefault()
  connectToROS($('input[name="url"]').val())
  ros.on('connection', connected_callback);
  ros.on('error', error_callback);
  ros.on('close', disconnected_callback);
});

/* ##########################################################################
        TEST BENCH
########################################################################## */

$('#start_grasp').bind('click', function(e) {
  e.preventDefault()
  var testTopic = new ROSLIB.Topic({
    ros : ros,
    name : '/test_bench',
    messageType : 'cobot_controllers/Test'
  });

  console.log("Starting routine....");

  var new_test = new ROSLIB.Message({
    width : parseFloat($('input[name="width"]').val()),
    force : parseInt($('input[name="force"]').val()),
    reps : parseInt($('input[name="reps"]').val())
  });

  console.log(new_test);
  testTopic.publish(new_test);
});

$('#move_start').bind('click', function(e) {
  e.preventDefault()
  var move_start_topic = new ROSLIB.Topic({
    ros : ros,
    name : '/move_start',
    messageType : 'std_msgs/Empty'
  });
  console.log("Go to start");
  var new_move = new ROSLIB.Message({});
  move_start_topic.publish(new_move);
});

$('#move_approach').bind('click', function(e) {
  e.preventDefault()
  var approachTopic = new ROSLIB.Topic({
    ros : ros,
    name : '/approach_cmd',
    messageType : 'std_msgs/Empty'
  });
  console.log("approach_cmd");
  var new_move = new ROSLIB.Message({});
  approachTopic.publish(new_move);
});

$('#test_height').bind('click', function(e) {
  e.preventDefault()
  var testHeightTopic = new ROSLIB.Topic({
    ros : ros,
    name : '/height_test',
    messageType : 'std_msgs/Float32'
  });
  console.log("Test height....");
  var new_height = new ROSLIB.Message({
    data : parseFloat($('input[name="height"]').val())
  });
  testHeightTopic.publish(new_height);
});

$('#opening').bind('click', function(e) {
  e.preventDefault()
  var openingTopic = new ROSLIB.Topic({
    ros : ros,
    name : '/franka_gripper/move/goal',
    messageType : 'franka_gripper/MoveActionGoal'
  });
  console.log("Opening");
  var new_opening = new ROSLIB.Message({
    goal :
            {
                width: 0.08,
                speed: 20.0
            }

  });
  openingTopic.publish(new_opening);
});

$('#homing').bind('click', function(e) {
  e.preventDefault()
  var homingTopic = new ROSLIB.Topic({
    ros : ros,
    name : '/homing_cmd',
    messageType : 'std_msgs/Empty'
  });
  console.log("Homing");
  var new_homing = new ROSLIB.Message({});
  homingTopic.publish(new_homing);
});

/* ##########################################################################
        DISPLAY PLANER STATUS
########################################################################## */

function updatePlanningPolicies(){
  var listServicesClient = new ROSLIB.Service({
    ros : ros,
    name : '/rosapi/services',
    serviceType : 'rosapi/Services'
  });

  var request = new ROSLIB.ServiceRequest();

  listServicesClient.callService(request, function(result) {
    result.services.forEach(function(element) {
      if (element.startsWith('/planner/')) {
        var select = document.getElementById("policy-selector");
        var option = document.createElement("option");
        option.text = element.split("/planner/")[1];
        select.add(option);
      }
    });
  });
}

function updateControllerList(){
  var listControllersClient = new ROSLIB.Service({
    ros : ros,
    name : 'controller_manager/list_controllers',
    serviceType : 'controller_manager_msgs/ListControllers'
  });

  var request = new ROSLIB.ServiceRequest();

  listControllersClient.callService(request, function(result) {
    result.services.forEach(function(element) {
      var select = document.getElementById("controller-selector");
      var option = document.createElement("option");
      option.text = element;
      select.add(option);
    });
  });
}

/**
 * Converts the information retrieved from the knowledge base into a
 * Multi-agent Disjunctive Temporal Constraint Network With Uncertainty.
 * @param {string} skill - The name of the skill to plan for.
 * @param {string} planning_policy - The policy to adopt.
 */
function makePlan(skill, planning_policy){

  var makePlanClient = new ROSLIB.Service({
    ros : ros,
    name : '/planner/' + planning_policy,
    serviceType : 'franka_tut_msgs/CreatePlan'
  });

  var request = new ROSLIB.ServiceRequest({
    list_steps : [],
    list_constraints : []
  });

  $.getJSON($SCRIPT_ROOT + '/skills/steps', {
        skill_name: skill
      }, function(data) {
        data.steps.forEach(function(element){
          var select = document.getElementById("step-selector");
          var option = document.createElement("option");
          option.text = element;
          select.add(option);
          $.getJSON($SCRIPT_ROOT + '/endpoint/step/', {
                step_name: element
          }, function(data) {
            request.list_steps.push(new ROSLIB.Message({
              name : element,
              tasks : data.result[element]
            }));
            if (data.result['constraints'] !== '') {
              request.list_constraints.push(new ROSLIB.Message({
                a : data.result['constraints'],
                b : element
              }));
            }
          });
        });
  });

  setTimeout(function(){
    console.log(request);
    $("#demonstrate")[0].disabled = false;
    makePlanClient.callService(request, function(result) {
      console.log(result.valid);
    });
  }, 2000);
}



/* ##########################################################################
        LEARNING BY DEMONSTRATION
########################################################################## */

$('#demonstration-modal').on('shown.bs.modal', function (e) {
  var recordMotionClient = new ROSLIB.ActionClient({
    ros : ros,
    serverName : '/record_motion',
    actionName : 'franka_tut_msgs/RecordMotionAction'
  });

  var goal = new ROSLIB.Goal({
    actionClient : recordMotionClient,
    goalMessage : {
      skill: $( "#skill-selector option:selected" ).text(),
      name : $( "#step-selector option:selected" ).text()
    }
  });

  goal.on('feedback', function(feedback) {
    console.log('Feedback: ');
  });

  goal.on('result', function(result) {
    console.log('Final Result: ');
  });

  goal.send();
})

$('#demonstration-modal').on('hidden.bs.modal', function (e) {
  var signal = new ROSLIB.Message();
  var stopRecording = new ROSLIB.Topic({
    ros : ros,
    name : '/end_record_motion',
    messageType : 'std_msgs/Empty'
  });
  stopRecording.publish(signal);
})


$(document).on('keypress',function(e) {
    if(e.which == 13) {
        $('#send').click();
    }
    else if(e.which == 18){
      $("#text").blur();
      console.log("pause");
      $.getJSON(
        $SCRIPT_ROOT + '/plan/pause',
        function(data) {
            updateStateIndicator(data.state)
        }
      );
    }
});


/* ##########################################################################
        PROCESS DIALOGS
########################################################################## */

function say(message){
  var confirmation = new ROSLIB.Message({
    data : message
  });
  speech.publish(confirmation);
}

function processRequest(message){
  createDialog(message, 'user');
  $.getJSON($SCRIPT_ROOT + '/nlp/conversation/msg', {
    a: message
  }, function(data) {
      createDialog(data.answer, 'robot');
      // updateRobotState(data.new_state);
  })
  $("#text").val('');
  $("#text").focus();
}

function createDialog(msg, author) {
  var div = document.createElement("div");
  var a = document.createElement("a");
  var t = document.createTextNode(msg);
  if (author=='user'){
    div.className = 'balon1 p-2 m-0';
    a.className = 'float-right';
  } else {
    div.className = 'balon2 p-2 m-0';
    a.className = 'float-left sohbet2';
  }
  a.appendChild(t);
  div.appendChild(a);
  document.getElementById("sohbet").appendChild(div);
}

$('#send').bind('click', send);

var sendMessage = new ROSLIB.Topic({
  ros : ros,
  name : '/new_plan',
  messageType : 'std_msgs/String'
});

function send(){
  var new_plan_request = new ROSLIB.Message({
    data : $('input[name="text"]').val()
  });

  sendMessage.publish(new_plan_request);
}

/* ########################################################################## */
