var PublicDrawCreator = {};

PublicDrawCreator.show_spread_step = function () {
    $('.step-configure').addClass('hidden');
    $('.step-spread').removeClass('hidden');
};

PublicDrawCreator.show_configure_step = function () {
    $('.step-spread').addClass('hidden');
    $('.step-configure').removeClass('hidden');
};

// Serialize a form to a JS object
$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

PublicDrawCreator.create_draw = function (){
    // Disable button to avoid duplicated submissions
    $('#publish').prop('disabled',true);

    // Serialize and clean the form
    var form_fields = $('#draw-form').serializeObject();
    delete form_fields["csrfmiddlewaretoken"];
    delete form_fields["_id"];
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
            $('#share-fb-icon').attr('data-href', draw_url);
            if (typeof FB !== 'undefined') { //refresh facebook items
                FB.XFBML.parse();
            }

            // Set the link of the "Go to the draw" button
            $('#go-to-draw').attr('href', url_draw_web);

            PublicDrawCreator.show_spread_step();
        })
        .fail(function (e){
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

    $('#try').click(function () {
        //PublicDrawCreator.try_draw();
        $('#draw-form').attr("action", PublicDrawCreator.url_try);
    });
};
