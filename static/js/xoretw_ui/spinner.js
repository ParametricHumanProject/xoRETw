(function ($) {
  $('.spinner .btn:first-of-type').on('click', function() {
    $('.spinner input').val( parseInt($('.spinner input').val(), 10) + 1);
  });
  $('.spinner .btn:last-of-type').on('click', function() {
    $('.spinner input').val( parseInt($('.spinner input').val(), 10) - 1);
  });

  $('.spinner2 .btn:first-of-type').on('click', function() {
    $('.spinner2 input').val( parseInt($('.spinner2 input').val(), 10) + 1);
  });
  $('.spinner2 .btn:last-of-type').on('click', function() {
    $('.spinner2 input').val( parseInt($('.spinner2 input').val(), 10) - 1);
  });

})(jQuery);
