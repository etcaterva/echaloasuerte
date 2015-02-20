function SlideSelector () {};

SlideSelector.select_everyone = function (relative_pos_selector){
    $('.slide-bar').attr("data-selected","everyone");
    $('#restriction-everyone').stop(true,true).addClass('restriction-selected', 200);
    $('#restriction-password').stop(true,true).removeClass('restriction-selected', 200);
    $('#restriction-invited').stop(true,true).removeClass('restriction-selected', 200);
    var move = relative_pos_selector + 10;
    $('.slide-selector').animate({"left": "-="+move+"px"}, "slow");
    $('#extra-password').hide();
    $('#extra-invited').hide();
    $('#extra-everyone').show();
}

SlideSelector.select_password = function (slide_bar_width, relative_pos_selector){
    $('.slide-bar').attr("data-selected","password");
    $('#restriction-everyone').stop(true,true).removeClass('restriction-selected', 200);
    $('#restriction-password').stop(true,true).addClass('restriction-selected', 200);
    $('#restriction-invited').stop(true,true).removeClass('restriction-selected', 200);
    var move = slide_bar_width/2 - relative_pos_selector - 10;
    $('.slide-selector').animate({"left": "+="+move+"px"}, "slow");
    $('#extra-everyone').hide();
    $('#extra-invited').hide();
    $('#extra-password').show();

}

SlideSelector.select_invited = function (slide_bar_width, relative_pos_selector){
    $('.slide-bar').attr("data-selected","invited");
    $('#restriction-everyone').stop(true,true).removeClass('restriction-selected', 200);
    $('#restriction-password').stop(true,true).removeClass('restriction-selected', 200);
    $('#restriction-invited').stop(true,true).addClass('restriction-selected', 200);
    var move = slide_bar_width - relative_pos_selector - 10;
    $('.slide-selector').animate({"left": "+="+move+"px"}, "slow");
    $('#extra-everyone').hide();
    $('#extra-password').hide();
    $('#extra-invited').show();
}

SlideSelector.setup = function (){
    $('#extra-password').hide();
    $('#extra-invited').hide();
    $( ".slide-selector" ).draggable({axis: "x", containment: "parent"});
    $('.slide-bar').click(function(e) {
        $slidebar = $('.slide-bar');
        $('.slide-selector').stop(true,true);
        var slide_bar_width = $slidebar.width();
        var pos_slide_bar = $slidebar.offset().left;
        var pos_selector = $('.slide-selector').offset().left;
        var relative_pos_click = e.pageX - pos_slide_bar;
        var relative_pos_selector = pos_selector - pos_slide_bar;
        if (relative_pos_click < slide_bar_width/4){
            SlideSelector.select_everyone(relative_pos_selector);
        }else{
            if (relative_pos_click > 3*slide_bar_width/4){
                SlideSelector.select_invited(slide_bar_width, relative_pos_selector);
            }else {
                SlideSelector.select_password(slide_bar_width, relative_pos_selector);
            }
        }
    });

    $('.slide-selector').mouseup(function (){
        $slidebar = $('.slide-bar');
        $('.slide-selector').stop(true,true);
        var slide_bar_width = $slidebar.width();
        var pos_slide_bar = $slidebar.offset().left;
        var pos_selector = $('.slide-selector').offset().left;
        var relative_pos_selector = pos_selector - pos_slide_bar;
        if (relative_pos_selector < slide_bar_width/4){
            SlideSelector.select_everyone(relative_pos_selector);
        }else{
            if (relative_pos_selector > 3*slide_bar_width/4){
                SlideSelector.select_invited(slide_bar_width, relative_pos_selector);
            }else {
                SlideSelector.select_password(slide_bar_width, relative_pos_selector);
            }
        }
    });
}
