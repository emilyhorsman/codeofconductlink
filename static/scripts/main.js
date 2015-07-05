$(function () {
    var $messageCloseButtons = $('.message .close-button');

    $messageCloseButtons.css('visibility', 'visible');

    $messageCloseButtons.on('click', function () {
        $(this).parent().hide();
    });

    var hover_icon = function() {
        var old_class = $(this).attr('class');
        $(this).attr('class', $(this).data('hover'));
        $(this).data('hover', old_class);
    };

    $('a[rel="external"]').hover(function() {
        var hover_elements = $(this).find('[data-hover]');
        if (hover_elements.length > 0) {
            hover_icon.call(hover_elements);
        }
    });
});
