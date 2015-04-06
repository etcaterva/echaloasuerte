var public_draw_manager = {};

// Updates the breadcrumb to show the steps that have been already done
public_draw_manager.update_breadcrumb = function (current_step){
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
}

// Store the step we are in (when creating a public draw) to send it in the POST
public_draw_manager.set_submition_type = function (current_step){
    var submit_type = "public_toss";
    if (current_step == "configure"){
        submit_type = "go_to_spread";
    } else if (current_step == "spread"){
        submit_type = "publish";
    }
    $("input[name=submit-type]").val(submit_type);

    // If "Try" button is clicked, the type of submition changes
    $('#try').click(function() {
        $("input[name=submit-type]").val("try");
        return true;
    });
}

// Thi function runs when the user make changes in the privacy of a public draw and click "Save" button
// It store the corresponding values in the input field which will be POSTed
public_draw_manager.update_privacy_fields = function (){
    var shared_type_field = $('input#shared-type');
    var mode = $('.slide-bar').attr('data-selected');
    if (mode == "invited"){
        $('#id_password').val("");
        shared_type_field.attr('value','Invite');
    }else if (mode == "password"){
        var password = $('#draw-password').val();
        $('#id_password').val(password);
        shared_type_field.attr('value','Public');
    }else{ // Everyone
        $('#id_password').val("");
        shared_type_field.attr('value','Public');
    }
}

//Initialize the UI to select the level of privacy for the draw
public_draw_manager.prepare_privacy_selection = function (){
    // Initialize the UI (slider) to choose the level of restriction of the public draw
    SlideSelector.setup();

    // Initialize button "Save changes". It stores the selection in the form input
    $('a#save-change-privacy').click(function () {
        public_draw_manager.update_privacy_fields();
    });
}

public_draw_manager.settings = function () {

    function main_screen_settings () {
        $('#settings-general').removeClass("hide");
        $('.settings-submenu').addClass("hide");
    };

    function close_settings () {
        $('#public-draw-settings').modal('hide');
        main_screen_settings();
    };

    $('li#edit-draw').click(function() {
        $('#settings-general').addClass("hide");
        $('#settings-edit-draw').removeClass("hide");
    });

    // Set up the UI to edit a public draw (already published)
    // Unlock the fields, hide toss button and present buttons to save changes and cancel the edition
    $('a#btn-edit-draw').click(function() {
        public_draw_manager.unlock_fields();
        $('button#public-toss').addClass('hide');
        $('div#edit-draw-save-changes').removeClass('hide');
        close_settings();
    });

    // When the user is editing a public draw, the buttons "Cancel edition" and "Save changes" are presented.
    // That's the first cancel button
    $('a#edit-draw-cancel').click(function() {
        // using replace instead on reload to avoid unintentional form submissions
        var url = window.location.href;
        window.location.replace(url);
    });

    // When the user is editing a public draw, the buttons "Cancel edition" and "Save changes" are presented.
    // That's the first "Save changes" button
    $('button#edit-draw-save').click(function() {
        $("input[name=submit-type]").val("edit_public_draw");
        return true;
    });




    $('li#invite').click(function() {
        $('#settings-general').addClass("hide");
        $('#settings-invite').removeClass("hide");
    });

    $('li#privacy').click(function() {
        $('#settings-general').addClass("hide");
        $('#settings-privacy').removeClass("hide");
    });

    $('.btn-settings-back').click(function() {
        main_screen_settings();
    });

    $('a#send-emails').click(function() {
        var draw_id = $(this).attr("data-id");
        var users = $('input#emails').val();
        $.get(public_draw_manager.url_invite_users, {draw_id: draw_id, emails: users}, function(data){
            if (data == "OK")
                alert("Users invited");
            else
                alert("One or more emails contains errors");
        });
    });

    $('a#save-change-privacy').click(function() {
        public_draw_manager.update_privacy_fields();
        var draw_id = $(this).attr("data-id");
        var shared_type = $('input#shared-type').val();
        var password = $('input#id_password').val();
        $.get(public_draw_manager.url_draw_privacy, {draw_id: draw_id, shared_type: shared_type, password: password}, function(data){
            if (data == "OK")
                alert("Privacy Changed");
            else
                alert("Privacy could not be changed");
        });
    });

}

public_draw_manager.lock_fields = function () {
    // Add read-only property to the inputs of the draw
    $('.protected').prop('readonly', true);

    // Add read-only property to inputs with tokenField
    $('.protected').tokenfield('readonly');
    $('.protected').parent('.tokenfield').attr('readonly', "true");
}

public_draw_manager.unlock_fields = function () {
    // Add read-only property to the inputs of the draw
    $('.protected').removeProp('readonly');

    // Add read-only property to inputs with tokenField
    $('.protected').tokenfield('writeable');
    $('.protected').parent('.tokenfield').removeAttr('readonly');
}

// Initialize the interface for a public draw
public_draw_manager.setup = function(current_step){
    public_draw_manager.set_submition_type(current_step);
    //Initialize the UI to select the level of privacy for the draw
    public_draw_manager.prepare_privacy_selection();
    // Initialize input to submit emails to be shown as a tokenField
    $('input#emails').tokenfield({createTokensOnBlur:true, delimiter: [',',' '], inputType: 'email', minWidth: 300});

    if (current_step == ""){
        // If the draw has already been published
        public_draw_manager.settings();
        public_draw_manager.lock_fields();
    } else{
        // If the the user is creating the draw
        public_draw_manager.update_breadcrumb(current_step);
        if (current_step == "spread"){
            $('.step-configure').hide();
        } else if (current_step == "configure"){
            $('.step-spread').hide();
        }
    }
}