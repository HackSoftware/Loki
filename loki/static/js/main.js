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
    var el = $(this);
    el.attr("disabled","disabled");
    e.preventDefault();
    var code = $(this).parents(".modal-content").find("textarea.message-text").val();
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
        el.removeAttr("disabled");
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
    $("#solution-task-id-" + taskId).find('.no-solutions').html("");
    $("#solution-task-id-" + taskId).find('.task-solution-link').html('<button class="btn btn-warning" id="btn-tasks-link">Решения</button>');
    var $taskRow = $("#task-" + taskId);

    if (new_data.status == 'ok') {
      $taskRow.find('.last-solution-status').html('<span class="pass-status-solution"><b>PASS</b> </span>');
    } else if (new_data.status == 'not_ok'){
      $taskRow.find('.last-solution-status').html('<span class="fail-status-solution"><b>FAIL</b> </span>');
    } else {
      $taskRow.find('.last-solution-status').html('<b>' + new_data.status + '</b>');
      }
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

  $(".student-note").click(function(){
    $(this).closest('.student-box').find('.student-notes-table').toggle();
  });

  $(".student-presence-percent").each(function(){
    var percent = parseInt($(this).html())/100;
    $(this).css("color", "rgb(" + Math.floor(255 * (1-percent)) + "," + Math.floor(255 * percent) + ",0)");
  });

  $('#id_company').selectize({
      create: true,
      persist: false,
      sortField: 'text',
      placeholder: 'Избери компания...'
  });

});
