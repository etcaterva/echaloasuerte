var PublicDrawCreator = {};

PublicDrawCreator.show_general_step = function () {
    PublicDrawCreator.update_breadcrumb('general');
    $('.step-configure').toggleClass('hidden', true);
    $('.step-invite').toggleClass('hidden', true);
    $('.step-general').toggleClass('hidden', false);
};

PublicDrawCreator.show_configure_step = function () {
    PublicDrawCreator.update_breadcrumb('configure');

    // Copy the draw's title to the resizable input
    var draw_title = $('#draw-title').val();
    $('#draw-title-container').find("[name='title']").val(draw_title);

    $('.step-general').toggleClass('hidden', true);
    $('.step-invite').toggleClass('hidden', true);
    $('.step-configure').toggleClass('hidden', false);

};

PublicDrawCreator.show_invite_step = function () {
    PublicDrawCreator.update_breadcrumb('invite');
    $('.step-general').toggleClass('hidden', true);
    $('.step-configure').toggleClass('hidden', true);
    $('.step-invite').toggleClass('hidden', false);
};


// Updates the breadcrumb to show the steps that have been already done
PublicDrawCreator.update_breadcrumb = function (target_step){
    var $label_general = $('.breadcrumb-public-draw #general');
    var $label_configure = $('.breadcrumb-public-draw #configure');
    var $label_invite = $('.breadcrumb-public-draw #invite');

    if (target_step == "invite"){

        $label_configure.toggleClass('focus', false);

        $label_invite.toggleClass('focus', true);
        $label_invite.toggleClass('done', true);
        $('.breadcrumb-public-draw').attr('data-current-step', 'invite');
    }
    else{
        if (target_step == "configure"){
            $label_general.toggleClass('focus', false);
            $label_configure.toggleClass('done', true);
            $label_configure.toggleClass('focus', true);
            $('.breadcrumb-public-draw').attr('data-current-step', 'configure');
        }
        else{
            if (target_step == "general"){
                $label_general.toggleClass('focus', true);
                $label_configure.toggleClass('focus', false);
                $label_invite.toggleClass('focus', false);
                $('.breadcrumb-public-draw').attr('data-current-step', 'general');
            }
        }
    }
};

// Initialize the interface for a public draw
PublicDrawCreator.setup = function(){
    $('#btn-configure').click(function () {
        // Validate title and description
        PublicDrawCreator.show_configure_step();
    });
};
