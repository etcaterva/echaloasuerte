var PublicDrawCreator = {};

PublicDrawCreator.setup_breadcrumb = function (){
    // However we reached here, the step "choose it" has already been done
    $('.breadcrumb-public-draw #choose').addClass('done');
    $('.breadcrumb-public-draw #choose').removeClass('focus');
    $('.breadcrumb-public-draw').attr('data-current-step', 'configure');

    PublicDrawCreator.update_breadcrumb("configure");

    $('.breadcrumb-public-draw #configure').click(function(){
        PublicDrawCreator.show_configure_step();
    })

    $('.breadcrumb-public-draw #spread').click(function(){
        PublicDrawCreator.show_spread_step();
    })
    $('.breadcrumb-public-draw #choose').click(function(){
        $( "#confirmation-change-draw-type" ).dialog( "open" );
    })
};

// Updates the breadcrumb to show the steps that have been already done
PublicDrawCreator.update_breadcrumb = function (current_step){
    if (current_step == "spread"){
        $('.breadcrumb-public-draw #configure').addClass('done');
        $('.breadcrumb-public-draw #configure').removeClass('focus');
        $('.breadcrumb-public-draw #spread').addClass('done');
        $('.breadcrumb-public-draw #spread').addClass('focus');
        $('.breadcrumb-public-draw').attr('data-current-step', 'spread');
    }
    else{
        if (current_step == "configure"){
            $('.breadcrumb-public-draw #configure').addClass('done');
            $('.breadcrumb-public-draw #configure').addClass('focus');
            $('.breadcrumb-public-draw #spread').removeClass('focus');
            $('.breadcrumb-public-draw').attr('data-current-step', 'configure');
        }
    }
};

// This function runs when the user make changes in the privacy of a public draw and click "Save" button
// It store the corresponding values in the input field which will be POSTed
PublicDrawCreator.update_privacy_fields = function (){
    var $shared_type_field = $('input#id_shared_type');
    var mode = $('#privacy-selector').attr('data-selected');
    var $privacy_icon = $('#privacy-level .fa');
    var $privacy_label = $('#public-mode-selected');
    if (mode == "invited"){
        $('#id_password').val("");
        $shared_type_field.attr('value','Invite');
        $privacy_icon.removeClass('fa-unlock');
        $privacy_icon.addClass('fa-lock')
        $privacy_label.empty();
        // TODO translate this
        $privacy_label.append('Only invited users');
    }else if (mode == "password"){
        var password = $('#draw-password').val();
        $('#id_password').val(password);
        $shared_type_field.attr('value','Public');
        $privacy_icon.removeClass('fa-unlock');
        $privacy_icon.addClass('fa-lock')
        $privacy_label.empty();
        // TODO translate this
        $privacy_label.append('Password or Invitation');
    }else{ // Everyone
        $('#id_password').val("");
        $shared_type_field.attr('value','Public');
        $privacy_icon.removeClass('fa-lock');
        $privacy_icon.addClass('fa-unlock')
        $privacy_label.empty();
        // TODO translate this
        $privacy_label.append('Everyone');
    }
}

//Initialize the UI to select the level of privacy for the draw
PublicDrawCreator.prepare_privacy_selection = function (){
    // Initialize the UI (slider) to choose the level of restriction of the public draw
    $("#privacy-selector").slideSelector();

    // Initialize button "Save changes". It stores the selection in the form input
    $('button#save-change-privacy').click(function () {
        PublicDrawCreator.update_privacy_fields();
    });
};

PublicDrawCreator.show_spread_step = function () {
    PublicDrawCreator.update_breadcrumb("spread");
    $('.step-configure').addClass('hidden');
    $('.step-spread').removeClass('hidden');
};

PublicDrawCreator.show_configure_step = function () {
    PublicDrawCreator.update_breadcrumb("configure");
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

    //Initialize the UI to select the level of privacy for the draw
    PublicDrawCreator.prepare_privacy_selection();

    // Initialize input to submit emails to be shown as a tokenField
    $('input#invite-emails').tokenfield({createTokensOnBlur:true, delimiter: [',',' '], inputType: 'email', minWidth: 150});

    PublicDrawCreator.setup_breadcrumb("configure");

    // Initialize the shared_type field to Public
    $('input#id_shared_type').val("Public");

    $('a.back-arrow').click(function () {
        var current_step = $('.breadcrumb-public-draw').attr('data-current-step');
        if (current_step == "spread"){ // If step is spread
            PublicDrawCreator.show_configure_step();
            return false;
        }
        else{
            if (current_step == "configure") {
                $( "#dialog" ).dialog( "open" );
                return true; // Go to the index (setup in href in <a> tag)
            }
        }
    });

    $('#next').click(function () {
        //PublicDrawCreator.show_spread_step();
        PublicDrawCreator.validate();
    });

    $('#try').click(function () {
        //PublicDrawCreator.try_draw();
        $('#draw-form').attr("action", PublicDrawCreator.url_try);
    });

    // Set up confirmation dialog that will be shown if the user tries to go to the index while he is setting up a public draw
    $(function() {
        $( "#confirmation-change-draw-type" ).dialog({
            resizable: false,
            autoOpen: false,
            modal: true,
            buttons: {
                // TODO "Change type" has to be tranlated
                "Change type": function() {
                    $( this ).dialog( "close" );
                    window.location.href = PublicDrawCreator.url_index;
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
};
