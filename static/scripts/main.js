$(function () {
  var $messageCloseButtons = $('.message .close-button');

  $messageCloseButtons.show();

  $messageCloseButtons.on('click', function () {
    $(this).parent().hide();
  });
});
