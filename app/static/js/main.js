(function() {
  'use strict';

  FastClick.attach(document.body);

  // helper fn to get parent
  function get_parent(el, className, context) {
    while ( el && !el.classList.contains(className) ) {
      el = el.parentNode;

      if ( el === context ) return false;
    }
    return el;
  }

  // map
  var map_el = document.getElementById('map');

  if (typeof(ol) !== undefined && map_el) {
    var latitude = parseFloat(map_el.getAttribute('data-lat')),
        longitude = parseFloat(map_el.getAttribute('data-long'));

    var map = new ol.Map({
      target: 'map',
      controls: [],
      interactions: [],
      layers: [
        new ol.layer.Tile({
          source: new ol.source.Stamen({
            layer: 'watercolor'
          })
        })
      ],
      view: new ol.View({
        center: ol.proj.transform([longitude, latitude], 'EPSG:4326', 'EPSG:3857'),
        zoom: 5
      })
    });
  }

  // image gallery
  function ImageGallery(el) {
    this.el = el;
    this.featured_ratio = 0.6666;
    this.width = this.el.offsetWidth;
  }

  ImageGallery.prototype.getDimensions = function(width, height, containerWidth, containerHeight) {
    var dimensions = {};

    if(width/height < containerWidth/containerHeight) {
      // full height, offset width
      var containerRatio = containerWidth/containerHeight,
          mediaRatio = width/height;

      // now set the variables
      dimensions.left = (1 - mediaRatio/containerRatio)*50 + '%';
      dimensions.top = 0 + '%';
      dimensions.width = mediaRatio/containerRatio * 100 + '%';
      dimensions.height = '100%';
    } else {
      // full width, offset height
      var containerRatio = containerHeight/containerWidth,
          mediaRatio = height/width;

      // now set positioning vars
      dimensions.top = (1 - mediaRatio/containerRatio) * 50 + '%';
      dimensions.left = 0 + '%';
      dimensions.width = '100%';
      dimensions.height = mediaRatio/containerRatio * 100 + '%';
    }

    return dimensions;
  };

  ImageGallery.prototype.update = function(thumb) {
    var old_img = this.featured.querySelector('img'),
        new_image = thumb.getAttribute('href');

    old_img.classList.add('fade-out');
    setTimeout(function() {
      old_img.parentElement.removeChild(old_img);
    }, 600);

    this.set_featured(new_image, thumb.getAttribute('alt'));
    this.el.querySelector('.current').classList.remove('current');
    thumb.classList.add('current');
  };

  ImageGallery.prototype.set_featured = function(src, caption) {
    var self = this;

    var img = document.createElement('img');
    img.classList.add('loading');

    this.featured.appendChild(img);

    img.onload = function() {
      var dimensions = self.getDimensions(this.width, this.height, self.width, self.width*self.featured_ratio);
      img.style.left = dimensions.left;
      img.style.top = dimensions.top;
      img.style.width = dimensions.width;
      img.style.height = dimensions.height;

      img.classList.remove('loading');
    };
    img.src = src;

    // caption
    if (caption) {
      this.caption.classList.remove('hidden');
      this.caption.innerHTML = caption;
    } else {
      this.caption.classList.add('hidden');
    }

  };

  ImageGallery.prototype.create_thumbs = function() {
    var self = this;

    // make thumb array of images
    this.thumbs = [];

    // make thumb container
    var thumb_container = document.createElement('div');
    thumb_container.classList.add('thumbs');

    for (var i = 0; i < this.images.length; i++) {
      var url = this.images[i].replace(/[\.]+(jpg|jpeg|png|gif)/, function(ext) {
        return '_thumb' + ext;
      });
      this.thumbs[i] = url;

      // make thumbnail
      var thumbnail = document.createElement('a');
      thumbnail.setAttribute('href', this.images[i]);
      if (this.captions && this.captions[i])
        thumbnail.setAttribute('alt', this.captions[i]);
      thumbnail.classList.add('thumbnail');
      if (i === 0) {
        thumbnail.classList.add('current');
      }
      thumbnail.innerHTML = '<img src="' + url + '">';

      // add thumb to container
      thumb_container.appendChild(thumbnail);
    }

    thumb_container.addEventListener('click', function(e) {
      var clicked_thumb = get_parent(e.target, 'thumbnail', thumb_container);
      if (clicked_thumb) {
        e.preventDefault();
        console.log ('clicked thumb');

        if (clicked_thumb.classList.contains('current')) return;

        // update featured image
        self.update(clicked_thumb);
      }
    });
    
    this.el.appendChild(thumb_container);
    console.log(this.thumbs);
  };

  ImageGallery.prototype.init = function() {
    var image_data = this.el.getAttribute('data-images');
    this.images = image_data.split(', ');

    var caption_data = this.el.getAttribute('data-captions');
    this.captions = [];
    if (caption_data) this.captions = caption_data.split(', ');

    this.featured = document.createElement('div');
    this.featured.classList.add('featured-image');
    this.el.appendChild(this.featured);

    this.caption = document.createElement('div');
    this.caption.classList.add('caption');
    this.featured.appendChild(this.caption);

    this.set_featured(this.images[0], this.captions[0]);
    this.create_thumbs();
  };

  var gallery = document.querySelectorAll('.image-gallery');
  for (var g = 0; g < gallery.length; g++) {
    var image_gallery = new ImageGallery(gallery[g]);
    image_gallery.init();
  }

})();