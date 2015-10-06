var PublicDraw = {};

PublicDraw.settings = function () {
    function init_settings_panel(){
        // Show the main settings screen
        $('#settings-general').removeClass("hide");
        $('.settings-submenu').addClass("hide");

        // Remove previous feedback in case they exist
        $('div#public-draw-settings div.feedback').addClass('hide');
    }

    // Open settings panel
    $('#edit-settings-button').click(function (){
        init_settings_panel();
    });

    // Show the settings' main screen
    $('.btn-settings-back').click(function (){
        init_settings_panel();
    });

    /*
    SETTINGS OPTION: Edit draw
    Show the confirmation dialog before beginning the edition
    */
    $('li#edit-draw').click(function() {
        $('#settings-general').addClass("hide");
        $('#settings-edit-draw').removeClass("hide");
    });

    /*
    SETTINGS OPTION: Edit draw
    Set up the UI to edit a public draw (already published)
    Unlock the fields, hide toss button and present buttons to save changes and cancel the edition
    */
    $('a#edit-draw-confirmation').click(function() {
        PublicDraw.unlock_fields();
        // Hide the toss button
        $('button#toss, #toss-button, #schedule-toss-button').addClass('hide');
        // Show the "Save changes" and "Cancel edition" buttons
        $('div#edit-draw-save-changes').removeClass('hide');
        // Close settings panel
        $('#public-draw-settings').modal('hide');
        // Disable Settings button
        $('#edit-settings-button').addClass( "hidden" );
        // Show the information div ("Separate items by commas...")
        $('#info-comma-separated').removeClass('hidden');
    });

    /*
    SETTINGS OPTION: Edit draw
    If the user cancel the draw edition, the page is reloaded.
    */
    $('a#edit-draw-cancel').click(function() {
        // Don't use reload to avoid unintentional form submissions
        window.location.href = String( window.location.href ).replace( "/#", "" );
    });

    /*
    SETTINGS OPTION: Edit draw
    If the has edited a public draw so the configuration is submitted to the server
    */
    $('button#edit-draw-save').click(function() {
        $("#draw-form").attr("action", PublicDraw.url_update_draw);
        return true;
    });


    /*
    SETTINGS OPTION: Invite users
    Show the invitation panel
    */
    $('li#invite').click(function() {
        $('#settings-general').addClass("hide");
        $('#settings-invite').removeClass("hide");
    });

    /*
    SETTINGS OPTION: Invite users
    Send the new users to the server
    */
    $('a#send-emails').click(function() {
        $('div#settings-invite div.feedback').addClass('hide');
        var draw_id = $(this).attr("data-id");
        var users = $('input#invite-emails').val();

        // Store the emails in the draw form input
        $('#users').val(users);

        $.get(PublicDraw.url_invite_users, {draw_id: draw_id, emails: users}, function(data){
            $('div#alert-invitation-success').removeClass('hide');
        })
        .fail(function() {
            $('div#alert-invitation-failed').removeClass('hide');
        });
    });
};

PublicDraw.lock_fields = function () {
    // Add read-only property to the inputs of the draw
    $('.protected').prop('readonly', true);
    $('.protected').prop('title', PublicDraw.msg_tooltip_protected);

    // Add read-only property to inputs with tokenField
    $('.protected').tokenfield('readonly');
    $('.protected').parent('.tokenfield').attr('readonly', "true");
};

PublicDraw.unlock_fields = function () {
    // Add read-only property to the inputs of the draw
    $('.protected').removeProp('readonly');

    // Add read-only property to inputs with tokenField
    $('.protected').tokenfield('writeable');
    $('.protected').parent('.tokenfield').removeAttr('readonly');
};


PublicDraw.bom_last_updated = "";
// Make a request to the server to check whether the draw has changed
// If so, reload the page.
PublicDraw.check_draw_changes = function () {
    $.ajax({
        url : PublicDraw.url_get_draw_details,
        method : "GET",
        data: { draw_id : PublicDraw.draw_id }
    }).done(function(data) {
        if(PublicDraw.bom_last_updated < moment.utc(data.last_updated_time)){
            window.location.reload();
        }
        for(var i=0; i<PublicDraw.chats.length; i++) {
            PublicDraw.chats[i].messages = data.messages;
        }
    }).fail (function() {
        console.log("Error when retrieving draw details");
    });

    setTimeout(PublicDraw.check_draw_changes,2000);
};

PublicDraw.save_settings = function (){
    $('button#save-settings').click(function() {
            var enable = $("#settings-chat-enabled").prop( "checked");
            $.get(PublicDraw.url_update_settings, {
                    draw_id: PublicDraw.draw_id,
                    enable_chat: enable
            }).done(function(data){
                // TODO show feedback to indicate that the changes were applied
                PublicDraw.enable_chat(enable);
                PublicDraw.bom_last_updated = new Date();
            })
            .fail(function() {
                // TODO Show feedback when the change could not be done
                console.log("Error when updating the draw details");
            });
        });
};

PublicDraw.enable_chat = function (enable){
    $.each(PublicDraw.chats, function(){
        this.enable(enable);
    });
};

// Initialize the interface for a public draw
PublicDraw.setup = function(){
    // Hide the information div ("Separate items by commas...") when displaying a public draw
    $('#info-comma-separated').addClass('hidden');

    // Initialize input to submit emails to be shown as a tokenField
    $('input#invite-emails').tokenfield({createTokensOnBlur:true, delimiter: [',',' '], inputType: 'email', minWidth: 300});
    $('input#invited-users').tokenfield({createTokensOnBlur:true, delimiter: [',',' '], inputType: 'email', minWidth: 300});

    $(".invited-users-spoiler").click(function() {
		$(this).parent().next().collapse('toggle');
	});

    PublicDraw.settings();
    PublicDraw.lock_fields();

    PublicDraw.check_draw_changes();
    PublicDraw.save_settings();
};
