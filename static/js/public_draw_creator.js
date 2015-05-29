var PublicDrawCreator = {};

// Updates the breadcrumb to show the steps that have been already done
PublicDrawCreator.update_breadcrumb = function (current_step){
    // However we reached here, the step "choose it" has already been done
    $('.info-public-draw #choose').addClass('done');
    if (current_step == "spread"){
        $('.info-public-draw #configure').addClass('done');
    }
    else{
        if (current_step == "configure"){
            // If the step "spread" has already been done, add the CSS class "done"
            // This part will be filled when the step backward is implemented
        }
    }
};

// This function runs when the user make changes in the privacy of a public draw and click "Save" button
// It store the corresponding values in the input field which will be POSTed
PublicDrawCreator.update_privacy_fields = function (){
    var $shared_type_field = $('input#id_shared_type');
    var mode = $('#privacy-selector').attr('data-selected');
    if (mode == "invited"){
        $('#id_password').val("");
        $shared_type_field.attr('value','Invite');
    }else if (mode == "password"){
        var password = $('#draw-password').val();
        $('#id_password').val(password);
        $shared_type_field.attr('value','Public');
    }else{ // Everyone
        $('#id_password').val("");
        $shared_type_field.attr('value','Public');
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


PublicDrawCreator.prepare_invitation_fields = function () {
    // Initialize input to submit emails to be shown as a tokenField
    $('input#invite-emails').tokenfield({createTokensOnBlur:true, delimiter: [',',' '], inputType: 'email', minWidth: 300});

    $('#publish').click(function () {
        var users_to_invite = $('#invite-emails').val();
        $('#users').val(users_to_invite);
    });
};

PublicDrawCreator.show_spread_step = function () {
    $('.step-configure').addClass('hidden');
    $('.step-spread').removeClass('hidden');
};

PublicDrawCreator.show_configure_step = function () {
    $('.step-spread').addClass('hidden');
    $('.step-configure').removeClass('hidden');
};

// Initialize the interface for a public draw
PublicDrawCreator.setup = function(current_step){
    //Initialize the UI to select the level of privacy for the draw
    PublicDrawCreator.prepare_privacy_selection();

    PublicDrawCreator.prepare_invitation_fields();

    PublicDrawCreator.update_breadcrumb(current_step);

    $('a#next').click(function () {
        PublicDrawCreator.show_spread_step();
    });

};
