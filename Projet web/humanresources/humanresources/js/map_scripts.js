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
$.getJSON("./api/stations_data_clean.csv", function (data) {
  console.log(data);

});
// Ajout de Features à la carte
//Ajout des lignes de métro
$.getJSON("./api/ligne_metro.geojson", function (data) {

  var dataLayer = L.geoJson(data, {
    onEachFeature: function (feature, layer) {
      var popupText = "Ligne: " + feature.properties.route_short_name;
      layer.bindPopup(popupText);
      layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
      });
    },
    style: function (feature) {
      var color = "#" + feature.properties.route_color;
      return {
        color: color
      }
    }
  });
  dataLayer.addTo(map);
});

//Ajout des Stations
$.getJSON("./api/Data_metro_avec_prix.geojson", function (data) {
  var station_layer = L.geoJson(data, {
    onEachFeature: function (feature, layer) {
      var popupText = "Station: " + feature.properties.nom_gare + "<br>Prix : " + feature.properties.prix_moyen_2014 + " €/m²";
      layer.bindPopup(popupText);
      layer.on({
        mouseover: highlightStation
      });
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

  console.log(e);


  layer.setStyle({
    weight: 5,
    color: '#F00',
    dashArray: '',
    fillOpacity: 0.7
  });

  if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
    layer.bringToFront();
  }
};

function highlightStation(e) {
  console.log(e);
  
}

function resetHighlight(e) {
  var layer = e.target;
  var color = "#" + layer.feature.properties.route_color;

  layer.setStyle({
    weight: 3,
    color: color,
    dashArray: '',
    fillOpacity: 0.7
  });

};

// create a vector circle centered on each point feature's latitude and longitude
function createCircles(feature, latlng) {
  return L.circleMarker(latlng, {
    color: '#666',
    radius: parseFloat(feature.properties.prix_moyen_2014) / 1000
  })
};

var markersClusterCustomPlus = new L.MarkerClusterGroup({
  iconCreateFunction: function (cluster) {
    var digits = (cluster.getChildCount() + '').length;
    return L.divIcon({
      html: cluster.getChildCount(),
      className: 'cluster digits-' + digits,
      iconSize: null
    });
  }
});

// var years = [dataLayer, station_layer];
// layerGroup = L.layerGroup(years);
// var sliderControl = L.Control.SliderControl({
//   layer: layerGroup,
//   follow: true
// });
// map.addControl(sliderControl);
// sliderControl.startSlider();