(function($){

    $.fn.autoGrowInput = function(o) {

        o = $.extend({
            numRows: 1,
            maxWidth: 100,
            minWidth: 30,
            comfortZone: 7000,
            title: "Draw"
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
                        if (newWidth < 2*o.maxWidth){
                            input.prop('rows', 2);
                        }else{ // The title can have maximum 3 rows
                            input.prop('rows', 3);
                        }
                    }

                };

            testSubject.insertAfter(input);
            $(this).off('keyup');
            $(this).off('keydown');
            $(this).off('update');
            $(this).bind('keyup keydown update', check);
            $(this).focus(function() {
                var is_protected = $(this).hasClass('protected');
                if (!is_protected && $(this).val() == o.title )
                    $(this).val('');
            });
            $(this).blur(function() {
                if ($(this).val() == '') {
                    $(this).val(o.title);
                }
                var max_width = $("#draw-title-container").width();
                $(this).width(max_width);
                check()
            });
            $(this).blur();
        });

        return this;

    };

})(jQuery);