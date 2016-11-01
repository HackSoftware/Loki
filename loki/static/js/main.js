$(document).ready(function(){
  if($('[data-toggle="popover"]').length > 0) {
    $('[data-toggle="popover"]').popover({ trigger: "focus"});
  }

  var regQuestion = document.getElementsByClassName("reg-img-container")[0];
  var regError =  document.getElementById('error_1_id_password');

  if (typeof(regError) != 'undefined' && regError != null){
     $(regQuestion).css({"margin-top" : "-26px"});
  }

  $(".edit-profile .editable-user-avatar").click(function(){
    $("#div_id_full_image input[type='file']").click()
  })

  $(document).on("submit", ".change-interview-form", function(event) {
    if(!$(this).data('submitted')) {
      event.preventDefault();
      if(confirm('Сигурен ли си, че желаеш да смениш интервюто си?')) {
        $(this).data('submitted', true);
        $(this).submit();
      }
    }

  });

  $("#div_id_full_image input[type='file']").change(function(){
    var form = $(this).closest("form");
    form.find("[type='submit']").removeClass("btn-warning").addClass("btn-success").html("Saving...");
    form.submit();
  })

  $(".submit-solution").click(function(e){
    e.preventDefault();
    var code = $("#message-text").val();
    var task_id = $(this).closest(".submit-solution").attr("value");
    var csrftoken = Cookies.get('csrftoken');
    $.ajax({
      url: '/education/api/solution/',
      type: "POST",
      dataType: "json",
      data: {
        task: task_id,
        code: code
      },
      headers: {"X-CSRFToken": csrftoken},
      success: function(data) {
        $("#task-modal-box-" + task_id).modal('hide');
        var solution = data;
        $("#task-" + task_id).find('.last-solution-status').html('<img class="panda-loading-gif" src="/static/website_images/panda-loading.gif" />');
        if (solution.status) {
          pollForSolutionStatus(solution, updateSolutionStatus, task_id);
        }
      }
    });
  });

  function pollForSolutionStatus(solution, completeCb, taskId) {
    function poller(solution, completeCb) {
      setTimeout(function () {
        if (solution.hasOwnProperty('data')) {
          url = '/education/api/solution-status/' + solution.data('solution-id') + '/'
        } else {
          url = '/education/api/solution-status/' + solution.id + '/'
        }
        $.get(url, function(data) {
          if (data.status !== "pending" && data.status !== "submitted") {
            completeCb(solution, data, taskId);
          } else {
            poller(solution, completeCb);
          }
        })
      }, 1000);
    };

    poller(solution, completeCb);
  };

  var updateSolutionStatus = function(solution, new_data, taskId) {
    $("#task-" + taskId).find('.last-solution-status').html('<b>' + new_data.status + '</b>');
  }

  var complete = function(solution, new_data) {
    solution.text(new_data.status);
  }

  $('.solution-status').each(function() {
    var taskId = "";
    if ($(this).data('status') == 'pending') {
      pollForSolutionStatus($(this), complete, taskId);
    }
  });

  $(".check-in").click(function(){
    $(this).closest('.course-box').find('.check-in-table').toggle();
  });

});
