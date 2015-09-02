var PublicDrawCreator = {};

PublicDrawCreator.show_spread_step = function () {
    $('.step-configure').addClass('hidden');
    $('.step-spread').removeClass('hidden');
};

PublicDrawCreator.show_configure_step = function () {
    $('.step-spread').addClass('hidden');
    $('.step-configure').removeClass('hidden');
};

// Get all the messages of a public draw and refresh the chat board
PublicDrawCreator.validate = function (){
    var form_fields = $('#draw-form').serialize();
    form_fields += "&draw_type=" + PublicDrawCreator.draw_type;
    $.post( PublicDrawCreator.url_validate, form_fields)
        .done(function( data ) {
            if (data.is_valid == true) {
                var $form = $('#draw-form');
                // Set the form action to create a new draw as it may be "try_draw"
                $form.attr("action", PublicDrawCreator.url_create_public_draw);

                // Since the form has been just validated, hide possible previous alerts
                $('.step-configure .alert').hide();

                PublicDrawCreator.show_spread_step();
            }else{
                var $form = $('#draw-form');
                $form.attr("action", PublicDrawCreator.url_try);
                $form.submit();
            }
        })
        .fail(function (){
            // TODO Translate this message and show it in a better way
            alert("Something went wrong");
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
        PublicDrawCreator.validate();
    });

    $('#try').click(function () {
        //PublicDrawCreator.try_draw();
        $('#draw-form').attr("action", PublicDrawCreator.url_try);
    });
};
