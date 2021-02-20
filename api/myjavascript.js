
var torArray = [];
var tor0Array = [];
var tor1Array = [];
var tor2Array = [];
var tor3Array = [];
var tor4Array = [];
var tor5Array = [];
var map;

function initialize() {
//	https://developers.google.com/maps/documentation/javascript/controls
	var myOptions = {
		zoom: 5,
		center: new google.maps.LatLng(39.8282, -98.5795),
		mapTypeControl: true,
		mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU},
		navigationControl: true,	
//		mapTypeId: google.maps.MapTypeId.ROADMAP//SATELLITE//HYBRID
		mapTypeId: google.maps.MapTypeId.TERRAIN
	}
	map = new google.maps.Map(document.getElementById("map_canvas"), myOptions)
	
//	pretty cool stuff you can do with the marker
//	https://developers.google.com/maps/documentation/javascript/events
//	drag and drop, UI, etc
	


//	google.maps.event.addListener(map, 'click', function() {  //turn on click 
//       infowindow.close();
// 	});
	


//	set markers where for what 
	setMarkers(map, tor, 'tor');
	}
	  
//	function createMarker(map, latlng, data, comment, color, type) {
function createMarker(map, latlng, EFscale,died,moneyloss) {
    var contentString = '<p align="left">'+EFscale+' '+died+'</p>';
    var marker = new google.maps.Marker({
        position: latlng,
        map: map,
//		icon: getMarkerImage(color),
//		shape: iconShape,
// 	    title: comment,
        zIndex: Math.round(latlng.lat()*-100000)<<5
//		Still dont know what this does but found it here 
//			http://stackoverflow.com/questions/19150033/introduce-z-index-as-a-variable-within-xml-data-for-atributes-relating-to-marker
        });
//			http://stackoverflow.com/questions/18902361/marker-shadows-in-google-maps-v3
//			http://stackoverflow.com/questions/19786986/bind-marker-with-polygon-vertices-google-mapv3/19796316#19796316
        torArray.push(marker); 
//			https://developers.google.com/maps/documentation/javascript/examples/marker-remove
	
//			https://developers.google.com/maps/documentation/javascript/events
//			add stuff like double-click and mouseover
    google.maps.event.addListener(marker, 'click', function() {
        infowindow.setContent(contentString); 
        infowindow.open(map,marker);
        });
	}

var tor0= [];
var tor1= [];
var tor2= [];
var tor3= [];
var tor4= [];
var tor5= [];

var report = [];
var efscales = [];
var losses = [];
var torpath1 = [];
var torpath2 = [];
var torpath3 = [];
var torpath4 = [];
var torpath5 = [];
// 	Add markers to the map
function setMarkers(map, locations, EFscale) {
	for (var i = 0; i < locations.length; i++) {
   		report = locations[i];
//		var startLatLng = new google.maps.LatLng(report[0], report[1]);
//		var endLatLng = new google.maps.LatLng(report[2], report[3]);
//	  	var combine = [startLatLng,endLatLng] // or use ...
		var combine = [{lat: report[0], lng: report[2]},{lat: report[1], lng: report[3]}];
//		var marker = createMarker(map,combine,report[6]);
		efscales = report[4];
		losses = report [5];

//		for each statement in range ([0],[5]) might work here better
       
		if (tor0){
            if (efscales == 0) {
				torpath0 = new google.maps.Polyline({
					path: (combine),
               	    geodesic: true,
               	    strokeColor: '#AA00FF',
                 	strokeOpacity: 1.0,
               	    strokeWeight: 1
                });
      	    torpath0.setMap(map);
			tor0Array.push(torpath0);
  	     	}
		}
		if (tor1){
            if (efscales == 1) {
				torpath1 = new google.maps.Polyline({
					path: (combine),
					geodesic: true,
					strokeColor: '#0000FF',
					strokeOpacity: 1.0,
					strokeWeight: 1.5
	   			});
			torpath1.setMap(map);
			tor1Array.push(torpath1);
			}
		}
		if (tor2){
            if (efscales == 2) {
				torpath2 = new google.maps.Polyline({
    		    	path: (combine),
					geodesic: true,
					strokeColor: '#59E817',
					strokeOpacity: 1.0,
					strokeWeight: 2.0
    			});
			torpath2.setMap(map);
			tor2Array.push(torpath2);
			}
    	}
		if (tor3){
            if (efscales == 3) {
    			torpath3 = new google.maps.Polyline({
					path: (combine),
					geodesic: true,
					strokeColor: '#e6e600',
					strokeOpacity: 1.0,
					strokeWeight: 2.5
    			});
			torpath3.setMap(map);
			tor3Array.push(torpath3);
			}
    	}
		if (tor4){
            if (efscales == 4) {
    			torpath4 = new google.maps.Polyline({
					path: (combine),
					geodesic: true,
					strokeColor: '#F87217',
					strokeOpacity: 1.0,
					strokeWeight: 3.0
				});
			torpath4.setMap(map);
			tor4Array.push(torpath4);
    		}
    	}
		if (tor5){
            if (efscales == 5) {
    			torpath5 = new google.maps.Polyline({
	 				path: (combine),
					geodesic: true,
					strokeColor: '#FF0000',
					strokeOpacity: 1.0,
					strokeWeight: 3.5
				});
			torpath5.setMap(map);
			tor5Array.push(torpath5);
			}
		}
  	}
}

//	});
//	Remove tornado reports from the map, but keep them in the array
//	function clearInput(element){
//	element.value="";
//	}
//	http://stackoverflow.com/questions/15969307/how-to-clear-textbox-on-html-using-javascript

 
function EF0() {
    for (i in tor0Array) {
        tor0Array[i].setMap(null);
  	}
}
function EF1() { 				
	for (i in tor1Array) {
    	tor1Array[i].setMap(null);
	}
}
function EF2() {
    for (i in tor2Array) {
       tor2Array[i].setMap(null);
  	}
}
function EF3() {
    for (i in tor3Array) {
        tor3Array[i].setMap(null);
 	}
}	
function EF4() {
    for (i in tor4Array) {
        tor4Array[i].setMap(null);
  	}
}
function EF5() {
    for (i in tor5Array) {
        tor5Array[i].setMap(null);
  	}
}

//  Shows any overlays currently in the array
function showOverlays() {
    for (i in tor0Array) {
        tor0Array[i].setMap(map);
    }
	for (i in tor1Array) {
        tor1Array[i].setMap(map);
    }
	for (i in tor2Array) {
        tor2Array[i].setMap(map);
    }
	for (i in tor3Array) {
        tor3Array[i].setMap(map);
    }
	for (i in tor4Array) {
        tor4Array[i].setMap(map);
    }
	for (i in tor5Array) {
        tor5Array[i].setMap(map);
    }
}