;(function ($) {

    jQuery.fn.extend({
        cast_input_value: function(){
            var type = this.attr("type");
            var value = this.val();
            console.log(type + " - " + value);
            if (type == "number"){
                return parseInt(value, 10);
            }else{
                if (type == "checkbox" ){
                    // Non checked checkbox are not processed at all
                    return true;
                }else{
                    if (type == "hidden" || type == "radio"){
                        if (value == "True"){
                            return true;
                        }else{
                            if (value == "False"){
                                return false;
                            }else{
                                if (!isNaN(value)){
                                    return parseInt(value, 10);
                                }
                                else{
                                    return value;
                                }
                            }
                        }
                    }
                }
            }
        }
    });

    // Set the defaults
    var pluginName = 'DrawManager',
        defaults = {
            is_shared: false,
            callback_render: null,
            callback_animate: null,
            url_toss: "",
            url_update: "",
            msg_result: "Result",
            msg_generated_on: "generated on"
        };


    /*********************************
     *     DRAW MANAGER CLASS DEFINITION
     ********************************/
    var DrawManager = function (element, options){
        this.init(element, options);
    };

    DrawManager.prototype = {

        constructor: DrawManager,

        edited_fields: {},


        init: function (element, options) {
            var that = this;
            this.$element = $(element);
            this.options = $.extend({}, defaults, options);

            $("#draw-form").find(":input").change(function() {
                var $this = $(this);
                that.edited_fields[$this.attr('name')] = $this.cast_input_value();
            });
        },

        add_result: function (result){
            var $results = $('#results').find('.accordion');

            // Add the new result to the accordion
            var result_html =   '<p class="h3">' + this.options.msg_result +
                                '       <small class="result-timestamp hidden-xs">' +
                                '       ' + this.options.msg_generated_on + ' ' + result.datetime +
                                '   </small>' +
                                '</p>' +
                                '<div class="result">';
            result_html += this.options.callback_render(result.items) + '</div>';
            $results.prepend(result_html);
            $results.accordion('refresh');

            // Open the new result in the accordion
            $results.accordion({active:0});

            // Animate the result when necessary
            if (this.options.callback_animate){
                this.options.callback_animate(result.items);
            }
        },

        toss: function(){
            $.ajax({
                method : "POST",
                url : this.options.url_toss
            }).done(function (){
                // Here results should be rendered without reloading
                window.location.reload();
            })
            .fail(function () {
                alert("{% trans 'There was an issue when tossing the draw :(' %}");
            });
        },

        check_changes_and_toss: function(){
            var that = this;
            if (Object.keys(this.edited_fields).length > 0) {
                console.log(this.edited_fields);
                var edited_data = JSON.stringify(this.edited_fields);
                console.log(edited_data);
                $.ajax({
                    type : 'PATCH',
                    contentType : 'application/json',
                    url : this.options.url_update,
                    data: edited_data
                }).done(function (){
                    that.toss();
                })
                .fail(function (e) {
                    alert("Not edited" + e);
                });
            }else{
                that.toss();
            }
        },

        update: function(){

        },

        // Serialize a form to a JS object
        serializeForm: function(fields_skipped) {
            var that = this;
            var rCRLF = /\r?\n/g,
                rsubmitterTypes = /^(?:submit|button|image|reset|file)$/i,
                rsubmittable = /^(?:input|select|textarea|keygen)/i,
                manipulation_rcheckableType = /^(?:checkbox|radio)$/i;
            var serialized_draw = {};
            var draw_form = $("#draw-form");
            var draw_object =  draw_form.map(function(){
                // Can add propHook for "elements" to filter or add form elements
                var elements = jQuery.prop( this, "elements" );
                return elements ? jQuery.makeArray( elements ) : this;
            })
            .filter(function(){
                var type = this.type;

                return this.name && $.inArray(this.name, fields_skipped) < 0 && $.inArray(this.name, fields_skipped) &&
                    !jQuery( this ).is( ":disabled" ) && rsubmittable.test( this.nodeName ) &&
                    !rsubmitterTypes.test( type ) && ( this.checked || !manipulation_rcheckableType.test( type ) );
            })
            .map(function( i, elem ){
                var input_value = jQuery( this ).val().replace( rCRLF, "\r\n" );
                var value;
                var type = elem.type;
                console.log("type: "+ that.infer_data_type(type,input_value));
                if (type == "number"){
                    value = parseInt(input_value, 10);
                }else{
                    if (type == "checkbox" ){
                        value = true;
                    }else{
                        if (type == "hidden" || type == "radio"){
                            if (input_value == "True"){
                                value = true;
                            }else{
                                if (input_value == "False"){
                                    value = false;
                                }else{
                                    if (!isNaN(input_value)){
                                        value = parseInt(input_value, 10);
                                    }
                                    else{
                                        value = input_value;
                                    }
                                }
                            }
                        }
                    }
                }
                return value == null ?
                    null :
                    jQuery.isArray( value ) ?
                        jQuery.map( value, function( value ){
                            return { name: elem.name, value: value, type: elem.type };
                        }) :
                        { name: elem.name, value: value, type: elem.type };
            })
            .get();
            $.each(draw_object, function() {
                if (serialized_draw[this.name] === undefined) {
                    serialized_draw[this.name] = this.value;
                } else {
                    console.log("ERROR: Two inputs in the forms share the same name");
                }
            });
            return serialized_draw;
        }

        
    };

    /*********************************
     *   DRAW MANAGER PLUGIN DEFINITION
     ********************************/
    $.fn.drawManager = function (option, param) {
        return this.each(function () {
            var $this = $(this)
                , data = $this.data('plugin_' + pluginName)
                , options = typeof option == 'object' && option

            if (typeof option === 'string') {
                data[option].apply(data)
            } else {
                if (!data && typeof option !== 'string' && !param) {
                    $this.data('plugin_' + pluginName, (new DrawManager(this, options)))
                }
            }
        })
    }

})(window.jQuery, window, document );
