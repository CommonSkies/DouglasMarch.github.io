#!/usr/local/epd-7.2-2-rh5-x86_64/bin/python
#SPCRPTS.PY
###########################################################
#The purpose of this script is to save time parsing SPC
#storm reports into the format required for creating
#markers in Google Maps.  The script will read a comma-
#delimited list of storm reports and write the necessary
#Javascript/HTML hybrid for making the markers.
#
#You may also wish to expand upon this script to have it
#write out your entire Google maps Javascript.  That's what
#I did and it's what I recommend to you.  Of course, you can
#always just type in the storm reports by hand if have
#nothing better to do with your time...
#
#Please see the comments throughout this script.
#
#Christopher M. Godfrey						   12 July 2010
#Modified 5 May 2011
###########################################################
#Import a bunch of stuff that you may or may not need
import sys,urllib2,os,cgi,time,glob,math,string,re
import datetime
#If you decide to make this script interact with a Web browser, uncomment the next lines
import cgitb; cgitb.enable()		#Gives nicely-formatted error messages
print "Content-type: text/html\n"  #Required first line to send to client for debugging
#This is the file that you want to read:
reports='Actual_tornadoes.csv'
###########################################################
#YOUR TURN (1 of 3):
#It's possible to have this script write out your entire Javascript code!
#Then you can include that script as an external file by placing the
#following in your HTML <head> section, along with any other HTML in
#that section:
#<head>
#  <script type="text/javascript" src="your_javascript.js"></script>
#</head>
#Open your external Javascript file for writing
java=open("myjavascript.js","w")
#Write the first part of your Javascript here.  Enclose
#everything in triple quotes.
#make sure that the arrays are declared before initialize
java.write(
'''
var torArray = [];
function initialize() {
//https://developers.google.com/maps/documentation/javascript/controls
	var myOptions = {
		zoom: 5,
		center: new google.maps.LatLng(39.8282, -98.5795),
		mapTypeControl: true,
		mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU},
		navigationControl: true,	
		//mapTypeId: google.maps.MapTypeId.ROADMAP//SATELLITE//HYBRID
		mapTypeId: google.maps.MapTypeId.TERRAIN
	}
	var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions)
//	var marker = new google.maps.Marker({
//  The below line is equivalent to writing:
//  position: new google.maps.LatLng(-34.397, 150.644)
//  position: {lat: 35.616, lng: 150.644},
//  https://developers.google.com/maps/documentation/javascript/markers
	
	//pretty cool stuff you can do with the marker
	//https://developers.google.com/maps/documentation/javascript/events
	//drag and drop, UI, etc
	
	google.maps.event.addListener(map, 'click', function() {  //turn on click 
       infowindow.close();
 	});
	//set markers where for what 
	setMarkers(map, tor, 'tor');
	}
	
// Data for the markers consisting of a name, a LatLng and a zIndex for the
// order in which these markers should display on top of each other. 
	  
	  
//var icons = new Array();
//icons["red"] = new google.maps.MarkerImage ("http://blizzard.atms.unca.edu/~cgodfrey/advcomp/maps/images/marker_red.png",   
		// This marker [image] is 20 pixels wide by 34 pixels tall.
		// press F12 and look under elements in Chrome 
//      new google.maps.Size(20, 34),
		// The origin for this image is 0,0.
		// center the image
//      new google.maps.Point(0,0),
		// The anchor for this image is the base of the balloon at 0,32.
		//Origins, anchor positions and coordinates of the marker increase in the X
		// direction to the right and in the Y direction down.
		//https://developers.google.com/maps/documentation/javascript/examples/icon-complex   
//	  new google.maps.Point(10, 34)); 
	
//function getMarkerImage(iconColor) {
//   if ((typeof(iconColor)=="undefined") || (iconColor==null)) { 
		//assign a color for all non color by looping
//     iconColor = "red"; 
//   }
//   if (!icons[iconColor]) {
//      icons[iconColor] = new google.maps.MarkerImage("http://blizzard.atms.unca.edu/~cgodfrey/advcomp/maps/images/marker_"+ iconColor +".png",
		// This marker is 20 pixels wide by 34 pixels tall.
//      new google.maps.Size(20, 34),
		// The origin for this image is 0,0.
//      new google.maps.Point(0,0),
		// The anchor for this image is the base of the flagpole at 0,32.
//      new google.maps.Point(10, 34));
//   } 
//   return icons[iconColor];
//}
  // Marker sizes are expressed as a Size of X,Y
  // where the origin of the image (0,0) is located
  // in the top left of the image.
  //****
//https://developers.google.com/maps/documentation/javascript/examples/icon-complex
  //****
  // Origins, anchor positions and coordinates of the marker
  // increase in the X direction to the right and in
  // the Y direction down.
//var iconImage = new google.maps.MarkerImage('http://blizzard.atms.unca.edu/~cgodfrey/advcomp/maps/images/marker_red.png',
		// This marker is 20 pixels wide by 34 pixels tall.
//      new google.maps.Size(20, 34),
		// The origin for this image is 0,0.
//      new google.maps.Point(0,0),
		// The anchor for this image is the base of the flagpole at 0,32.
//      new google.maps.Point(10, 34));
	  
	  
		// Shapes define the clickable region of the icon.
		// The type defines an HTML &lt;area&gt; element 'poly' which
		// traces out a polygon as a series of X,Y points. The final
		// coordinate closes the poly by connecting to the first
		// coordinate.
//  var iconShape = {
//      coord: [1,1,1,20,18,20,18,1],
//      type: 'poly'
//   };
var infowindow = new google.maps.InfoWindow(
  { 
    size: new google.maps.Size(150,50)
  });
  
//function createMarker(map, latlng, data, comment, color, type) {
function createMarker(map, latlng, EFscale,died,moneyloss) {
    var contentString = '<p align="left">'+EFscale+' '+died+'</p>';
    var marker = new google.maps.Marker({
        position: latlng,
        map: map,

    //    icon: getMarkerImage(color),

      //  shape: iconShape,
      //  title: comment,
        zIndex: Math.round(latlng.lat()*-100000)<<5
			//Still dont know what this does but found it here 
			//http://stackoverflow.com/questions/19150033/introduce-z-index-as-a-variable-within-xml-data-for-atributes-relating-to-marker
        });
			//http://stackoverflow.com/questions/18902361/marker-shadows-in-google-maps-v3
			//http://stackoverflow.com/questions/19786986/bind-marker-with-polygon-vertices-google-mapv3/19796316#19796316
        torArray.push(marker); 
			//https://developers.google.com/maps/documentation/javascript/examples/marker-remove
	
//https://developers.google.com/maps/documentation/javascript/events
// add stuff like double-click and mouseover
    google.maps.event.addListener(marker, 'click', function() {
        infowindow.setContent(contentString); 
        infowindow.open(map,marker);
        });
	}
''')	
###########################################################
#Open and read the SPC comma-delimited storm reports file
file=open(reports,'r')
lines=file.readlines()
#Initialize type of report
type="None"
#Initialize marker variables
tor=""
#Loop through the reports and parse the data
for line in lines:
	cols=line.split(',')
	dummy = int(1)
	#Leave out the headers and determine type of report (always tor, wind, hail in order)
	if cols[15]=="0" or cols[16]=="0" or cols[17]=="0" or cols[18]=="0":	#Eliminate latlon with 0
		dummy = 0
	if dummy == 1:
		ytd=cols[0]
		year=cols[1]
		mon=cols[2]
		day=cols[3]
		ymd=cols[4]
		time=cols[5]
		EFscale=cols[10]
		died=cols[12]
		moneyloss=cols[13]
		startlat=cols[15]
		endlat=cols[16]
		startlon=cols[17]
		endlon=cols[18]
		comment=cols[28].strip()	#Must remove carriage lreturn
		#Fix weird values
		if ytd=="9999": ytd="Unknown"
    ###########################################################
	#YOUR TURN AGAIN (2 of 3):
	#Now we can write the necessary code for our markers! (Copy and modify this for tor, wind, & hail)
	#You may need to change this to match your version of your Google maps Javascript code, but this
	#works with mine.
		tor=tor+'''['''+startlat+''', '''+startlon+''', '''+endlat+''', '''+endlon+''', '''+EFscale+''', '''+moneyloss+''', "<b>Time:</b> '''+ymd+''','''+time+''', UTC<br><b>EF-Scale</b> '''+EFscale+'''<br><b>Fatality:</b> '''+died+'''"],'''
###########################################################
#Write the storm reports to the Javascript
java.write('''
var tor= ['''+tor+'''];
''')
###########################################################
#YOUR TURN ONE MORE TIME (3 of 3):
#Close out the Javascript; put the rest of your Javascript here!
java.write('''

var report = [];
var efscales = [];
var losses = [];
var torpath1 = [];
var torpath2 = [];
var torpath3 = [];
var torpath4 = [];
var torpath5 = [];


// Add markers to the map
function setMarkers(map, locations, EFscale) {
	for (var i = 0; i < locations.length; i++) {
   	report = locations[i];
//	var startLatLng = new google.maps.LatLng(report[0], report[1]);
//	var endLatLng = new google.maps.LatLng(report[2], report[3]);
//	   var combine = [startLatLng,endLatLng] // or use ...
   var combine = [{lat: report[0], lng: report[2]},{lat: report[1], lng: report[3]}];

   // var marker = createMarker(map,combine,report[6]);
	efscales = report[4];
	losses = report [5];

	if (efscales == 1){
	torpath1 = new google.maps.Polyline({
		path: (combine),
		//geodesic: true,
		strokeColor: '#1F45FC',
		strokeOpacity: 1.0,
    	strokeWeight: .5
	});
	torpath1.setMap(map)
	}

	if (efscales == 2){
    torpath2 = new google.maps.Polyline({
        path: (combine),
        //geodesic: true,
        strokeColor: '#59E817',
        strokeOpacity: 1.0,
        strokeWeight: 1.0
    });
	torpath2.setMap(map)
	}

    else if (efscales == 3){
    torpath3 = new google.maps.Polyline({
        path: (combine),
        //geodesic: true,
       strokeColor: '#FFFF00',
        strokeOpacity: 1.0,
        strokeWeight: 1.5
    });
	torpath3.setMap(map)
    }

    else if (efscales == 4){
    torpath4 = new google.maps.Polyline({
        path: (combine),
        //geodesic: true,
        strokeColor: '#F87217',
        strokeOpacity: 1.0,
        strokeWeight: 2.0
    });
	torpath4.setMap(map)
    }

    else if (efscales == 5){
    torpath5 = new google.maps.Polyline({
        path: (combine),
        //geodesic: true,
       strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2.5
	});
	torpath5.setMap(map)
	}
   }
}
//        if (efscales = 2) {
//            strokeWeight: 12
//        },
//		 if (efscales = "1") {
//            strokeWeight: 0.4
//        } else if (efscales = "2") {
//            strokeWeight: 0.6
//        } else if (efscales = "3") {
//            strokeWeight: 0.8
//        } else if (efscales = "4") {
//            strokeWeight: 1.0
//        } else if (efscales = "5") {
//           strokeWeight: 1.2
//        }
//	});

// Remove tornado reports from the map, but keep them in the array
//function clearInput(element){
//element.value="";
//}    //http://stackoverflow.com/questions/15969307/how-to-clear-textbox-on-html-using-javascript
function EF1() { 				
	if (torArray) {
	if (efscales != 1) {
	    for (i in torArray) {
	     torArray[i].setMap(null);
	  }
    }
  }
}
// Shows any overlays currently in the array
//function showOverlays() {
  //if (markersArray) {   //for other markers
//    for (i in torArray) {
//      torArray[i].setMap(map);
//    }
//}
''')
###########################################################
java.close()
print "Wrote the Javascript file. Now write your HTML file and view your map on the Web!"


