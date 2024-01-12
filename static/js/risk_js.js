// Initialize variables
var hoverButton = document.getElementById('submitButton');
var graph = document.getElementById('graph');
var graphDiv = document.getElementById('graph-div');
var resultText = document.getElementById('risk-result');
var resultBox = document.getElementById('Risk')
var locationInput = document.getElementById('location-input')
var hidden = document.getElementById('hidden')
var mapScript = document.getElementById('mapScript')

//Insert maps API key (In progress)
//mapScript.addEventListener('DOMContentLoaded', function () {
//  mapScript.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyAkqT5NcD8JHNfdPqy2iVWqkLDv9Kl208A&callback=initMap"
//});
//Functions
function showHidden() {
  graph.style.display = 'flex'
  graphDiv.style.display = 'flex'
  resultBox.style.display = 'flex'
};

function changeColors() {
  console.log('Hello World!');
  hoverButton.addEventListener('click', function() {
    hoverButton.style.backgroundColor = '#3498db';
    showHidden();
  });
};

function initMap() {
  // Specify the initial map options (center, zoom, etc.)
  var Map = google.maps.importLibrary("maps");
  var mapOptions = {
    center: { lat: 37.7749, lng: -122.4194 }, // San Francisco, CA
    zoom: 2,
  };
  // Create a new map object and associate it with the "map" div
  var map = new google.maps.Map(document.getElementById('map'), mapOptions);
  // Create a marker and set its position initially to the center of the map
  marker = new google.maps.Marker({
    map: map,
    draggable: true,
    animation: google.maps.Animation.DROP,
    position: { lat: 37.7749, lng: -122.4194 },
    });
  // Add a listener for the dragend event to update the marker's position
  google.maps.event.addListener(marker, 'dragend', function () {
    updateMarkerPosition(marker.getPosition());
  });
  submitButton.addEventListener('click', function () {
    submitMarkerPosition(marker.getPosition())
  });
};
function updateMarkerPosition(latLng) {
  // You can use latLng to get the latitude and longitude of the selected location
  console.log('Selected Location:', latLng.lat(), latLng.lng());
}
function submitMarkerPosition(latLng) {
  //Submits the current latitude and longitude of marker as a string
  lat = latLng.lat().toFixed(6);
  lng = latLng.lng().toFixed(6);
  locale = lat + "," + lng;
  locationInput.value = locale
}

//Actionable Code
if (hidden.innerText == 'show') {
  console.log('Showing hidden');
  showHidden();
};


// Call the initMap function when the Google Maps API is loaded. Should be last line of code
google.maps.event.addDomListener(window, 'load', initMap);


