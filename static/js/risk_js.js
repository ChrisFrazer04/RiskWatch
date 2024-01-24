// Initialize variables
var hoverButton = document.getElementById('submitButton');
var graph = document.getElementById('graph');
var graphDiv = document.getElementById('graph-div');
var resultText = document.getElementById('risk-result');
var resultBox = document.getElementById('Risk')
var locationInput = document.getElementById('location-input')
var hidden = document.getElementById('hidden')
var mapScript = document.getElementById('mapScript')
var resultsDetailed = document.getElementById('results-detailed')
var riskLevel = document.getElementById('riskLevel')
var detailedToggle = document.getElementById('detailedToggle')
var factors = document.getElementById('factors')
var reference = document.getElementById('reference')
var bottomDivider = document.getElementById('bottomDivider')
var riskColon = document.getElementById('riskColon')
var supportedToggle = document.getElementById('supportedToggle')
var percentile = document.getElementById('percentile')
var percentileHeader = document.getElementById('percentileHeader')
var factorHeader = document.getElementById('factorHeader')
//Insert maps API key (In progress)
//mapScript.addEventListener('DOMContentLoaded', function () {
//  mapScript.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyAkqT5NcD8JHNfdPqy2iVWqkLDv9Kl208A&callback=initMap"
//});

//Functions
function showHidden() {
  graph.style.display = 'flex';
  graphDiv.style.display = 'flex';
  resultText.style.display = 'flex';
  riskLevel.style.display = 'flex';
  detailedToggle.style.display = 'flex';
  bottomDivider.style.display = 'flex';
};

function showHidden2() {
  resultsDetailed.style.display = 'flex';
  resultText.style.display = 'flex';
  bottomDivider.style.display = 'flex';
  supportedToggle.style.display = 'flex'
  riskColon.style.display = 'none';
  //supportedText.style.display = 'flex';
}

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
    center: { lat: 32.2761, lng: -41.0330 },
    zoom: 3,
  };
  // Create a new map object and associate it with the "map" div
  var map = new google.maps.Map(document.getElementById('map'), mapOptions);
  // Create a marker and set its position initially to the center of the map
  marker = new google.maps.Marker({
    map: map,
    draggable: true,
    animation: google.maps.Animation.DROP,
    position: {lat: 38.5586, lng: -77.0817},
    });
  // Add a listener for the dragend event to update the marker's position
  google.maps.event.addListener(map, 'mouseup', function (event) {
    marker.setPosition(event.latLng);
    updateMarkerPosition(event.latLng)
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

function toggleDetails (){
    var toggleClass = detailedToggle.classList.value;
    detailedToggle.addEventListener('click', function () {
        resultsDetailed.classList.toggle('bordered');
        percentile.classList.toggle('hidden');
        detailedToggle.classList.toggle('closed');
        factors.classList.toggle('hidden');
        reference.classList.toggle('hidden');
        factorHeader.classList.toggle('hidden');
        percentileHeader.classList.toggle('hidden');
        //console.log(detailedToggle.classList.value);
        if (detailedToggle.classList.value != 'closed') {
            detailedToggle.innerHTML = 'Detailed Analysis: &#x25B4;';
        }
        else {
            detailedToggle.innerHTML = 'Detailed Analysis: &#x25BE;';
        }
})
}

function toggleSupported (){
    supportedToggle.addEventListener('click', function () {
        resultsDetailed.classList.toggle('bordered');
        supportedToggle.classList.toggle('closed');
        percentile.classList.toggle('hidden');
        if (supportedToggle.classList.value != 'closed') {
            supportedToggle.innerHTML = 'Supported Countries &#x25B4;';
        }
        else {
            supportedToggle.innerHTML = 'Supported Countries &#x25BE;';
        }
})
}

//Actionable Code
if (hidden.innerText == 'show') {
  showHidden();
  toggleDetails();
};

if (hidden.innerText == 'show2') {
    showHidden2();
    toggleSupported();
    console.log('Showing hidden 2');
};

if (hidden.innerText == 'show3') {
    riskLevel.style.display = 'flex';
    bottomDivider.style.display = 'flex';
    resultText.style.display = 'flex';
    riskColon.style.display = 'none';
}

if (riskLevel.innerText == 'Very High') {
    riskLevel.style.color = '#D80C0C';
};
if (riskLevel.innerText == 'High') {
    riskLevel.style.color = '#D8510C';
};
if (riskLevel.innerText == 'Moderate') {
    riskLevel.style.color = '#D8D20C';
};
if (riskLevel.innerText == 'Low') {
    riskLevel.style.color = '#82D80C';
};
if (riskLevel.innerText == 'Very Low') {
    riskLevel.style.color = '#3DD80C';
};
if (riskLevel.innerText == 'Minimal') {
    riskLevel.style.color = '#07A01F';
};
if (riskLevel.innerText == 'None') {
    riskLevel.style.color = '#2A8FCE';
};

// Call the initMap function when the Google Maps API is loaded. Should be last line of code
google.maps.event.addDomListener(window, 'load', initMap);


