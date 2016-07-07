$(function() {
  $('.progress-bar').each(function() {
    var bar_value = $(this).attr('aria-valuenow') + '%';
     $(this).css('width', bar_value);
  });
});