;(function ($) {

    // Set the defaults
    var pluginName = 'EASDataTable',
        defaults = {
            type: "profile", // Can be "profile" or "public_draw"
            dataTable_plugin: null,
            msg_your_draws: "",
            msg_search: ""
        };

    /*********************************
     *     EASDATATABLE CLASS DEFINITION
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

            if (this.options.type == "public_draw" ){
                this.checkbox_filter_your_draws();
            }
            else{ // Then is the datatable for the profile
                this.checkbox_filter_public_draws();
            }
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
                var dataTable = that.options.dataTable_plugin.api();
                if ($(this).prop('checked')){
                    dataTable.column(5).search("y").draw();
                } else{
                    dataTable.column(5).search("").draw();
                }
            });
        },

        checkbox_filter_public_draws: function(){
            var that = this;
            // Render checkbox and label
            var html_only_public_draws = '<div class="checkbox"><label><input id="only-public-draws" type="checkbox">' +
                            this.options.msg_your_draws + '</label></div>';
            var $el = this.$element.find('.dataTables_length');
            $el.append(html_only_public_draws);

            // Set the action of the checkbox
            this.$element.find('#only-public-draws').click(function(){
                var dataTable = that.options.dataTable_plugin.api();
                if ($(this).prop('checked')){
                    dataTable.column(4).search("y").draw();
                } else{
                    dataTable.column(4).search("").draw();
                }
            });
        },

        add_bootstrap: function(){
            var $search_input = this.$element.find(".dataTables_filter input");
            // Remove the content of the label, and the label itself
            this.$element.find(".dataTables_filter label").contents().filter(function(){ return this.nodeType != 1; }).remove();
            $search_input.unwrap();
            $search_input.addClass("form-control");
            $search_input.prop("id","search-draw" );
            $search_input.prop("placeholder",this.options.msg_search );
            $search_input.parent().addClass("col-xs-12");
            $search_input.wrap( "<div class='input-group'></div>" );
            $search_input.before("<span class='input-group-addon'><span class='fa fa-search'></span></span>");
        }
    };

    /*********************************
     *     EASDATATABLE PLUGIN DEFINITION
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




