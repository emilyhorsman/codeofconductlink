$(function () {
  var $messageCloseButtons = $('.message .close-button');

  $messageCloseButtons.css('visibility', 'visible');

  $messageCloseButtons.on('click', function () {
    $(this).parent().hide();
  });
});
