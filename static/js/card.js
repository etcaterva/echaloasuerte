
function Card() {}

/* Pre: the baseUrl has to point to the folder with the images through static files*/
Card.baseUrl = "";
Card.result = 0;
Card.css_class = "col-xs-6 col-sm-4 col-lg-3 card-container";

Card.draw = function(results){
    Card.baseUrl += "img_cards/";
    for (i = 0; i < results.length; i++) {
        img_path = Card.baseUrl + results[i] + ".png";
        string_img = "<div class='" + Card.css_class + "'><img src='" + img_path + "'/></div>";
        document.write(string_img);
    }
}