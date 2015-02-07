(function($){

    $.fn.autoGrowInput = function(o) {

        o = $.extend({
            maxWidth: 100,
            minWidth: 30,
            comfortZone: 7000,
            title: "Default title"
        }, o);

        this.filter('textarea').each(function(){

            var minWidth = o.minWidth || $(this).width(),
                val = '',
                input = $(this),
                testSubject = $('<tester/>').css({
                    position: 'absolute',
                    top: -9999,
                    left: -9999,
                    width: 'auto',
                    fontSize: input.css('fontSize'),
                    fontFamily: input.css('fontFamily'),
                    fontWeight: input.css('fontWeight'),
                    letterSpacing: input.css('letterSpacing'),
                    whiteSpace: 'nowrap'
                }),
                check = function() {
                    if (val === (val = input.val())) {return;}
                     console.log("js: " + o.maxWidth);
                    // Enter new content into testSubject
                    var escaped = val.replace(/&/g, '&amp;').replace(/\s/g,'&nbsp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                    testSubject.html(escaped);

                    // Calculate new width + whether to change
                    var testerWidth = testSubject.width(),
                        newWidth = (testerWidth + o.comfortZone) >= minWidth ? testerWidth + o.comfortZone : minWidth,
                        currentWidth = input.width(),
                        isValidWidthChange = (newWidth < currentWidth && newWidth >= minWidth)
                                             || (newWidth > minWidth && newWidth < o.maxWidth);

                    // Animate width
                    if (isValidWidthChange) {
                        input.width(newWidth);
                        input.prop('rows', 1);
                    }
                    else{
                        input.prop('rows', 2);
                    }

                };

            testSubject.insertAfter(input);
            $(this).off('keyup');
            $(this).off('keydown');
            $(this).off('update');
            $(this).bind('keyup keydown update', check);
            $(this).focus(function() {
                if ($(this).val() == o.title)
                    $(this).attr("size", 3);
                    $(this).val('');
            });
            $(this).blur(function() {
                if ($(this).val() == '')
                    $(this).val(o.title);
                    var max_width = $("#draw-title-container").width()*2/3;
                    $(this).width(max_width);
            });

        });

        return this;

    };

})(jQuery);