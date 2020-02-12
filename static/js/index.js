$('#tabs nav').hide();
$('.tab-content').hide();

$('#tabs a:first').addClass('active');

$('#tabs a').click(function(event) {
  $('#tabs a').removeClass('active');
  $(this).addClass('active');
  $('.tab-content').hide();

  var selectTab = $(this).attr("href");

  $(selectTab).fadeIn();
});

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

function dismiss_alert(){
  setTimeout(function(){
    $(".alert")[0].classList = ["alert fade"];
  }, 2000);
}

$('#hide-connect').bind('click', function(e) {
    if ($("#hide-connect")[0].innerHTML == "Hide") {
      $("#hide-connect")[0].innerHTML = "Show connection tab";
    } else {
       $("#hide-connect")[0].innerHTML = "Hide";
    }
});

$('#connect').bind('click', function(e) {
    e.preventDefault();
    setTimeout(function(){
      $.getJSON($SCRIPT_ROOT + '/robot', function(data) {
          if (data.url != ""){
            alert_success();
            $('#tabs nav').show();
            $('.tab-content:first').show();
            updatePlanningPolicies();
            updateControllerList();
          } else {
            alert_failure();
          }
      });
    }, 1000);
});

$('#camera').bind('click', function(e) {
  window.open('/camera');
});

$('#planner').bind('click', function(e) {
    e.preventDefault();
    $.getJSON($SCRIPT_ROOT + '/robot', function(data) {
        if (data.url != ""){
          makePlan($( "#skill-selector option:selected" ).text(), $( "#policy-selector option:selected" ).text());
          $("#visualize")[0].disabled = false;
          $("#visualize")[0].classList = ["btn btn-primary"];
          $("#execute")[0].disabled = false;
          $("#execute")[0].classList = ["btn btn-primary"];
        }
    });
});

$('#visualize').bind('click', function(e) {
    var cmdVis = new ROSLIB.Topic({
      ros : ros,
      name : '/visualize_plan',
      messageType : 'std_msgs/Empty'
    });

    var signal = new ROSLIB.Message({});
    cmdVis.publish(signal);
});

$('#execute').bind('click', function(e) {
    var cmdExec = new ROSLIB.Topic({
      ros : ros,
      name : '/execute_plan',
      messageType : 'std_msgs/Empty'
    });

    var signal = new ROSLIB.Message({});
    cmdExec.publish(signal);
});

$.getJSON($SCRIPT_ROOT + '/robot', function(data) {
    if (data.url != ""){
      $('#tabs nav').show();
      $('.tab-content:first').show();
    }
});
