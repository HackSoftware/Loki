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

  $(".submit-dialog-btn").click(function(){
    var task = $(this).parent().parent();
  });

  $('#task-modal-box').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var taskName = button.data('task-name');
    var modal = $(this);
    modal.find('.modal-title').text(taskName);

    window.modalTriggerButton = button;
    var task_id = button.data("task-id");
    $("#submit-solution").val(task_id);
  });

  $("#submit-solution").click(function(e){
    e.preventDefault();
    var code = $("#message-text").val();
    var task_id = $("#submit-solution").attr("value");
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
        $("#task-modal-box").modal('hide');
        var solution = data;
        window.modalTriggerButton.parent().parent().find('.last-solution-status').html('<img class="panda-loading-gif" src="/static/website_images/panda-loading.gif" />');
        if (solution.status) {
          pollForSolutionStatus(solution, updateSolutionStatus);
        }
      }
    });
  });

  function pollForSolutionStatus(solution, completeCb) {
    function poller(solution, completeCb) {
      setTimeout(function () {
        if (solution.hasOwnProperty('data')) {
          url = '/education/api/solution-status/' + solution.data('solution-id') + '/'
        } else {
          url = '/education/api/solution-status/' + solution.id + '/'
        }
        $.get(url, function(data) {
          if (data.status !== "pending" && data.status !== "submitted") {
            completeCb(solution, data);
          } else {
            poller(solution, completeCb);
          }
        })
      }, 1000);
    };

    poller(solution, completeCb);
  };

  var updateSolutionStatus = function(solution, new_data) {
    window.modalTriggerButton.parent().parent().find('.last-solution-status').html('<b>' + new_data.status + '</b>');
  }

  var complete = function(solution, new_data) {
    solution.text(new_data.status);
  }

  $('.solution-status').each(function() {
    if ($(this).data('status') == 'pending') {
      pollForSolutionStatus($(this), complete);
    }
  });

  $(".check-in").click(function(){
    $(this).closest('.course-box').find('.check-in-table').toggle();
  });

});
