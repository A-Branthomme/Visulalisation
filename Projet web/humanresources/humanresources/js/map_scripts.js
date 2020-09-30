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
var station1 =
  {
    "type":"Feature",
    "properties":{
      "ID":"1842",
      "STATION":"GARE DU NORD",
      "CITY":"Paris",
      "QUARTER":"10",
      "TRAFIC":"49977513",
      "LINES":"4-5",
      "COLORS":"#BB4D98-#DE8B53"
      },
      "geometry":{
        "type":"Point",
        "coordinates":[
           2.35470307836603,
           48.8799654432891
        ]
      }
  };

  var station2 =
    {
      "type":"Feature",
      "properties":{
        "ID":"1842",
        "STATION":"GARE DU NORD",
        "CITY":"Paris",
        "QUARTER":"10",
        "TRAFIC":"49977513",
        "LINES":"4-5",
        "COLORS":"#BB4D98-#DE8B53"
        },
        "geometry":{
          "type":"Point",
          "coordinates":[
             2.36470307836603,
             48.8799654432891
          ]
        }
    };

// L.geoJSON(station).addTo(map);

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
}

  var years = [station1, station2];
  layerGroup = L.layerGroup(years);
  var sliderControl = L.Control.SliderControl({
    layer: layerGroup,
    follow: true
  });
  map.addControl(sliderControl);
  sliderControl.startSlider();
