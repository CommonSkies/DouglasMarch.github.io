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
#<head>0
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
''')	
###########################################################
#Open and read the SPC comma-delimited storm reports file
file=open(reports,'r')
lines=file.readlines()
#Initialize type of report
type="None"
#Initialize marker variables
tor=""
tor0=""
tor1=""
tor2=""
tor3=""
tor4=""
tor5=""
#Loop through the reports and parse the data
for line in lines:
	cols=line.split(',')
	dummy = int(1)
	#Leave out the headers and determine type of report
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
		if (EFscale == 0):	
			tor0=tor0+'''['''+startlat+''', '''+startlon+''', '''+endlat+''', '''+endlon+''', '''+EFscale+''', '''+moneyloss+''', "<b>Time:</b> '''+ymd+''','''+time+''', UTC<br><b>EF-Scale</b> '''+EFscale+'''<br><b>Fatality:</b> '''+died+'''"],'''
		if (EFscale == 1):	
			tor1=tor1+'''['''+startlat+''', '''+startlon+''', '''+endlat+''', '''+endlon+''', '''+EFscale+''', '''+moneyloss+''', "<b>Time:</b> '''+ymd+''','''+time+''', UTC<br><b>EF-Scale</b> '''+EFscale+'''<br><b>Fatality:</b> '''+died+'''"],'''
		if (EFscale == 2):	
			tor2=tor2+'''['''+startlat+''', '''+startlon+''', '''+endlat+''', '''+endlon+''', '''+EFscale+''', '''+moneyloss+''', "<b>Time:</b> '''+ymd+''','''+time+''', UTC<br><b>EF-Scale</b> '''+EFscale+'''<br><b>Fatality:</b> '''+died+'''"],'''
		if (EFscale == 3):	
			tor3=tor3+'''['''+startlat+''', '''+startlon+''', '''+endlat+''', '''+endlon+''', '''+EFscale+''', '''+moneyloss+''', "<b>Time:</b> '''+ymd+''','''+time+''', UTC<br><b>EF-Scale</b> '''+EFscale+'''<br><b>Fatality:</b> '''+died+'''"],'''
		if (EFscale == 4):	
			tor4=tor4+'''['''+startlat+''', '''+startlon+''', '''+endlat+''', '''+endlon+''', '''+EFscale+''', '''+moneyloss+''', "<b>Time:</b> '''+ymd+''','''+time+''', UTC<br><b>EF-Scale</b> '''+EFscale+'''<br><b>Fatality:</b> '''+died+'''"],'''
		if (EFscale == 5):	
			tor5=tor5+'''['''+startlat+''', '''+startlon+''', '''+endlat+''', '''+endlon+''', '''+EFscale+''', '''+moneyloss+''', "<b>Time:</b> '''+ymd+''','''+time+''', UTC<br><b>EF-Scale</b> '''+EFscale+'''<br><b>Fatality:</b> '''+died+'''"],'''
###########################################################
#Write the storm reports to the Javascript
java.write('''
var tor= ['''+tor+'''];
var tor0= ['''+tor0+'''];
var tor1= ['''+tor1+'''];
var tor2= ['''+tor2+'''];
var tor3= ['''+tor3+'''];
var tor4= ['''+tor4+'''];
var tor5= ['''+tor5+'''];
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
''')
###########################################################
java.close()
print "Wrote the Javascript file. Now write your HTML file and view your map on the Web!"

