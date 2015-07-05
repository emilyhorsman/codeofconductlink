$(function () {
    var $messageCloseButtons = $('.message .close-button');

    $messageCloseButtons.css('visibility', 'visible');

    $messageCloseButtons.on('click', function () {
        $(this).parent().hide();
    });

    var hover_icon = function() {
        if (!$(this).data('hover'))
            return;

        var old_class = $(this).attr('class');
        $(this).attr('class', $(this).data('hover'));
        $(this).data('hover', old_class);
    };

    $('a[rel="external"]').hover(function() {
        hover_icon.call($(this).find('[data-hover]'));
    });
});
