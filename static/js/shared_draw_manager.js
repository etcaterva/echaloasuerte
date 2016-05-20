function disable_tooltip_share_url(){
    // Do not open tooltip for the url input when hovered
    $('.url-share').tooltip({
        position: { my: 'center bottom' , at: 'center top-10' },
        disabled: true,
        close: function( event, ui ) {
            $(this).tooltip('disable');
        }
    });
}

jQuery.fn.extend({
    /**
     * Select the content of an input and try to copy it into the clipboard
     */
    select_and_copy: function () {
        // Select the input text
        var $this = $(this);
        var input = $this[0];
        input.setSelectionRange(0, input.value.length);
        try {
            // Try to copy the selected text into the clipboard
            if (document.execCommand('copy')) {
                $this.tooltip('enable').tooltip('open');
                setTimeout(function(){
                    $this.tooltip('close');
                }, 2000);
            }
        } catch (err) {
            // Browser does not support copying to clipboard
        }
    }
});

/*******************************
      Shared draw creation
 ******************************/
SharedDrawCreator = {};
SharedDrawCreator.show_general_step = function () {
    SharedDrawCreator.update_breadcrumb('general');
    $('.step-configure').toggleClass('hidden', true);
    $('.step-invite').toggleClass('hidden', true);
    $('.step-general').toggleClass('hidden', false);
};

SharedDrawCreator.show_configure_step = function () {
    SharedDrawCreator.update_breadcrumb('configure');

    // Copy the draw's title to the resizable input
    var draw_title = $('#draw-title').val();
    var $draw_title_resizable = $('#draw-title-container').find("[name='title']");
    $draw_title_resizable.val(draw_title);

    $('.step-general').toggleClass('hidden', true);
    $('.step-invite').toggleClass('hidden', true);
    $('.step-configure').toggleClass('hidden', false);

    // Once shown, trigger 'blur' event to force resizing
    $draw_title_resizable.blur();
};

SharedDrawCreator.show_invite_step = function () {
    SharedDrawCreator.update_breadcrumb('invite');
    $('.step-general').toggleClass('hidden', true);
    $('.step-configure').toggleClass('hidden', true);
    $('.step-invite').toggleClass('hidden', false);
};


// Updates the breadcrumb to show the steps that have been already done
SharedDrawCreator.update_breadcrumb = function (target_step){
    var $breadcrumb = $('.breadcrumb-shared-draw');
    var $label_general = $breadcrumb.find('#general');
    var $label_configure = $breadcrumb.find('#configure');
    var $label_invite = $breadcrumb.find('#invite');

    if (target_step == "invite"){
        $label_configure.toggleClass('focus', false);
        $label_invite.toggleClass('focus', true);
        $label_invite.toggleClass('done', true);
        $breadcrumb.attr('data-current-step', 'invite');

        // Disable breadcrumb links to previous steps
        $breadcrumb.find('#general').attr('disabled', 'disabled');
        $breadcrumb.find('#configure').attr('disabled', 'disabled');
    }
    else{
        if (target_step == "configure"){
            $label_general.toggleClass('focus', false);
            $label_configure.toggleClass('done', true);
            $label_configure.toggleClass('focus', true);
            $breadcrumb.attr('data-current-step', 'configure');
        }
        else{
            if (target_step == "general"){
                $label_general.toggleClass('focus', true);
                $label_configure.toggleClass('focus', false);
                $label_invite.toggleClass('focus', false);
                $breadcrumb.attr('data-current-step', 'general');
            }
        }
    }
};

SharedDrawCreator.setup = function(){
    disable_tooltip_share_url();

    // Initialize the links in the breadcrumb
    var $breadcrumb = $('.breadcrumb-shared-draw');
    $breadcrumb.find('#general').click(SharedDrawCreator.show_general_step);
    $breadcrumb.find('#configure').click(SharedDrawCreator.show_configure_step);
};

/*******************************
      Shared draw display
 ******************************/
var SharedDraw = {};
SharedDraw.defaults = {
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
    msg_tooltip_protected: "To edit the details go to Settings"
};

SharedDraw.setup_settings_panel = function () {
    function show_settings_panel(){
        // Show the main settings screen
        $('#settings-general').removeClass("hide");
        $('.settings-submenu').addClass("hide");

        // Remove previous feedback in case they exist
        $('div#shared-draw-settings-modal div.feedback').addClass('hide');
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
    Set up the UI to edit a shared draw (already published)
    Unlock the fields, hide toss button and present buttons to save changes and cancel the edition
    */
    $('a#edit-draw-confirmation').click(function() {
        SharedDraw.lock_fields(false);
        // Hide the toss button
        $('#shared-draw-toss, #schedule-toss-button').addClass('hide');
        // Show the "Save changes" and "Cancel edition" buttons
        $('div#edit-draw-save-changes').removeClass('hide');
        // Close settings panel
        $('#shared-draw-settings-modal').modal('hide');
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
    If the has edited a shared draw so the configuration is submitted to the server
    */
    $('#edit-draw-save').click(function() {
        SharedDraw.options.draw_manager.drawManager('update_shared_draw');
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
            url: SharedDraw.options.url_invite_users
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
SharedDraw.lock_fields = function(locked){
    var $protected_fields = $('.protected');
    var $protected_hidden_fields = $('.protected-hidden');
    var $protected_inputs = $('input.protected, textarea.protected');
    var $protected_buttons = $('button.protected');
    var $protected_tokenfields = $('input.protected.eas-tokenfield');
    if (locked){
        // Add tooltip to state that they are protected
        $protected_fields.prop('title', SharedDraw.options.msg_tooltip_protected);

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
        $protected_inputs.removeProp('readonly');

        // Remove disabled class from buttons
        $protected_buttons.toggleClass('disabled', false);

        // Remove read-only property to inputs with tokenField
        $protected_tokenfields.tokenfield('writeable');
        $protected_tokenfields.parent('.tokenfield').removeAttr('readonly');
    }
};

// Make a request to the server to check whether the draw has changed
// If so, reload the page.
SharedDraw.check_draw_changes = function () {
    $.ajax({
        method : "GET",
        contentType : 'application/json',
        url : SharedDraw.options.url_get_chat_messages
    }).done(function(data) {
        if(SharedDraw.options.bom_last_updated < moment.utc(data.last_updated_time)){
            window.location.reload();
        }
        for(var i=0; i<SharedDraw.options.chats.length; i++) {
            SharedDraw.options.chats[i].messages = data.messages;
        }
    }).fail (function() {
        console.log("Error when retrieving draw details");
    });
};

SharedDraw.save_settings = function (){
    var enable = $("#settings-chat-enabled").prop( "checked");
    var data = JSON.stringify({'enable_chat': enable});
    $.ajax({
        method : "PATCH",
        contentType : 'application/json',
        url : SharedDraw.options.url_update,
        data: data
    }).done(function(data) {
        // TODO show feedback to indicate that the changes were applied
        SharedDraw.enable_chat(enable);
        SharedDraw.options.bom_last_updated = new Date();
    }).fail (function() {
        // TODO Show feedback when the change could not be done
        console.log("Error when updating the draw details");
    });
};

SharedDraw.enable_chat = function (enable){
    $.each(SharedDraw.options.chats, function(){
        this.enable(enable);
    });
};

SharedDraw.setup_buttons = function (){
        $("#confirm-schedule-button").click( function() {
            $('#confirm-schedule-button').prop('disabled',true);
            SharedDraw.options.draw_manager.drawManager('schedule_toss');
        });

        $('#schedule-toss-button').click(function() {
            $('#schedule-toss-modal').modal('show');
        });

        $("#shared-draw-toss").click( function() {
            SharedDraw.options.draw_manager.drawManager('toss');
            return false;
        });

        $('#subscribe-button').click(function() {
            if (SharedDraw.options.is_authenticated){
                var isSubscribed = $('#subscribe-button').attr("data-active") === "y";
                SharedDraw.subscribe(!isSubscribed)
            }else{
                alert(SharedDraw.options.msg_login_to_subscribe);
            }
        });
};

SharedDraw.subscribe = function (subscribe){
    var $subscribe_button = $('#subscribe-button');
    if (subscribe) {
        $.ajax({
            method : "POST",
            url : SharedDraw.options.url_subscribe,
            data: "{}"
        }).done(function (){
            console.log("subscribed to draw");
            $subscribe_button.attr("data-active", "n");
        })
        .fail(function (error) {
            alert(SharedDraw.options.msg_error_subscribe);
            console.log(error);
        });
    } else {
        $.ajax({
            method : "DELETE",
            url : SharedDraw.options.url_subscribe,
            data: {}
        }).done(function (){
            console.log("Unsubscribed to draw");
            $subscribe_button.attr("data-active", "y");
        })
        .fail(function (error) {
            alert(SharedDraw.options.msg_error_unsubscribe);
            console.log(error);
        });
    }
};

// Initialize the interface for a shared draw
SharedDraw.setup = function(options){
    SharedDraw.options = $.extend({}, SharedDraw.defaults, options);

    disable_tooltip_share_url();

    // Hide the information div ("Separate items by commas...") when displaying a shared draw
    $('#info-comma-separated').addClass('hidden');

    // Initialize input to submit emails to be shown as a tokenField
    $('input#invite-emails').tokenfield({createTokensOnBlur:true, delimiter: [',',' '], inputType: 'email', minWidth: 300});
    $('input#invited-users').tokenfield({createTokensOnBlur:true, delimiter: [',',' '], inputType: 'email', minWidth: 300});

    $(".invited-users-spoiler").click(function() {
		$(this).parent().next().collapse('toggle');
	});

    // Update url in the FB share button
    $('.url-share').val(SharedDraw.options.url_share_fb);

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
    SharedDraw.lock_fields(true);

    SharedDraw.setup_settings_panel();
    SharedDraw.setup_buttons();

    // Check periodically if the draw has been updated
    SharedDraw.check_draw_changes();

    $('#save-settings').bind("click", SharedDraw.save_settings);

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

