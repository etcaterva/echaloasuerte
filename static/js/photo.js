/**
  Given a canvas retrieved from Jquery, draws the photo and points
  as stated in data-url and data-points
**/
function draw_canvas(canvas) {
  var MAX_WIDTH = window.screen.availWidth / 4;
  var ctx = canvas[0].getContext('2d');
  var img = new Image();
  img.onload = function(){
    img_width = this.width;
    img_height = this.height;
    if (img_width > MAX_WIDTH) {
        var resize = img_width / MAX_WIDTH;
        img_width = img_width / resize;
        img_height = img_height / resize;
    }
    canvas.attr('width', img_width);
    canvas.attr('height', img_height);
    ctx.drawImage(img, 0, 0, img_width, img_height);
    var points = canvas.attr('data-points').split(';');
    $.each(points, function(idx, point){
        drawPoint(ctx,
            img_width / 100 * Number(point.split(',')[0]),
            img_height / 100 * Number(point.split(',')[1]));
    });
  };
  img.src = canvas.attr('data-url');
}

/** Draws a point whithin the context of a canvas */
function drawPoint(ctx, x, y) {
    ctx.beginPath();
    ctx.arc(x,y,5,0,2*Math.PI);
    ctx.fillStyle = "red";
    ctx.fill();
}
