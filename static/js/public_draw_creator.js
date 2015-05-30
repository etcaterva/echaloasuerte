var PublicDrawCreator = {};

// Updates the breadcrumb to show the steps that have been already done
PublicDrawCreator.update_breadcrumb = function (current_step){
    // However we reached here, the step "choose it" has already been done
    $('.breadcrumb-public-draw #choose').addClass('done');
    $('.breadcrumb-public-draw #choose').removeClass('focus');
    $('.breadcrumb-public-draw').attr('data-current-step', 'configure');
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
PublicDrawCreator.try_draw = function (){
    var that = this;
    var $chat = this.$element.find("#chat-board");
    $.ajax({
        url : PublicDrawCreator.url_try,
        method : "GET",
        data: { draw_id : this.options.draw_id},
        success : function(data){

            var arr = data.messages;
            for (var i = 0, length = arr.length; i < length; i++) {
              var element = arr[i];
              console.log(element);
            }
        }
    });
};

// Initialize the interface for a public draw
PublicDrawCreator.setup = function(){
    //Initialize the UI to select the level of privacy for the draw
    PublicDrawCreator.prepare_privacy_selection();

    PublicDrawCreator.prepare_invitation_fields();

    PublicDrawCreator.update_breadcrumb("configure");

    $('a#next').click(function () {
        PublicDrawCreator.show_spread_step();
    });

    $('a.back-arrow').click(function () {
        var current_step = $('.breadcrumb-public-draw').attr('data-current-step');
        if (current_step == "spread"){ // If step is spread
            PublicDrawCreator.show_configure_step();
            return false;
        }
        else{
            if (current_step == "configure") {
                // TODO Ask for confimation, as the process done will be lost
                $( "#dialog" ).dialog( "open" );
                return true; // Go to the index (href in <a> tag)
            }
        }
    });

    $('a#try').click(function () {
        PublicDrawCreator.try_draw();
    });

    $('.breadcrumb-public-draw #configure').click(function(){
        PublicDrawCreator.show_configure_step();
    })

    $('.breadcrumb-public-draw #spread').click(function(){
        PublicDrawCreator.show_spread_step();
    })
    $('.breadcrumb-public-draw #choose').click(function(){
        // TODO Ask for confimation, as the process done will be lost
        $( "#confirmation-change-draw-type" ).dialog( "open" );
    })

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
