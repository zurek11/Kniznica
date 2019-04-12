$(function() {
  $('.datetimepicker').datetimepicker();

  $('.datetimepicker-addon').on('click', function() {
  	$(this).prev('input.datetimepicker').data('DateTimePicker').toggle();
  });
});

$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
});
