var framenum = 0;
var framecnt = 0;
var flipping = null;
var choice = 0;
var pict = new Array(3, 4, 1, 4);
var cachedimages = new Array(5);
cachedimages[0] = new Image();
cachedimages[0].src = "img/head.jpg";
cachedimages[1] = new Image();
cachedimages[1].src = "img/tail_dist.jpg";
cachedimages[2] = new Image();
cachedimages[2].src = "img/tail.jpg";
cachedimages[3] = new Image();
cachedimages[3].src = "img/head_dist.jpg";
cachedimages[4] = new Image();
cachedimages[4].src = "img/dist.jpg";

/* 	choice = 0 (HEAH)
	choice = 2 (TAIL)
*/
function flip_coin(force_choice) {
	framecnt = 0;
	choice = force_choice;
	animate();
}
function animate() {
	framenum = (framecnt) % 4;
	$("#img-coin" ).attr("src", cachedimages[pict[framenum]].src);
	framecnt++;
	if ((framecnt > 8) && (framenum == choice)) {
		$("#img-coin" ).attr("src", cachedimages[framenum].src);
		flipping = null;
	}
	else
		flipping = setTimeout("animate()", 30);
}