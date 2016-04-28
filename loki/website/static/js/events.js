$('.teacher-avatar').click(function(teacher){
  var teacherId = '#teacher-' + $(this).data('teacherid')
  $('.teacher-info').css('display', 'none');
  $('.glyphicon-chevron-down').css('display', 'none');
  $('.glyphicon-chevron-right').css('display', 'inline');
  $('.course-teacher-image').find('img').removeClass('active-teacher-image');
  $(this).find(".glyphicon-chevron-right").css('display', 'none');
  $(this).find(".glyphicon-chevron-down").css('display', 'inline');
  $(this).find("img").addClass('active-teacher-image');
  $('.teacher-info-container').removeClass('active-teacher-info');
  $(this).find('.teacher-info-container').addClass('active-teacher-info');
  $(teacherId).css('display', 'block');
})