;(function ($) {

    // Set the defaults
    var pluginName = 'EASFavourites',
        defaults = {
            url_add: "",
            url_remove: "",
            user_authenticated: false,
            draw_id: "",
            path_img_star: "",
            path_img_star_empty: "",
            msg_regsiter: "",
            msg_toss: ""
        };

    /*********************************
     *     FAVOURITES CLASS DEFINITION
     ********************************/
    var FavoritesManager = function (element, options){
        this.init(element, options);
    };

    FavoritesManager.prototype = {

        constructor: FavoritesManager,

        init: function (element, options) {
            var that = this
            this.$element = $(element);
            this.options = $.extend({}, defaults, options);
            this.$element.click(function () {
                if (that.options.user_authenticated == false) {
                    alert("You need an account to save your favourite draws");
                } else {
                    if (that.options.draw_id == 'None') {
                        alert("Click on the 'Toss' button to try the draw first");
                    } else {
                        var is_fav = (that.$element.attr("data-active") == "y");
                        var $fav_image = that.$element.find('img');
                        var $fav_loading = that.$element.find('#fav-loading');
                        $fav_image.addClass("hidden");
                        $fav_loading.removeClass("hidden");
                        if (is_fav) {
                            $.ajax({
                                method : "DELETE",
                                contentType : 'application/json',
                                url : that.options.url_remove
                            }).done(function (){
                                that.$element.attr("data-active", "n");
                                that.$element.find('img').attr("src", that.options.path_img_star_empty);
                                $fav_loading.addClass("hidden");
                                $fav_image.removeClass("hidden");
                                that.remove_from_favorite_panel();
                            });
                        } else {
                            $.ajax({
                                method : "POST",
                                contentType : 'application/json',
                                data: JSON.stringify({
                                    id: that.options.draw_id
                                }),
                                url : that.options.url_add
                            }).done(function (){
                                that.$element.attr("data-active", "y");
                                that.$element.find('img').attr("src", that.options.path_img_star);
                                $fav_loading.addClass("hidden");
                                $fav_image.removeClass("hidden");
                                that.options.title = $('#draw-title-container textarea').val();
                                that.add_to_favorite_panel();
                            });
                        }
                    }
                }
            });
        },

        add_to_favorite_panel: function (){
            // Hide the "favourites empty" label in case it was rendered
            $('span#favourites-empty').hide();
            this.render_favourite_line();
        },

        remove_from_favorite_panel: function(){
            // Show the "favourites empty" label in case it was rendered
            $('span#favourites-empty').show();
            // Remove the draw from the favourites section
            $('a[href*="' + this.options.draw_id + '"]').remove();
        },

        render_favourite_line: function(){
            var html =  ' <a href="/draw/' + this.options.draw_id + '/">' +
                    ' <li> ' + this.options.title + ' | now </li>' +
                    ' </a>';
            $('#favourites-panel ul').append(html);
        }
    };

    /*********************************
     *     FAVOURITES PLUGIN DEFINITION
     ********************************/
    $.fn.favourites = function (option, param) {
        return this.each(function () {
            var $this = $(this)
                , data = $this.data('plugin_' + pluginName)
                , options = typeof option == 'object' && option

            if (typeof option === 'string') {
                data[option].apply(data)
            } else {
                if (!data && typeof option !== 'string' && !param) {
                    $this.data('plugin_' + pluginName, (new FavoritesManager(this, options)))
                }
            }
        })
    }

})(window.jQuery, window, document );
