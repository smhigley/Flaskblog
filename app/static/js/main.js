(function() {
  'use strict';

  FastClick.attach(document.body);

  var map_el = document.getElementById('map'),
      latitude = parseFloat(map_el.getAttribute('data-lat')),
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

})();