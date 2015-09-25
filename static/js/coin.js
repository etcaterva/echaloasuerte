var framenum = 0;
var framecnt = 0;
var pict = new Array(3, 4, 1, 4);
var cachedimages = new Array(5);


var coin = {};

coin.result = 0;

coin.setup = function (baseUrl) {
    cachedimages[0] = new Image();
    cachedimages[0].src = baseUrl + "head.png";
    cachedimages[1] = new Image();
    cachedimages[1].src = baseUrl + "tail_dist.png";
    cachedimages[2] = new Image();
    cachedimages[2].src = baseUrl + "tail.png";
    cachedimages[3] = new Image();
    cachedimages[3].src = baseUrl + "head_dist.png";
    cachedimages[4] = new Image();
    cachedimages[4].src = baseUrl + "dist.png";
    framecnt = 0;
}

coin.animate = function () {
    framenum = (framecnt) % 4;
    $("#img-coin" ).attr("src", cachedimages[pict[framenum]].src);
    framecnt++;
    if ((framecnt > 8) && (framenum == coin.result)) {
        $("#img-coin" ).attr("src", cachedimages[framenum].src);
    } else {
        setTimeout("coin.animate()", 30);
    }
}

coin.flip = function (result) {
    /*     choice = 0 (HEAH)
    choice = 2 (TAIL)
    */
    if (result == "head")
        coin.result = 0
    else
        coin.result = 2
    coin.animate();
}
