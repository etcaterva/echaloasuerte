var PublicDrawCreator = {};

PublicDrawCreator.show_spread_step = function () {
    $('.step-configure').addClass('hidden');
    $('.step-spread').removeClass('hidden');
};

PublicDrawCreator.show_configure_step = function () {
    $('.step-spread').addClass('hidden');
    $('.step-configure').removeClass('hidden');
};


jQuery.fn.extend({
    // Serialize a form to a JS object
    serializeForm: function(fields_skipped) {
        var rCRLF = /\r?\n/g,
            rsubmitterTypes = /^(?:submit|button|image|reset|file)$/i,
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

            return this.name && $.inArray(this.name, fields_skipped) < 0 &&
                !jQuery( this ).is( ":disabled" ) && rsubmittable.test( this.nodeName ) &&
                !rsubmitterTypes.test( type ) && ( this.checked || !manipulation_rcheckableType.test( type ) );
        })
        .map(function( i, elem ){
            var val = jQuery( this ).val().replace( rCRLF, "\r\n" );
                var type = elem.type;
            if (type == "number"){
                val = parseInt(val, 10);
            }else if (type == "checkbox" ){
                val = true;
            }else if (type == "hidden" || type == "radio"){
                if (val == "True"){
                    val = true;
                }else if (val == "False"){
                    val = false;
                }else if (!isNaN(val)){
                    val = parseInt(val, 10);
                }
            }
            return val == null ?
                null :
                jQuery.isArray( val ) ?
                    jQuery.map( val, function( val ){
                        return { name: elem.name, value: val, type: elem.type };
                    }) :
                    { name: elem.name, value: val, type: elem.type };
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

PublicDrawCreator.create_draw = function (){
    // Disable button to avoid duplicated submissions
    $('#publish').prop('disabled',true);

    // Serialize and clean the form
    var fields_skipped = ["csrfmiddlewaretoken", "_id"];
    var form_fields = $('#draw-form').serializeForm(fields_skipped);
    form_fields["type"] = PublicDrawCreator.draw_type;
    var data = JSON.stringify(form_fields);

    $.ajax({
        type : "POST",
        contentType : 'application/json',
        url: PublicDrawCreator.url_create,
        data: data
        }).done(function( data, textStatus, xhr ) {
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

            PublicDrawCreator.show_spread_step();
        })
        .fail(function (){
            var $form = $('#draw-form');
            $form.attr("action", PublicDrawCreator.url_try);
            $form.submit();
        });
};

PublicDrawCreator.title_changed = false;
PublicDrawCreator.shake_title = function(){
    if (!PublicDrawCreator.title_changed) {
        $('#draw-title-container').effect('shake',{ direction: "right", times: 3, distance: 20},1000);
       setTimeout(PublicDrawCreator.shake_title, 5000);
    }
};

// Initialize the interface for a public draw
PublicDrawCreator.setup = function(){
    var $title_container = $("#draw-title-container");
    $("textarea.autogrow").click( function() {
        PublicDrawCreator.title_changed = true;
        // Stop the shaking animation
        $title_container.stop(true,true);
        // Remove residual div of shake effect
        if ($title_container.parent().is('.ui-effects-wrapper')){
            $title_container.unwrap();
            // If we remove the parent, the click won't be propagated, need to "re-click" it
            $("textarea.autogrow").click();
        }
        // Remove residual CSS class from shake effect
        $title_container.removeAttr('style');
    });

    PublicDrawCreator.shake_title();

    // Initialize input to submit emails to be shown as a tokenField
    $('input#invite-emails').tokenfield({createTokensOnBlur:true, delimiter: [',',' '], inputType: 'email', minWidth: 150});


    // Initialize the shared_type field to Public
    $('input#id_shared_type').val("Public");

    $('#publish').click(function () {
        //PublicDrawCreator.show_spread_step();
        PublicDrawCreator.create_draw();
    });

    /*$('#try').click(function () {
        //PublicDrawCreator.try_draw();
        $('#draw-form').attr("action", PublicDrawCreator.url_try);
    });*/
};
