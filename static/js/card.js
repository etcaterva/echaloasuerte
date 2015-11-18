var Card = {};

/* Pre: the baseUrl has to point to the folder with the images through static files*/
Card.baseUrl = "";
Card.css_class = "card-container ";

Card.draw = function(results){
    // Set widths based on the number of cards to show
    switch (results.length) {
        case 1:
            Card.css_class += "col-xs-12";
            break;
        case 2:
            Card.css_class += "col-xs-6";
            break;
        case 3:
            Card.css_class += "col-xs-6 col-sm-4";
            break;
        default:
            Card.css_class += "col-xs-6 col-sm-3";
            break;
    }


    var render_html = "<div class='row'>";
    for (var i = 0; i < results.length; i++) {
        var img_path = Card.baseUrl + results[i] + ".png";
        var html = "<div class='" + Card.css_class + "'><img src='" + img_path + "' alt='card"+results[i]+"'/></div>";
        render_html += html;
    }
    render_html += "</div>";
    return render_html;
};