
var Card = {};

/* Pre: the baseUrl has to point to the folder with the images through static files*/
Card.baseUrl = "";
Card.results = [];
Card.css_class = "card-container ";

Card.setup = function(baseUrl, results){
    Card.baseUrl = baseUrl + "img_cards/";
    Card.results = results;

    switch (Card.results.length) {
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
}

Card.draw = function(){
    document.write("<div class='row'>");
    for (i = 0; i < Card.results.length; i++) {
        var img_path = Card.baseUrl + Card.results[i] + ".png";
        var html = "<div class='" + Card.css_class + "'><img src='" + img_path + "'/></div>";
        document.write(html);
    }
    document.write("</div>");
}