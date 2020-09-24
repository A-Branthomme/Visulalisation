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
var geojsonFeature = {
    "type": "Feature",
    "properties": {
        "name": "Coors Field",
        "amenity": "Baseball Stadium",
        "popupContent": "This is where the Rockies play!"
    },
    "geometry": {
        "type": "Point",
        "coordinates": [2.333,48.853]
    }
};

L.geoJSON(geojsonFeature).addTo(map);
