//Création du fond de carte
var myLayer = L.tileLayer('http://{s}.tile.stamen.com/toner-lite/{z}/{x}/{y}.png', {
    attribution: 'Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors, CC-BY-SA',
    subdomains: 'abcd',
    minZoom: 0,
    maxZoom: 20
});

//Création de la carte
var map = new L.Map("map", {
    center: new L.LatLng(48.853, 2.333),
    zoom: 13,
    layers: [myLayer]
});

// Ajout de Features à la carte
//Ajout des lignes de métro
$.getJSON("../../Data Paris/Stations/ligne_metro.geojson", function(data) {
  var dataLayer = L.geoJson(data, {
        onEachFeature: function(feature, layer) {
            var popupText = "Ligne: " + feature.properties.route_short_name;
            layer.bindPopup(popupText);
            layer.on({
                mouseover: highlightFeature,
                // mouseout: resetHighlight,
                click: zoomToFeature
            });
          },
        style: function(feature){
          var color = "#" + feature.properties.route_color;
          return{
            color: color
          }
        }
        });
  dataLayer.addTo(map);
  });

//Ajout des Stations

$.getJSON("../../Data Paris/Stations/Data_metro_avec_prix.geojson", function(data) {
  var station_layer = L.geoJson(data, {
        onEachFeature: function(feature, layer) {
            var popupText = "Station: " + feature.properties.nom_gare;
            layer.bindPopup(popupText);
          },
        pointToLayer: createCircles
        });
  station_layer.addTo(map);
  });

  function zoomToFeature(e) {
      map.fitBounds(e.target.getBounds());
  };

  function highlightFeature(e) {
      var layer = e.target;

      layer.setStyle({
          weight: 5,
          color: '#666',
          dashArray: '',
          fillOpacity: 0.7
      });

      if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
          layer.bringToFront();
      }
  };

  function resetHighlight(e) {
};

// create a vector circle centered on each point feature's latitude and longitude
function createCircles(feature, latlng) {
  return L.circleMarker(latlng, {
    color: '#666',
    radius: parseFloat(feature.properties.prix_moyen_2014)/1000
  })
};

var years = [dataLayer, station_layer];
layerGroup = L.layerGroup(years);
var sliderControl = L.Control.SliderControl({
  layer: layerGroup,
  follow: true
});
map.addControl(sliderControl);
sliderControl.startSlider();
