;(function ($) {

    // Set the defaults
    var pluginName = 'EASDataTable',
        defaults = {
            dataTable_plugin: null,
            msg_your_draws: "",
            msg_search: "",
            msg_show: "Show",
            msg_entries: "entries"
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
            this.add_bootstrap();
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
        },

        add_bootstrap: function(){
            var $search_input = this.$element.find(".dataTables_filter input");
            // Remove the content of the label, and the label itself
            this.$element.find(".dataTables_filter label").contents().filter(function(){ return this.nodeType != 1; }).remove();
            $search_input.unwrap();

            $search_input.addClass("form-control");
            $search_input.prop("id","public-draw-search" );
            $search_input.prop("placeholder",this.options.msg_search );
            $search_input.parent().addClass("col-xs-12");
            $search_input.wrap( "<div class='input-group'></div>" );
            $search_input.after("<span class='input-group-btn'><button class='btn btn-default' type='button'><span class='fa fa-search'></span></button></span>");
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

    $.fn.outerHTML = function() {
      return jQuery('<div />').append(this.eq(0).clone()).html();
    };

})(window.jQuery, window, document );




