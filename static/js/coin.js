var framenum = 0;
var framecnt = 0;
var flipping = null;
var pict = new Array(3, 4, 1, 4);
var cachedimages = new Array(5);


/* 	choice = 0 (HEAH)
	choice = 2 (TAIL)
*/
function coin() {}

/* Pre: the baseUrl has to point to the folder with the images through static files*/
coin.baseUrl = "";
coin.result = 0;

coin.setup = function () {
    cachedimages[0] = new Image();
    cachedimages[0].src = coin.baseUrl + "head.png";
    cachedimages[1] = new Image();
    cachedimages[1].src = coin.baseUrl + "tail_dist.png";
    cachedimages[2] = new Image();
    cachedimages[2].src = coin.baseUrl + "tail.png";
    cachedimages[3] = new Image();
    cachedimages[3].src = coin.baseUrl + "head_dist.png";
    cachedimages[4] = new Image();
    cachedimages[4].src = coin.baseUrl + "dist.png";
	framecnt = 0;
}


coin.animate = function () {
	framenum = (framecnt) % 4;
	$("#img-coin" ).attr("src", cachedimages[pict[framenum]].src);
	framecnt++;
	if ((framecnt > 8) && (framenum == coin.result)) {
		$("#img-coin" ).attr("src", cachedimages[framenum].src);
		flipping = null;
	}
	else
		flipping = setTimeout("coin.animate()", 30);
}


coin.flip = function () {
    coin.setup()
	coin.animate();
}