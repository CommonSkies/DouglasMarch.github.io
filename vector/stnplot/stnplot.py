#!/usr/bin/python
#Plots a map using the vplot system available at mensch.org/vplot.
#Thanks to B. Fiedler for the map and vplot.  I coded the rest. See
#the comments throughout and especially at the end.
#C. Godfrey			February 2009
#
#Typical usage:
#  stnplot.py
#  stnplot.py -o map.eps -a
#  stnplot.py -o map.eps -a -v -d

import cPickle,vplot,math,getopt,sys,string,re
pickledboundaries='world_us_country.pickle'
verbose=False 	#Set to True with -v to activate more print statements when debugging
epsfilename='map.eps' 	#This name will be used unless the -o option is invoked 
recoord=False 	#Set to True by using -a,  which invoke azimuthal_equidistant
dots=False 	#Set to True by using -d,  which puts red dots on the end of the map line segments

#Get the command line options.  (In this application, otherargs should be empty.):
alloptions, otherargs= getopt.getopt(sys.argv[1:],'o:vad') #Note the : after the o
for theopt,thearg in alloptions:
	if theopt=='-o': #-o needs filename after it, which is now thearg
		epsfilename=thearg	
	elif theopt=='-a': 
		recoord=True
	elif theopt=='-v': 
		verbose=True
	elif theopt=='-d': 
		dots=True
	else: #Something went wrong
		print "Uh-oh, what are these??? ", theopt, thearg
		sys.exit()

#Use these 2 functions to plot something other than the Mercator projection
def azimuthal_equidistant(lon,lat,lonc):
	#See http://www.progonos.com/furuti/MapProj/Normal/CartHow/HowAzEqDA/howAzEqDA.html
	#lonc is the longitude line you want directed downward
	#x and y are scaled by 1/4 the circumference of the Earth
	r=(90.-lat)/90.
	theta=(lon-lonc)*math.pi/180.
	y=-r * math.cos(theta)
	x= r * math.sin(theta)
	return x,y
def reCoordList(a,maptrans,param):
	#Converts a list of pairs of lon, lat to the  
	#projection coordinates x, y (the Cartesian plot coordinates)
	#given by function maptrans, accepting a single parameter
	m=0
	b=[]
	while m<len(a):
		lon,lat,m=vplot.next2(a,m) #Uses vplot
		x,y=maptrans(lon,lat,param)
		b.append(x)
		b.append(y)
	return b

#Set the bounds for the map:
lonmin=-83.50
#lonmin=-82.57
lonmax=-76.00
#lonmax=-73.57
latmin=33.00
#latmin=28.62
latmax=38.00
#latmax=35.62

#Open and read the map file
mapfile=open(pickledboundaries,'r')
thedict=cPickle.load(mapfile) #thedict receives the dictionary stored in the pickled file
if verbose: print "Keys in pickled dictionary:",thedict.keys()
lines=thedict['lines']
heads=thedict['heads'] 
mapfile.close()
if verbose: print "type(lines)=",type(lines),"   len(lines)=",len(lines)
if verbose: print "Here is a sample:",lines[0]

#Open file and set map projection
a=vplot.eps_class(epsfilename) #Open an EPS file and set default scales
if not recoord:
	a.scale(lonmin,lonmax,latmin,latmax) #Set bounds for Mercator map
	print "Using Mercator projection."
else:
	a.scale(-1.00,1.00,-1.00,1.00) #Set bounds for the azimuthal_equidistant map 
	lonc=-75. #Use this parameter to set the downward-pointing longitude
	print "Using Azimuthal-Equidistant projection."

#Draw map
for i in range(0,len(heads)):
	dum1,dum2,linelatmax,linelatmin,linelonmax,linelonmin=[float(x) for x in heads[i]]
	#If no part of the line is in the visible map, don't plot it:
	#The following block makes my map look funny:
	#if linelatmin>latmax or linelatmax<latmin or \
	#   linelonmin>lonmax or linelonmax<lonmin: continue
	line=lines[i]
	if recoord:
		line=reCoordList(line,azimuthal_equidistant,lonc) 
	a.color('black')
	a.draw(line[:])
	if dots:
		a.color('red')
		for i in range(0,len(line),2):
			a.circle(line[i],line[i+1],50L,'F') #Makes the end points of line segments visible

############################################################
############################################################
# YOUR TURN (PART I) - See comments at end of program
# Draw lightly-colored dashed latitude and longitude lines at
# evenly-spaced intervals (every three degrees or so).
# YOUR CODE GOES HERE:

a.color(205,205,205)

lonstart=lonmin-20
lonend=lonmax+20
latstart=latmin-20
latend=latmax+20

space=range(0,300,3)
a.linewidth(1)
for i in space:
	a.dashdraw([[lonstart,latmin+i],lonend,latmin+i])
	a.dashdraw([[lonmin+i,latstart],lonmin+i,latend])

############################################################
############################################################

#Make some colors
white=[255,255,255]
red=[200,0,0]
green=[0,180,0]
black=[0,0,0]
orange=[248,114,23]

#Here is Asheville!
lon=-82.566
lat=35.6165
if recoord:
	lon,lat=azimuthal_equidistant(lon,lat,lonc) #lat/lon cooords are not really lat/lon anymore
	print lat,lon



#Test a few things...
#a.arrow(lon,lat-8.7,lon+8.0,lat,15)
#a.color(80,255,80)
#a.circle(-78.0,24.0,25,'F') #Lat/Lon must be real numbers (not integers)!
#a.circle(lon,lat,2,'F')
#a.color(red)
#a.arrow(lon,lat,lon+8.0,lat,15)
#a.text(lon+0.1,lat-0.05,0,12,"UNC Asheville")
#a.color(green)
#a.text(-78.0,29.0,0,20,"Make")
#a.text(-76.5,29.3,45,20,"a")
#a.color('red')
#a.text(-76.0,29.6,90,20,"map")

#Test wind barbs
#NOTE: Size is radius of cloud cover circle/0.13
#ccrad=5.0
#ccrad=ccrad/0.13
#a.windbarb(-78.0,31.5,0,40,ccrad) #x,y,speed,dir,size
#a.windbarb(-78.5,31.5,7,30,ccrad)
#a.windbarb(-79.0,31.5,47,20,ccrad)
#a.windbarb(-79.5,31.5,107,10,ccrad)
#a.color(80,80,240)
#a.windbarb(-77.0,34.0,10,0,20)	#Note how this is NOT from the north!
#a.color(green)
#a.windbarb(-77.0,31.0,40,70,ccrad)
#a.color(red)
#a.windbarb(-77.0,31.0,60,135,ccrad)
#a.color(orange)
#a.windbarb(-77.0,31.0,140,225,ccrad)

#Test circles
#a.color(255,130,80)
#a.circle(-78.0,32.0,5,'F') #Lat/Lon must be real numbers (not integers)!
#rgb=[80,80,240]
#a.color(rgb)
#a.circle(-78.3,31.2,5) #Open circle
#a.sector(-81.0,35.5,5,5,0,90,'F') #x,y,inner_radius,outer_radius,angle1,angle2,[fill]
#a.sector(-80.5,35.0,0,20,270,90,'F') #x,y,inner_radius,outer_radius,angle1,angle2,[fill]
#a.sector(-81.0,34.8,0,25,270,90,'F') #x,y,inner_radius,outer_radius,angle1,angle2,[fill]

#Read METAR data
infile=open("200902111900metar.dat","r")
line=infile.readlines()
line=line[1:]	#Lose the header
for metar in line:
	#A simple way to remove whitespace before causing problems later
	metar=re.sub("North ","North_",metar)
	metar=re.sub("South ","South_",metar)
	metar=re.sub("West ","West_",metar)
	metar=re.sub("New ","New_",metar)
	metar=re.sub("Rhode ","Rhode_",metar)

	#Split line into individual strings
	metar=metar.split()

	#Remove whitespace in station names
	for i in metar:
		while metar[2] != "US:":
		#	print metar
			new=metar.pop(1)+"_"+metar.pop(1) #.pop(x) removes x from list EACH time it's called
			metar.insert(1,new)
		#	print metar

	#Use this for testing anywhere
	#print metar

	#Strip out variables...you may want to add a few variables using
	# this formatting as an example
	icao=metar[0]
	lat=string.atof(metar[4][:-1])	#Convert to float; drop last character
	lon=string.atof(metar[5][:-1])*-1	#West longitudes are negative
	elev=string.atoi(metar[6])
	temp=repr(int(round(string.atof(metar[9]))))	#Convert to float, round integer, back to string
	dwpt=repr(int(round(string.atof(metar[10]))))
	wspd=string.atoi(metar[12])	#Convert to integer
	wdir=string.atoi(metar[13]) 
	vis=string.atof(metar[14])
	pres=string.atof(metar[15])	#Convert to float
	cloud=(metar[16])

	if icao=="KAVL":
		print "\nHere are a few of the decoded observations from Asheville:"
		print icao,lat,lon,elev,temp,wspd,vis,pres
#		print icao,pres

############################################################
############################################################
# YOUR TURN (PART II) - See comments at end of program
# Draw station plots showing at least wind speed and direction,
# temperature, dewpoint, cloud cover, and pressure following
# typical convention (see the class Web site for links to
# station plot examples). Also include a title with the date
# and time.

	#You may need to define a few other variables here.  See
	#the code above for formatting examples.

	scale=1.0	#Use this to scale your entire station plot
	#Be sure to adjust for missing observations, coded as -999.

	#YOUR CODE GOES HERE:
	a.color(50,150,255)
	if cloud == "CLR":
		a.circle(lon,lat,3) #Open circle
	if cloud == "FEW":
		a.color(204,0,204)
		a.sector(lon,lat,0,3,0,90,'F') #x,y,inner_radius,outer_radius,angle1,angle2,[fill]
		a.circle(lon,lat,3) #Open circle
	if cloud == "SCT":
		a.color(0,205,0)
		a.sector(lon,lat,0,3,270,90,'F') #x,y,inner_radius,outer_radius,angle1,angle2,[fill]
		a.circle(lon,lat,3) #Open circle
	if cloud == "BKN":
		a.color(255,128,0)
		a.sector(lon,lat,0,3,180,90,'F') #x,y,inner_radius,outer_radius,angle1,angle2,[fill]
		a.circle(lon,lat,3) #Open circle
	if cloud == "OVC":
		a.color(255,0,0)
		a.circle(lon,lat,3,'F') #Open circle
	a.color(black)
	ccrad=3.0
	ccrad=ccrad/0.13
###	wdir=wdir-180.0 
	wdir=270-wdir 
	a.windbarb(lon,lat,wspd,wdir,ccrad)	
#	if wdir >-100:
#		wdir=wdir-90.0 
#		a.windbarb(lon,lat,wspd,wdir,ccrad)	
#		transform=" scale(1,-1)"
	if temp!=-9999:
		a.color(red)
		a.text(lon-.25,lat+.05,0,7,temp)
	if dwpt!=-9999:
		a.color(green)
		a.text(lon-.25,lat-.03,0,7,dwpt)
	if pres!=-9999:
		a.color(255,128,0)
		if pres>1000.0 and pres<1010.0:
			pres=str(int(round((pres-1000)*10)))
			a.text(lon+.05,lat+.05,0,7,"0"+pres)
		elif pres>1010.0:
			pres=str(int(round((pres-1000)*10)))
			a.text(lon+.05,lat+.05,0,7,pres)
		elif pres<1000.0:
			pres=str(int(round((pres-900)*10)))
			a.text(lon+.05,lat+.05,0,7,pres)
	a.color()
	a.linewidth()
	a.color(255,0,0)
	a.rect(-75.2,32.50,-79.0,48)
	a.color(0,0,0)
	a.text(-78.9,32.85,0,13,"METAR Observations")
	a.text(-78.9,32.65,0,13,'1900 UTC 15 February 2009')

############################################################
############################################################

#Clean up
a.close()

#print "\nYOUR TURN: See the comments at the end of stnplot.py\n"
# Your job:
# Draw station plots showing the observations across the region
# near North Carolina.  You may use either the included file of
# decoded METAR observations or create your own set of more recent
# observations. At a minimum, your finished product should include
# the following:
#	1) Lightly-colored, dashed latitude and longitude lines
#	2) Wind barbs showing wind speed and direction at all sites
#	3) Cloud cover at all sites
#	4) Temperature, dewpoint, and sea-level pressure at all sites using
#		different colors
#	5) The base map showing the region around North Carolina (change the
#       bounds of the map so that North Carolina is in the middle)
#	6) A title showing the date and time of the observations
# Convert your EPS output to a PNG image and post both your PNG image
# and your source code, along with a link to your EPS output, on your
# password-protected Web page.

# You could also add some flare to your plots by including
# the station ID, pressure tendency, present weather, and visibility.
# You could color-code the plots according to elevation, visibility, or
# the height of the cloud deck (I only gave you the highest layer of
# clouds, but we can pretend that this is the lowest layer). Be imaginative!
