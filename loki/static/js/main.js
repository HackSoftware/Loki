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

    // Add task_id to the form
    var task_id = button.data("task-id");
    $(".modal form input[name='task_id']").val(task_id);
  });
});
