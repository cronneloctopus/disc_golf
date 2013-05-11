var map;
function init() {
  var mapOptions = {
    zoom: 14,
    center: new google.maps.LatLng(courseLat, courseLon),
    mapTypeId: google.maps.MapTypeId.SATELLITE
  };
  map = new google.maps.Map(document.getElementById('map'), mapOptions);
  
  marker = new google.maps.Marker({
    position: new google.maps.LatLng(courseLat, courseLon),
    map: map
  })

}

google.maps.event.addDomListener(window, 'load', initialize);
