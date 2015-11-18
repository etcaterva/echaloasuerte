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
                return this.prop( "checked");
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
                return value.split(',');
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
                if (value != null){
                    return { name: elem.name, value: value, type: elem.type };
                }else{
                    return null;
                }
            })
            .get();
            $.each(draw_object, function() {
                var regex_set = /^set_[0-9]/i;
                if (regex_set.test(this.name)){
                    if (serialized_draw['sets'] === undefined){
                        serialized_draw['sets'] = [];
                    }
                    serialized_draw['sets'].push(this.value);
                }else if (serialized_draw[this.name] === undefined) {
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

        /**
         * Store callback functions to render results dynamically
         * render: Specify how to render the result
         * animate: Optional function. Only needed in case it needs animation (i.e. roll dice)
         */
        draw_callbacks: {
            'dice': {
                'render': function(results){
                    return D6.render_dice(results.length);
                },
                'animate': function(results){
                    D6.roll(results);
                }
            },
            'card': {
                'render': function(results){
                    return Card.draw(results);
                }
            },
            'coin': {
                'render': function(result){
                    return result;
                },
                'animate': function(result){
                    $('#img-coin').coin('flip', result);
                }
            },
            'number': {
                'render': function(results){
                    var html = '<ul class="list-group">';
                        for (var res in results){
                            html += '<li class="list-group-item">' + results[res] + '</li>';
                        }
                    html += '</ul>';
                    return html;
                }
            },
            'letter': {
                'render': function(results){
                    var html = '<ul class="list-group">';
                        for (var res in results){
                            html += '<li class="list-group-item">' + results[res] + '</li>';
                        }
                    html += '</ul>';
                    return html;
                }
            },
            'tournament': {
                'render': function(_){
                    return '<div id="bracket-result"></div>';
                },
                'animate': function (results) {
                    function cleanBracketDisplay(){
                        $('.team .label').css('color', 'black')
                                        .css('text-align','left')
                                        .css('position','relative');
                        $('.jQBracket .tools span').css('display','none');
                    }

                    $('#bracket-result').bracket({
                        init: {teams: results},
                        save: cleanBracketDisplay,
                    });
                    $('.result').css('height','auto','important');
                    cleanBracketDisplay();
                }
            },
            'item': {
                'render': function(results){
                    var html = '<ul class="list-group">';
                        for (var res in results){
                            html += '<li class="list-group-item">' + results[res] + '</li>';
                        }
                    html += '</ul>';
                    return html;
                }
            },
        },
        /**
         * Get the callback functions to render the current draw type
         * @returns {*}
         */
        get_callbacks: function(){
          return this.draw_callbacks[this.options.draw_type];
        },

        /**
         * Add a result to the list of previous results
         *
         * @param result Result to add
         */
        add_result: function (result){
            var callbacks = this.get_callbacks();
            var $results = $('#results').find('.accordion');

            // Add the new result to the accordion
            var result_html =   '<p class="h3">' + this.options.msg_result +
                                '       <small class="result-timestamp hidden-xs">' +
                                '       ' + this.options.msg_generated_on + ' ' + result.datetime +
                                '   </small>' +
                                '</p>' +
                                '<div class="result">';
            result_html += callbacks.render(result.items) + '</div>';
            $results.prepend(result_html);
            $results.accordion('refresh');

            // Open the new result in the accordion
            $results.accordion({active:0});

            // Animate the result when necessary
            if (callbacks.animate){
                callbacks.animate(result.items);
            }
        },

        /**
         * Toss the current draw and reload the page
         */
        toss: function(){
            var that = this;
            // Lock submit buttons to avoid unintentional submitions
            $('.submit-lockable').prop('disabled',true);

            $.ajax({
                method : "POST",
                contentType : 'application/json',
                url : this.options.url_toss
            }).done(function (results){
                // Register the event in Google Analytics
                var is_shared = that.options.is_shared ? 'shared' : 'private';
                ga('send', 'event', 'toss', that.options.draw_type, is_shared);

                // Here results should be rendered without reloading
                //window.location.reload();
                that.add_result(results);
            }).fail(function () {
                alert("{% trans 'There was an issue when tossing the draw :(' %}");
            }).always(function(){
                $('.submit-lockable').prop('disabled',false);
            });
        },

        /**
         * Attempt to create a shared draw.
         * If the draw is created successfully, the invitation methods are presented to the user.
         * If not, the errors are rendered on the form
         *
         * ONLY USED IN SHARED DRAWS
         */
        publish: function(){
            var that = this;

            this.create_draw(
                callback_done = function( data, textStatus, xhr ){
                    // Register the event in Google Analytics
                    ga('send', 'event', 'create_draw', that.options.draw_type, 'shared');

                    // Get the url to the draw
                    var url_draw_api = xhr.getResponseHeader('Location');
                    var url_draw_web = url_draw_api.replace(/api\/v[\d\.]+\//g,'');
                    // Expose link to invite users
                    $('#send-emails').attr('data-link-invite', url_draw_api);
                    // Present the link to the user
                    $('.url-share').val(url_draw_web);
                    // Set url to the FB share button
                    $('#share-fb-icon').attr('data-href', url_draw_web);
                    if (typeof FB !== 'undefined') { //refresh facebook items
                        FB.XFBML.parse();
                    }

                    // Set the link of the "Go to the draw" button
                    $('#go-to-draw').attr('href', url_draw_web);

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
         *
         * ONLY USED IN NORMAL DRAWS
         */
        create_and_toss: function(){
            var that = this;

            this.create_draw(
                callback_done = function( data, textStatus, xhr ){
                    // Register the event in Google Analytics
                    ga('send', 'event', 'create_draw', that.options.draw_type, 'private');
                    ga('send', 'event', 'toss', that.options.draw_type, 'private');

                    // Get the url to the draw
                    var url_draw_api = xhr.getResponseHeader('Location');
                    var url_draw_web = url_draw_api.replace(/api\/v[\d\.]+\//g,'');
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
            // Lock submit buttons to avoid unintentional submitions
            $('.submit-lockable').prop('disabled',true);

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
            .fail(callback_fail)
            .always(function(){
                $('.submit-lockable').prop('disabled',false);
            });
        },

        /**
         * Try if the configuration of the draw is valid.
         * If so, the results are presented to the user (the draw is not saved in the server)
         *
         * ONLY USED IN SHARED DRAWS
         */
        try_draw: function(){
            // Lock submit buttons to avoid unintentional submitions
            $('.submit-lockable').prop('disabled',true);

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
            }).always(function(){
                $('.submit-lockable').prop('disabled',false);
            });
        },

        schedule_toss: function() {
            // Lock submit buttons to avoid unintentional submitions
            $('.submit-lockable').prop('disabled',true);

            var schedule_timestamp = moment.utc(new Date($("#toss-schedule").val())).format();
            this.options.url_schedule_toss = this.options.url_schedule_toss.replace('ts_placeholder',schedule_timestamp);
            $.ajax({
                type : 'POST',
                contentType : 'application/json',
                url : this.options.url_schedule_toss
            }).done(function (){
                // Here response should be rendered without reloading
                window.location.reload();
            })
            .fail(function (e) {
                alert("There was an issue when scheduling the draw :(");
            }).always(function(){
                $('.submit-lockable').prop('disabled',false);
            });
        },

        /**
         * Check whether the user has modified any field and if so the draw is updated in the server.
         * After that the draw is tossed
         *
         * ONLY USED IN NORMAL DRAWS
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
         * Updates the current draw if there were any changes
         * As a result, the page is always reloaded.
         *
         * ONLY USED IN SHARED DRAWS
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
                // Lock submit buttons to avoid unintentional submitions
                $('.submit-lockable').prop('disabled',true);

                var edited_data = JSON.stringify(this.edited_fields);
                $.ajax({
                    type : 'PATCH',
                    contentType : 'application/json',
                    url : this.options.url_update,
                    data: edited_data
                })
                .done(callback_done)
                .fail(callback_fail)
                .always(function(){
                    $('.submit-lockable').prop('disabled',false);
                });
        },

        /**
         * Show the spread step in the creation process of a shared draw
         *
         * ONLY USED IN SHARED DRAWS
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
