var PublicDraw = {};

PublicDraw.defaults = {
    draw_id: null,
    is_authenticated: false,
    bom_last_updated: null,
    chats: null,
    draw_manager: null,
    url_invite_users: null,
    url_get_chat_messages: null,
    url_update: null,
    url_subscribe: null,
    msg_login_to_subscribe: "Please, log in to be able to subscribe to a draw",
    msg_error_subscribe: "There was an issue when subscribing to the draw :(",
    msg_error_unsubscribe: "There was an issue when unsubscribing to the draw :(",
};

PublicDraw.setup_settings_panel = function () {
    function show_settings_panel(){
        // Show the main settings screen
        $('#settings-general').removeClass("hide");
        $('.settings-submenu').addClass("hide");

        // Remove previous feedback in case they exist
        $('div#public-draw-settings div.feedback').addClass('hide');
    }

    // Open settings panel
    $('#edit-settings-button').click(function (){
        show_settings_panel();
    });

    // Show the settings' main screen
    $('.btn-settings-back').click(function (){
        show_settings_panel();
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
        PublicDraw.lock_fields(false);
        // Hide the toss button
        $('#shared-draw-toss, #schedule-toss-button').addClass('hide');
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
    $('#edit-draw-save').click(function() {
        PublicDraw.options.draw_manager.drawManager('update_shared_draw');
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
        $('div#settings-invite').find('div.feedback').addClass('hidden');
        var users = $('input#invite-emails').val();

        // Serialize the emails
        var users_to_invite = {'add_user': users.split(',')};
        var data = JSON.stringify(users_to_invite);

        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            data: data,
            url: PublicDraw.options.url_invite_users
        }).done(function(){
            $('#alert-invitation-success').removeClass('hidden');
            console.log("users invited");
        }).fail(function(){
            $('#alert-invitation-fail').removeClass('hidden');
            console.log("users NOT invited");
        });
    });
};

/**
 * Lock and unlock the form fields
 *
 * @param locked Determines whether the fields will be locked or unlocked
 */
PublicDraw.lock_fields = function(locked){
    var $protected_fields = $('.protected');
    var $protected_hidden_fields = $('.protected-hidden');
    var $protected_inputs = $('input.protected');
    var $protected_buttons = $('button.protected');
    var $protected_tokenfields = $('input.protected.eas-tokenfield');
    if (locked){
        // Add tooltip to state that they are protected
        $protected_fields.prop('title', PublicDraw.options.msg_tooltip_protected);

        // Hide fields that should not be shown in shared draws
        $protected_hidden_fields.toggleClass('hidden', true);

        // Add read-only property to the inputs of the draw
        $protected_inputs.prop('readonly', true);

        // If disabled class to buttons
        $protected_buttons.toggleClass('disabled', true);

        // Add read-only property to inputs with tokenField
        $protected_tokenfields.tokenfield('readonly');
        $protected_tokenfields.parent('.tokenfield').attr('readonly', "true");
    }else{
        // Remove the tooltip
        $protected_fields.prop('title','');

        // Show fields that were hidden in shared draws
        $protected_hidden_fields.toggleClass('hidden', false);

        // Remove read-only property to the inputs of the draw
        $protected_fields.removeProp('readonly');

        // Remove disabled class from buttons
        $protected_buttons.toggleClass('disabled', false);

        // Remove read-only property to inputs with tokenField
        $protected_tokenfields.tokenfield('writeable');
        $protected_tokenfields.parent('.tokenfield').removeAttr('readonly');
    }
};

// Make a request to the server to check whether the draw has changed
// If so, reload the page.
PublicDraw.check_draw_changes = function () {
    $.ajax({
        method : "GET",
        contentType : 'application/json',
        url : PublicDraw.options.url_get_chat_messages
    }).done(function(data) {
        if(PublicDraw.options.bom_last_updated < moment.utc(data.last_updated_time)){
            window.location.reload();
        }
        for(var i=0; i<PublicDraw.options.chats.length; i++) {
            PublicDraw.options.chats[i].messages = data.messages;
        }
    }).fail (function() {
        console.log("Error when retrieving draw details");
    });
};

PublicDraw.save_settings = function (){
    var enable = $("#settings-chat-enabled").prop( "checked");
    var data = JSON.stringify({'enable_chat': enable});
    $.ajax({
        method : "PATCH",
        contentType : 'application/json',
        url : PublicDraw.options.url_update,
        data: data
    }).done(function(data) {
        // TODO show feedback to indicate that the changes were applied
        PublicDraw.enable_chat(enable);
        PublicDraw.options.bom_last_updated = new Date();
    }).fail (function() {
        // TODO Show feedback when the change could not be done
        console.log("Error when updating the draw details");
    });
};

PublicDraw.enable_chat = function (enable){
    $.each(PublicDraw.options.chats, function(){
        this.enable(enable);
    });
};

PublicDraw.setup_buttons = function (){
        $("#confirm-schedule-button").click( function() {
            $('#confirm-schedule-button').prop('disabled',true);
            PublicDraw.options.draw_manager.drawManager('schedule_toss');
        });

        $('#schedule-toss-button').click(function() {
            $('#schedule-toss-modal').modal('show');
        });

        $("#shared-draw-toss").click( function() {
            PublicDraw.options.draw_manager.drawManager('toss');
            return false;
        });

        $('#subscribe-button').click(function() {
            if (PublicDraw.options.is_authenticated){
                var isSubscribed = $('#subscribe-button').attr("data-active") === "y";
                PublicDraw.subscribe(!isSubscribed)
            }else{
                alert(PublicDraw.options.msg_login_to_subscribe);
            }
        });
};

PublicDraw.subscribe = function (subscribe){
    var $subscribe_button = $('#subscribe-button');
    if (subscribe) {
        $.ajax({
            method : "POST",
            url : PublicDraw.options.url_subscribe,
            data: "{}"
        }).done(function (){
            console.log("subscribed to draw");
            $subscribe_button.attr("data-active", "n");
        })
        .fail(function (error) {
            alert(PublicDraw.options.msg_error_subscribe);
            console.log(error);
        });
    } else {
        $.ajax({
            method : "DELETE",
            url : PublicDraw.options.url_subscribe,
            data: {}
        }).done(function (){
            console.log("Unsubscribed to draw");
            $subscribe_button.attr("data-active", "y");
        })
        .fail(function (error) {
            alert(PublicDraw.options.msg_error_unsubscribe);
            console.log(error);
        });
    }
};

// Initialize the interface for a public draw
PublicDraw.setup = function(options){
    PublicDraw.options = $.extend({}, PublicDraw.defaults, options);

    // Hide the information div ("Separate items by commas...") when displaying a public draw
    $('#info-comma-separated').addClass('hidden');

    // Initialize input to submit emails to be shown as a tokenField
    $('input#invite-emails').tokenfield({createTokensOnBlur:true, delimiter: [',',' '], inputType: 'email', minWidth: 300});
    $('input#invited-users').tokenfield({createTokensOnBlur:true, delimiter: [',',' '], inputType: 'email', minWidth: 300});

    $(".invited-users-spoiler").click(function() {
		$(this).parent().next().collapse('toggle');
	});

    // Update url in the FB share button
    $('.url-share').val(PublicDraw.options.url_share_fb);

    // Add datetime picker to schedule draws
    $('.datetimepicker').datetimepicker({value:moment().format()});

    // When fields are focused, pre-selected its content
    $('#draw-form').find('.form-control').click(function() {
        var attr = $(this).hasClass('protected');
        if (typeof attr === typeof undefined || attr === false) {
            $(this).select();
        }
    });

    // Add the styled tooltip
    $(".protected").tooltip({
        show: {delay: 500},
        track: true
    });
    PublicDraw.lock_fields(true);

    PublicDraw.setup_settings_panel();
    PublicDraw.setup_buttons();

    // Check periodically if the draw has been updated
    PublicDraw.check_draw_changes();

    $('#save-settings').bind("click", PublicDraw.save_settings);

    // Make description box collapsible
    var $description_area = $('#draw-description-area');
    var collapsed_height = $description_area.outerHeight();
    $description_area.focus(function () {
        var text = document.getElementById('draw-description-area');
        $(this).animate({ height: text.scrollHeight }, 500);
    });
    $description_area.blur(function () {
        $(this).animate({ height: collapsed_height }, 500);
    });
};
