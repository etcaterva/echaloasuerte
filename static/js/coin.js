;(function ($) {

    // Set the defaults
    var pluginName = 'Coin',
        defaults = {
            base_url: null
        };

    /*********************************
     *     COIN CLASS DEFINITION
     ********************************/
    var Coin = function (element, options){
        this.init(element, options);
    };

    Coin.prototype = {
        constructor: Coin,
        image_store: [],
        animation_frame_counter: 0,
        result: null,

        init: function (element, options) {
            this.$element = $(element);
            this.options = $.extend({}, defaults, options);

            this.cache_images();
        },

        cache_images: function () {
            this.image_store[0] = new Image();
            this.image_store[0].src = this.options.base_url + "head.png";
            this.image_store[1] = new Image();
            this.image_store[1].src = this.options.base_url + "tail_dist.png";
            this.image_store[2] = new Image();
            this.image_store[2].src = this.options.base_url + "tail.png";
            this.image_store[3] = new Image();
            this.image_store[3].src = this.options.base_url + "head_dist.png";
            this.image_store[4] = new Image();
            this.image_store[4].src = this.options.base_url + "dist.png";
        },

        // Store the positions of the blurry images in order to show the animation
        blurry_images_array: [3, 4, 1, 4],

        animate: function(){
            var that = this;
            function animate_loop(){
                var image_frame = that.animation_frame_counter % that.blurry_images_array.length;
                that.$element.attr("src", that.image_store[that.blurry_images_array[image_frame]].src);
                that.animation_frame_counter++;
                if ((that.animation_frame_counter > 8) && (image_frame == that.result)) {
                    that.$element.attr("src", that.image_store[image_frame].src);
                } else {
                    setTimeout(animate_loop, 30);
                }
            }
            this.animation_frame_counter = 0;
            animate_loop();
        },

        flip: function(result){
            if (result == "head") {
                this.result = 0;  // (HEAD)
            } else {
                this.result = 2;  // (TAIL)
            }
            this.animate();
        }

    };

    /*********************************
     *   COIN PLUGIN DEFINITION
     ********************************/
    $.fn.coin = function (option, param) {
        return this.each(function () {
            var $this = $(this);
            var data = $this.data('plugin_' + pluginName);
            var options = typeof option == 'object' && option;

            if (typeof option === 'string') {
                data[option].apply(data, param);
            } else {
                if (!data && typeof option !== 'string' && !param) {
                    $this.data('plugin_' + pluginName, (new Coin(this, options)))
                }
            }
        })
    }

})(window.jQuery, window, document );
