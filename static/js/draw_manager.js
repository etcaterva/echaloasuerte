;(function ($) {

    jQuery.fn.extend({

        /**
         * Cast the data contained in the input
         *
         * The type of data it's inferred from the input 'type' attribute, the classes it may have and the value itself
         * @returns {*} Returns the value casted (String, Integer, Bool or Array)
         */
        cast_input_value: function(){
            var type = this.attr("type");
            var value = this.val().replace( /\r?\n/g, "\r\n" ); // Avoid CRLF injection
            if (type == "number"){
                return parseInt(value, 10);
            }else if (type == "checkbox" ){
                // Non checked checkbox are not processed at all
                return true;
            }else if (type == "hidden" || type == "radio"){
                if (value == "True"){
                    return true;
                }else if (value == "False"){
                    return false;
                }else if (!isNaN(value)){
                        return parseInt(value, 10);
                } else {
                    return value;
                }
            } else if (this.hasClass('eas-tokenfield')){
                var items = value.split(',');
                console.log(items)
                return items;
                //return value;
            } else{
                return value;
            }
        },

        /**
         * Serialize the form into a JS object
         * @param excluded_fields An array of inputs which will be ignored
         * @returns {Object} The serialized form
         */
        serializeForm: function(excluded_fields) {
            var rsubmitterTypes = /^(?:submit|button|image|reset|file)$/i,
                rsubmittable = /^(?:input|select|textarea|keygen)/i,
                manipulation_rcheckableType = /^(?:checkbox|radio)$/i;

            var serialized_draw = {};
            var draw_object =  this.map(function(){
                // Can add propHook for "elements" to filter or add form elements
                var elements = jQuery.prop( this, "elements" );
                return elements ? jQuery.makeArray( elements ) : this;
            })
            .filter(function(){
                var type = this.type;
                return this.name && $.inArray(this.name, excluded_fields) < 0 &&
                    !jQuery( this ).is( ":disabled" ) && rsubmittable.test( this.nodeName ) &&
                    !rsubmitterTypes.test( type ) && ( this.checked || !manipulation_rcheckableType.test( type ) );
            })
            .map(function( i, elem ){
                var value = jQuery( this ).cast_input_value();
                return value == null ?
                    null :
                    { name: elem.name, value: value, type: elem.type };
            })
            .get();
            $.each(draw_object, function() {
                if (serialized_draw[this.name] === undefined) {
                    serialized_draw[this.name] = this.value;
                } else {
                    console.log("ERROR: Two inputs in the forms share the same name (" + this.name + ")");
                }
            });
            return serialized_draw;
        }
    });

    // Set the defaults
    var pluginName = 'DrawManager',
        defaults = {
            draw_type: null,
            is_shared: false,
            callback_render: null,
            callback_animate: null,
            url_toss: "",
            url_update: "",
            url_create: "",
            url_try: "",
            url_schedule_toss: "",
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

            // Record in 'edited_fields' when inputs are changed
            this.$element.find(":input").change(function() {
                var $this = $(this);
                that.edited_fields[$this.attr('name')] = $this.cast_input_value();
            });

            // Add toggle behaviour to show and hide "allow repeat" checkbox based on the number of results
            var toggle_allow_repeat = function (){
                if (that.$element.find('#id_number_of_results').val() > 1){
                    that.$element.find('#div_id_allow_repeat').removeClass('hidden');
                }else{
                    that.$element.find('#div_id_allow_repeat').addClass('hidden');
                }
            };
            $('#id_number_of_results').bind('keyup change', toggle_allow_repeat);
            toggle_allow_repeat();

            // Resize the title textarea based on the screen size
            autosize = function(){
                var max_width = $("#draw-title-container").width()*2/3;
                $("textarea.autogrow").width(max_width);
                $("textarea.autogrow").autoGrowInput({title:'{{ default_title }}',maxWidth: max_width,minWidth:30,comfortZone:30});
            };
            // Autosize the title box the first time
            autosize();
            // Autosize every time the window is resized
            $( window ).resize(function() {
                autosize();
            });

            // Initialize results' accordion
            $('#results').find('.accordion').accordion({
                collapsible: true,
                heightStyle: "content"
            });


            if (this.options.is_shared){
                // Initialize input to submit emails as a tokenFields
                $('input#invite-emails').tokenfield({
                    createTokensOnBlur:true,
                    delimiter: [',',' '],
                    inputType: 'email',
                    minWidth: 150
                });
            }
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

        /**
         * Toss the current draw and reload the page
         */
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

        /**
         * Attempt to create a shared draw.
         * If the draw is created successfully, the invitation methods are presented to the user.
         * If not, the errors are rendered on the form
         */
        publish: function(){
            var that = this;
            // Disable button to avoid duplicated submissions
            $('#publish').prop('disabled',true);

            this.create_draw(
                callback_done = function( data, textStatus, xhr ){
                    // Get the url to the draw
                    var url_draw_api = xhr.getResponseHeader('Location');
                    var url_draw_web = url_draw_api.replace(/api\/v[\d\.]+\//g,'');
                    // Present the link to the user
                    $('.url-share').val(url_draw_web);
                    // Set url to the FB share button
                    $('#share-fb-icon').attr('data-href', url_draw_web);
                    if (typeof FB !== 'undefined') { //refresh facebook items
                        FB.XFBML.parse();
                    }

                    // Set the link of the "Go to the draw" button
                    $('#go-to-draw').attr('href', url_draw_web);

                    // TODO Show next step in the creation
                    that.show_spread_step();
                },
                callback_fail = function () {
                    // TODO Error should be rendered manually here
                    that.try_draw();
                }
            );
        },

        /**
         * Attempt to create a normal draw.
         * If the draw is created it is automatically tossed and the results are presented
         * If not, the errors are rendered in the form
         */
        create_and_toss: function(){
            var that = this;
            // Disable button to avoid duplicated submissions
            $('#create-and-toss').prop('disabled',true);

            this.create_draw(
                callback_done = function( data, textStatus, xhr ){
                    // Get the url to the draw
                    var url_draw_api = xhr.getResponseHeader('Location');
                    var url_draw_web = url_draw_api.replace(/api\/v[\d\.]+\//g,'');
                    // TODO Could we just auto-toss in normal draws when they are created?
                    window.location.href = url_draw_web;
                },
                callback_fail = function (e) {
                    // TODO Error should be rendered manually here
                    that.try_draw();
                }
            );
        },

        /**
         * Creates a draw with the data from the current draw form
         *
         * @param callback_done Function executed if the creation success
         * @param callback_fail Function executed if the creation fails
         */
        create_draw: function(callback_done, callback_fail){
            // Serialize and clean the form
            var fields_skipped = ["csrfmiddlewaretoken", "_id"];
            var form_fields = $('#draw-form').serializeForm(fields_skipped);
            form_fields["type"] = this.options.draw_type;
            var data = JSON.stringify(form_fields);

            $.ajax({
                type : "POST",
                contentType : 'application/json',
                url: this.options.url_create,
                data: data
            })
            .done(callback_done)
            .fail(callback_fail);
        },

        /**
         * ONLY USED IN SHARED DRAWS
         * The draw is tried and the results are presented to the user (the draw is not saved in the server)
         */
        try_draw: function(){
            // Serialize and clean the draw form
            var excluded_fields = ["_id", "csrfmiddlewaretoken"];
            var form_fields = this.$element.serializeForm(excluded_fields);
            form_fields["type"] = this.options.draw_type;
            var data = JSON.stringify(form_fields);

            $.ajax({
                type : 'POST',
                contentType : 'application/json',
                url : this.options.url_try,
                data: data
            }).done(function( data ) {
                // TODO Results should be rendered properly
                var result = data.items;
                var result_cad = "Result: ";
                for (var i=0; i<result.length; i++){
                    result_cad += result[i] + ", ";
                }
                alert(result_cad);
            }).fail(function (e){
                // TODO Improve feedback
                console.log("ERROR: " + e.responseText);
            });
        },

        schedule_toss: function() {
            var schedule_timestamp = moment.utc(new Date($("#toss-schedule").val())).format();
            this.options.url_schedule_toss = this.options.url_schedule_toss.replace('ts_placeholder',schedule_timestamp);
            console.log(schedule_timestamp);
            $.ajax({
                type : 'POST',
                contentType : 'application/json',
                url : this.options.url_schedule_toss
            }).done(function (){
                // Here response should be rendered without reloading
                //window.location.reload();
                console.log("done")
            })
            .fail(function (e) {
                alert("There was an issue when scheduling the draw :(");
            });
        },

        /**
         * ONLY USED IN NORMAL DRAWS
         * Check whether the user has modified any field and if so the draw is updated in the server.
         * After that the draw is tossed
         */
        check_changes_and_toss: function(){
            var that = this;
            if (Object.keys(this.edited_fields).length > 0) {
                this.update(
                    callback_done = function (){
                        that.toss();
                    },
                    callback_fail = function (e) {
                        alert("Not edited" + e);
                    }
                );
            }else{
                that.toss();
            }
        },

        /**
         * ONLY USED IN SHARED DRAWS
         * Updates the current draw if there were any changes
         *
         * As a result, the page is always reloaded.
         */
        update_shared_draw: function(){
            if (Object.keys(this.edited_fields).length > 0) {
                this.update(
                    callback_done = function (){
                        // Don't use reload to avoid unintentional form submissions
                        window.location.href = String( window.location.href ).replace( "/#", "" );
                    },
                    callback_fail = function (e) {
                        alert("Not edited" + e);
                    }
                );
            }else{
                window.location.href = String( window.location.href ).replace( "/#", "" );
            }
        },

        /**
         * Updates the current draw.
         * Only the fields stored in 'this.edited_fields' are updated
         * 
         * @param callback_done Function executed if the update success
         * @param callback_fail Function executed if the update fails
         */
        update: function(callback_done, callback_fail){
                var edited_data = JSON.stringify(this.edited_fields);
                $.ajax({
                    type : 'PATCH',
                    contentType : 'application/json',
                    url : this.options.url_update,
                    data: edited_data
                })
                .done(callback_done)
                .fail(callback_fail);
        },

        /**
         * Show the spread step in the creation process of a shared draw
         */
        show_spread_step: function () {
            $('.step-configure').addClass('hidden');
            $('.step-spread').removeClass('hidden');
        },

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
