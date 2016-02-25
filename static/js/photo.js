/**
  Given a canvas retrieved from Jquery, draws the photo and points
  as stated in data-url and data-points
**/
function draw_canvas(canvas) {
  var MAX_WIDTH = canvas.parent().width();
  if (!canvas.is('#canvas-photo-main')){
	  // If the canvas is in the history make it smaller to fit in the accordion
	  MAX_WIDTH *= 0.8;
  }
  var ctx = canvas[0].getContext('2d');
  var img = new Image();
  img.onload = function(){
    var img_width = this.width;
    var img_height = this.height;

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


/*globals $, jQuery, CSPhotoSelector */

$(document).ready(function () {
	var selector, callbackAlbumSelected, callbackPhotoUnselected, callbackSubmit;
	var buttonOK = $('#CSPhotoSelector_buttonOK');
	var o = this;


	/* --------------------------------------------------------------------
	 * Photo selector functions
	 * ----------------------------------------------------------------- */

	fbphotoSelect = function(id) {
		// if no user/friend id is sent, default to current user
		if (!id) id = 'me';

		callbackAlbumSelected = function(albumId) {
			var album, name;
			album = CSPhotoSelector.getAlbumById(albumId);
			// show album photos
			selector.showPhotoSelector(null, album.id);
		};

		callbackAlbumUnselected = function(albumId) {
			var album, name;
			album = CSPhotoSelector.getAlbumById(albumId);
		};

		callbackPhotoSelected = function(photoId) {
			var photo;
			photo = CSPhotoSelector.getPhotoById(photoId);
			buttonOK.show();
		};

		callbackPhotoUnselected = function(photoId) {
			var photo;
			album = CSPhotoSelector.getPhotoById(photoId);
			buttonOK.hide();
		};

		callbackSubmit = function(photoId) {
			var photo;
			photo = CSPhotoSelector.getPhotoById(photoId);
			$('#id_photo_url').val(photo.source).trigger('change');
		};


		// Initialise the Photo Selector with options that will apply to all instances
		CSPhotoSelector.init({debug: true});

		// Create Photo Selector instances
		selector = CSPhotoSelector.newInstance({
			callbackAlbumSelected	: callbackAlbumSelected,
			callbackAlbumUnselected	: callbackAlbumUnselected,
			callbackPhotoSelected	: callbackPhotoSelected,
			callbackPhotoUnselected	: callbackPhotoUnselected,
			callbackSubmit			: callbackSubmit,
			maxSelection			: 1,
			albumsPerPage			: 6,
			photosPerPage			: 200,
			autoDeselection			: true
		});

		// reset and show album selector
		selector.reset();
		selector.showAlbumSelector(id);
	}

	fetch_fb_photos = function(){
		FB.login(function (response) {
			if (response.authResponse) {
				fbphotoSelect();
			}
		}, {scope:'user_photos'});
	};
});
