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
$.getJSON("./api/ligne_metro.geojson", function (data) {

  var dataLayer = L.geoJson(data, {
    onEachFeature: function (feature, layer) {
      var popupText = "Ligne: " + feature.properties.route_short_name;
      layer.bindPopup(popupText);
      layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlightLigne,
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

//Load du geojson des stations
var json = (function() {
  var json = null;
  $.ajax({
    'async': false,
    'global': false,
    'url': "./api/Data_metro_avec_prix.geojson",
    'dataType': "json",
    'success': function(data) {
      json = data;
    }
  });
  return json;
})();

//Variable gérant le coefficient de taille des Cercles
let zoom = 1500

//Ajout des Stations 2014
var station_layer_2014 = L.geoJson(json, {
  onEachFeature: function (feature, layer) {
    var popupText = "<b>Station : </b>" + feature.properties.nom_gare + "<br><b>Prix 2014 : </b>" + Number(parseFloat(feature.properties.prix_moyen_2014).toFixed(2))+" €/m²";
    layer.bindPopup(popupText);
    layer.on({
      mouseover: highlightStation,
      mouseout: resetHighlightStation
    });
  },
  pointToLayer: function createCircles(feature, latlng) {
    return L.circleMarker(latlng, {
      color: '#666',
      radius: parseFloat(feature.properties.prix_moyen_2014) / zoom
    })
  }
});
station_layer_2014.addTo(map);

//Ajout des Stations 2015
var station_layer_2015 = L.geoJson(json, {
  onEachFeature: function (feature, layer) {
    var popupText = "<b>Station : </b>" + feature.properties.nom_gare + "<br><b>Prix 2015 : </b>" + Number(parseFloat(feature.properties.prix_moyen_2015).toFixed(2))+" €/m²";
    layer.bindPopup(popupText);
    layer.on({
      mouseover: highlightStation,
      mouseout: resetHighlightStation
    });
  },
  pointToLayer: function createCircles(feature, latlng) {
    return L.circleMarker(latlng, {
      color: '#666',
      radius: parseFloat(feature.properties.prix_moyen_2015) / zoom
    })
  }
});
station_layer_2015.addTo(map);

//Ajout des Stations 2016
var station_layer_2016 = L.geoJson(json, {
  onEachFeature: function (feature, layer) {
    var popupText = "<b>Station : </b>" + feature.properties.nom_gare + "<br><b>Prix 2016 : </b>" + Number(parseFloat(feature.properties.prix_moyen_2016).toFixed(2))+" €/m²";
    layer.bindPopup(popupText);
    layer.on({
      mouseover: highlightStation,
      mouseout: resetHighlightStation
    });
  },
  pointToLayer: function createCircles(feature, latlng) {
    return L.circleMarker(latlng, {
      color: '#666',
      radius: parseFloat(feature.properties.prix_moyen_2016) / zoom
    })
  }
});
station_layer_2016.addTo(map);

//Ajout des Stations 2017
var station_layer_2017 = L.geoJson(json, {
  onEachFeature: function (feature, layer) {
    var popupText = "<b>Station : </b>" + feature.properties.nom_gare + "<br><b>Prix 2017 : </b>" + Number(parseFloat(feature.properties.prix_moyen_2017).toFixed(2))+" €/m²";
    layer.bindPopup(popupText);
    layer.on({
      mouseover: highlightStation,
      mouseout: resetHighlightStation
    });
  },
  pointToLayer: function createCircles(feature, latlng) {
    return L.circleMarker(latlng, {
      color: '#666',
      radius: parseFloat(feature.properties.prix_moyen_2017) / zoom
    })
  }
});
station_layer_2017.addTo(map);

//Ajout des Stations 2018
var station_layer_2018 = L.geoJson(json, {
  onEachFeature: function (feature, layer) {
    var popupText = "<b>Station : </b>" + feature.properties.nom_gare + "<br><b>Prix 2018: </b>" + Number(parseFloat(feature.properties.prix_moyen_2018).toFixed(2))+" €/m²";
    layer.bindPopup(popupText);
    layer.on({
      mouseover: highlightStation,
      mouseout: resetHighlightStation
    });
  },
  pointToLayer: function createCircles(feature, latlng) {
    return L.circleMarker(latlng, {
      color: '#666',
      radius: parseFloat(feature.properties.prix_moyen_2018) / zoom
    })
  }
});
station_layer_2018.addTo(map);

//Ajout des Stations 2019
var station_layer_2019 = L.geoJson(json, {
  onEachFeature: function (feature, layer) {
    var popupText = "<b>Station : </b>" + feature.properties.nom_gare + "<br><b>Prix 2019 : </b>" + Number(parseFloat(feature.properties.prix_moyen_2019).toFixed(2)) +" €/m²";
    layer.bindPopup(popupText);
    layer.on({
      mouseover: highlightStation,
      mouseout: resetHighlightStation
    });
  },
  pointToLayer: function createCircles(feature, latlng) {
    return L.circleMarker(latlng, {
      color: '#666',
      radius: parseFloat(feature.properties.prix_moyen_2019) / zoom
    })
  }
});
station_layer_2019.addTo(map);

var baseMaps = {
    "Background": myLayer,
};

var overlayMaps = {
    "2014": station_layer_2014,
    "2015": station_layer_2015,
    "2016": station_layer_2016,
    "2017": station_layer_2017,
    "2018": station_layer_2018,
    "2019": station_layer_2019,

};

L.control.layers(baseMaps, overlayMaps).addTo(map);

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
  var layer = e.target;

  console.log(e);

  layer.setStyle({
    color :'#F00'
  });


}

function resetHighlightStation(e) {
  var layer = e.target;
  var color = "#" + layer.feature.properties.route_color;

  layer.setStyle({
    color: '#666'
  });

};

function resetHighlightLigne(e) {
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
    radius: parseFloat(feature.properties.prix_moyen_2014) / 1800
  })
};


var years = [station_layer_2014, station_layer_2015];
layerGroup = L.layerGroup(years);
var sliderControl = L.Control.SliderControl({
  layer: layerGroup,
  follow: true
});
map.addControl(sliderControl);
sliderControl.startSlider();
