;(function ($) {

    // Set the defaults
    var pluginName = 'EASSlideSelector',
        defaults = {
            url_send_message: "",
            url_get_messages: "",
            draw_id: ""
        };

    /*********************************
     *     SLIDESELECTOR CLASS DEFINITION
     ********************************/
    var SlideSelector = function (element, options){
        this.init(element, options);
    };

    SlideSelector.prototype = {

        constructor: SlideSelector,

        test: function() {
            console.log("testtt");
        },

        init: function (element, options){
            var that = this
            this.$element = $(element);
            this.options = $.extend( {}, defaults, options) ;
            this.width = this.$element.find('.slide-bar').width();
            this.relative_pos_selector = 0;

            this.renderUI();

            $('#extra-password').hide();
            $('#extra-invited').hide();
            this.$element.find( ".slider-selector" ).draggable({axis: "x", containment: "parent"});
            this.$element.find('.slide-bar').click(function(e) {
                var $slidebar = $(this);
                that.$element.find('.slider-selector').stop(true,true);
                that.width = $slidebar.width();
                var pos_slide_bar = $slidebar.offset().left;
                var pos_selector = $('.slider-selector').offset().left;
                var relative_pos_click = e.pageX - pos_slide_bar;
                that.relative_pos_selector = pos_selector - pos_slide_bar;
                if (relative_pos_click < that.width/4){
                    that.select_everyone();
                }else{
                    if (relative_pos_click > 3*that.width/4){
                        that.select_invited();
                    }else {
                        that.select_password();
                    }
                }
            });
        },

        select_everyone: function (no_animation){
            if (no_animation ) {
                this.$element.find('.slider-selector').css({'left': '0%'});
            }else{
                var move = this.relative_pos_selector + 10;
                this.$element.find('.slider-selector').animate({"left": "-="+move+"px"}, "slow");
            }
            this.$element.find('.slide-bar').attr("data-selected","everyone");
            $('#restriction-everyone').stop(true,true).addClass('restriction-selected', 200);
            $('#restriction-password').stop(true,true).removeClass('restriction-selected', 200);
            $('#restriction-invited').stop(true,true).removeClass('restriction-selected', 200);
            $('#extra-password').hide();
            $('#extra-invited').hide();
            $('#extra-everyone').show();
        },

        select_password: function (no_animation){
            if (no_animation ) {
                $('.slider-selector').css({'left': '50%'});
            }else{
                var move = this.width/2 - this.relative_pos_selector - 10;
                $('.slider-selector').animate({"left": "+="+move+"px"}, "slow");
            }
            $('.slide-bar').attr("data-selected","password");
            $('#restriction-everyone').stop(true,true).removeClass('restriction-selected', 200);
            $('#restriction-password').stop(true,true).addClass('restriction-selected', 200);
            $('#restriction-invited').stop(true,true).removeClass('restriction-selected', 200);

            $('#extra-everyone').hide();
            $('#extra-invited').hide();
            $('#extra-password').show();

        },

        select_invited: function (no_animation){
            if (no_animation ) {
                $('.slider-selector').css({'left': '100%'});
            }else{
                var move = this.width - this.relative_pos_selector - 10;
                $('.slider-selector').animate({"left": "+="+move+"px"}, "slow");
            }
            $('.slide-bar').attr("data-selected","invited");
            $('#restriction-everyone').stop(true,true).removeClass('restriction-selected', 200);
            $('#restriction-password').stop(true,true).removeClass('restriction-selected', 200);
            $('#restriction-invited').stop(true,true).addClass('restriction-selected', 200);
            $('#extra-everyone').hide();
            $('#extra-password').hide();
            $('#extra-invited').show();
        },

        // Render the elements for the UI
        renderUI: function (){
            var html = '<div data-selected="everyone" class="slide-bar ui-widget-content">' +
                            '<div class="slider-tick position-1"></div>' +
                            '<div class="slider-tick position-2"></div>' +
                            '<div class="slider-tick position-3"></div>' +
                            '<div class="slider-selector" ></div>' +
                        '</div>';
            this.$element.append(html);
        }
    };

    /*********************************
     *     SLIDESELECTOR PLUGIN DEFINITION
     ********************************/
    $.fn.slideSelector = function (option, param) {
        this.each(function () {
            var $this = $(this)
                , data = $this.data('plugin_' + pluginName)
                , options = typeof option == 'object' && option

            if (typeof option === 'string') {
                data[option].apply(data, ['no_animation'])
            } else {
                if (!data && typeof option !== 'string' && !param) {
                    $this.data('plugin_' + pluginName, (new SlideSelector(this, options)))
                }
            }
        })
    }

})(window.jQuery, window, document );




