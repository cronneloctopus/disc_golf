// init function to generate open layers map
function init() {
    if (courseLat != undefined && courseLon != undefined) {
        var lat            = courseLat;
        var lon            = courseLon;
        var zoom           = 14;

        var fromProjection = new OpenLayers.Projection("EPSG:4326");   // Transform from WGS 1984
        var toProjection   = new OpenLayers.Projection("EPSG:900913"); // to Spherical Mercator Projection
        var position       = new OpenLayers.LonLat(lon, lat).transform(fromProjection, toProjection);

        map = new OpenLayers.Map("map");
        var mapnik = new OpenLayers.Layer.OSM();
        map.addLayer(mapnik);

        var markers = new OpenLayers.Layer.Markers( "Markers" );
        map.addLayer(markers);
        markers.addMarker(new OpenLayers.Marker(position));

        map.setCenter(position, zoom);
    } else {
        $(document).ready(function() {
            $('#map').html('No Map Data');
        });
   };
};