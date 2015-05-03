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
            var html_search_input = '<div class="input-group">' +
                                        '<input id="public-draw-search" class="form-control" type="text" placeholder="' + this.options.msg_search + '">' +
                                        '<span class="input-group-btn"><button class="btn btn-default" type="button"><span class="fa fa-search"></span></button></span>';
            this.$element.find('#public-draws_filter').empty();
            this.$element.find('#public-draws_filter').append(html_search_input);

            // Select input to choose the number of results
            var html_select = this.$element.find('select').outerHTML();
            html_select =  '<label for="inputKey" class="col-md-1 control-label">Show</label>' +
                            '<label id="entry-label" for="inputKey" class="col-md-1 control-label">entries</label>' +
                            '<div class="col-md-10"> ' + html_select + '</div>';

            console.log(html_select);
            this.$element.find('.dataTables_length').empty();
            this.$element.find('.dataTables_length').append(html_select);
            this.$element.find('.dataTables_length').append('<p class="form-control-static"></p>');
            this.$element.find('select').addClass("form-control");
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




