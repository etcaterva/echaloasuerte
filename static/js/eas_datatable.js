;(function ($) {

    // Set the defaults
    var pluginName = 'EASDataTable',
        defaults = {
            dataTable_plugin: null,
            msg_your_draws: ""
        };

    /*********************************
     *     SLIDESELECTOR CLASS DEFINITION
     ********************************/
    var EASDataTable = function (element, options){
        this.init(element, options);
    };

    EASDataTable.prototype = {

        constructor: EASDataTable,

        init: function (element, options){
            var that = this;
            this.$element = $(element);
            this.options = $.extend( {}, defaults, options) ;

            this.checkbox_filter_your_draws();
        },

        checkbox_filter_your_draws: function(){
            var that = this;
            // Render checkbox and label
            var html_only_my_draws = '<div class="checkbox"><label><input id="only-your-draws" type="checkbox">' +
                            this.options.msg_your_draws + '</label></div>';
            this.$element.find('.dataTables_length').append(html_only_my_draws);

            // Set the action of the checkbox
            this.$element.find('#only-your-draws').click(function(){
                if ($(this).prop('checked')){
                    that.options.dataTable_plugin.column(5).search("y").draw();
                } else{
                    that.options.dataTable_plugin.column(5).search("").draw();
                }
            });
        }
    };

    /*********************************
     *     SLIDESELECTOR PLUGIN DEFINITION
     ********************************/
    $.fn.easDataTable = function (option, param) {
        this.each(function () {
            var $this = $(this)
                , data = $this.data('plugin_' + pluginName)
                , options = typeof option == 'object' && option

            if (typeof option === 'string') {
                data[option].apply(data, ['no_animation'])
            } else {
                if (!data && typeof option !== 'string' && !param) {
                    $this.data('plugin_' + pluginName, (new EASDataTable(this, options)))
                }
            }
        })
    }

})(window.jQuery, window, document );




