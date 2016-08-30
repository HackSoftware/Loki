$(document).ready(function(){
    if($('[data-toggle="popover"]').length > 0) {
      $('[data-toggle="popover"]').popover({ trigger: "focus"});
    }

    var regQuestion = document.getElementsByClassName("reg-img-container")[0];
    var regError =  document.getElementById('error_1_id_password');

    if (typeof(regError) != 'undefined' && regError != null){s
       $(regQuestion).css({"margin-top" : "-26px"});
    }

    $(".edit-profile .editable-user-avatar").click(function(){
      $("#div_id_full_image input[type='file']").click()
    })

    $("#div_id_full_image input[type='file']").change(function(){
      var form = $(this).closest("form");
      form.find("[type='submit']").removeClass("btn-warning").addClass("btn-success").html("Saving...");
      form.submit();
    })
});
