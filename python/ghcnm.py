#!/usr/bin/python2.7
# Written by C. Godfrey: 16 May 2012

# See comments below for "YOUR TURN (PART I-IV)".
# These comments describe the revisions that you must make to this script.
# When everything works satisfactorily, please post your ghcnm.py, ghcnm.html,
# and image files in your password-protected directory and notify your
# instructor that you have finished. Note that "print" will print to your
# screen, which is useful for testing and debugging, while "print >> outfile"
# will print to your output file ghcnm.html.

# The indentations here are with a TAB, rather than 4 spaces!!

import os, sys, glob, random, string
import matplotlib               #Use matplotlib for drawing figures and using speedy arrays
matplotlib.use('Agg')           #Prevent need for a X server
from pylab import *
from numpy import ma
import numpy as np              #Needed for NumPy array operations

###############################################################################################
# You can automatically grab the latest data and then unzip and untar it. Python works
# interactively with the terminal and the outside world.  Great stuff can result!  Set 'grabit'
# equal to 1 below to see how this could work.  Note that there are other ways to accomplish
# this that remain purely Python. To speed things up a bit, you can set 'grabit' back to zero
# to skip this step once you have your data. Note that you must also supply a URL for Python to
# grab the data automatically.

grabit=0	#Switch to grab new data (0: skip it ; 1: get new data)

##############################################################################################
if grabit==1:
	#Grab the latest time series of unadjusted monthly average temperature data
	urlbase="ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/v3/"	#i.e., "ftp://ftp.ncdc.../v3/"
	zipfile="ghcnm.tavg.latest.qcu.tar.gz"	#i.e., "ghcnm.tavg.latest.qcu.tar.gz"

	print "Attempting to grab ",urlbase+zipfile
	os.system("wget "+urlbase+zipfile)
	print "Attempting to unzip "+zipfile
	os.system("gunzip -f "+zipfile)
	print "Attempting to untar "+zipfile[:-3]
	os.system("tar xvf "+zipfile[:-3])
else:
	print "We already have the data.  Let's continue without getting an update."

#Now determine the appropriate data directory.  We might have multiple versions from different
#download dates (e.g., ghcnm.v3.1.0.20120512 vs. ghcnm.v3.1.0.20120516).  Let's just pick the
#latest one, which should be at the end of the directory listing.

files=glob.glob("ghcnm.v3*")	#Creates a Python LIST of the files matching these criteria in this directory
#files=glob.glob("*")			#You could do this for all of your files
files.sort()					#Sort the list in alphanumeric order
#print files					#See for yourself!
try:
	dir=files[-1]				#Pick the last file or directory in the list; that's our data directory!
	print "The data directory is",dir		#See, it works!
except:
	print "\n\nHey, wait!  Python works, but it doesn't look like you have"
	print "actually downloaded any data yet.  You need to fix the code by"
	print "changing 'grabit' and adding the correct URL and file name."
	print "Bye!"
	sys.exit()

#Now that we have the data and know where to find the files, we can read and store the data.
##############################################################################################

#There are ways to search a file for a specific character string (say, a station).  For now,
# just set the station ID for the relevant station (e.g., Asheville) here.
station="42572315000"	#Here is the Asheville ID

#We will need all the data anyway, so let's read it in. Notice that the file name begins the same
# as the directory name, except that '.tavg' is inserted after 'ghcnm'.
flnm=dir+"/"+dir[:5]+".tavg"+dir[5:]+".qcu.dat"		#This is the actual data file name
file=open(flnm,"r")									#Open the file
lines=file.readlines()								#This reads the entire file as a character string

#We will need this function later. It returns the mean of an array with missing values. Thanks to eyurtsev.
def nanmean(data, **args):
	#Usage: x=nanmean(data,[axis=0 or axis=1 or leave it out])
	return np.ma.filled(np.ma.masked_array(data,np.isnan(data)).mean(**args), fill_value=np.nan)

#Python uses data structures called dictionaries. Unlike arrays, dictionaries are indexed with
# keys instead of numbers.  Keys can be almost anything.  In this case, we'll use the station IDs
# as keys.  It's like having a grocery cart (a dictionary) full of bags labeled "Frozen", "Dairy",
# and "Bread" (the keys). Each bag contains lots of products (the values), which can be almost any
# data type.  Cleverly, we can also make these values contain new dictionaries!  Inside the
# grocery cart (dictionary) with the bag labeled "Dairy" (key), we could have milk (a value that
# is itself a dictionary) with brand "Laura Lynn" (key) costing $3.25 (value) and milk with brand
# "Oakhurst" (another key) costing $4.25 (that key's value).  Google "Python dictionary" to learn
# more about this data structure.

stid={}			#Create an empty DICTIONARY of station IDs
yrcount={}		#Create an empty dictionary of the number of years in each station's record
stnarr={}		#Create an empty dictionary to hold 2-D arrays of data for each station
yr={}			#Create an empty dictionary to hold 1-D arrays of years in each station's record

for line in lines:
	#Strip the station ID and year out of each line
	id=line[0:11]
	year=line[11:15]

	#Create a new dictionary inside the stid dictionary to hold the data for each year.
	if id in stid:	#First test to see if the station ID key exists. (We don't want to overwrite it!)
		pass		#Don't do anything.  This is a placeholder when a line of code is required.
	else:
		stid[id]={}
	if year in stid[id]:
		pass
	else:
		stid[id][year]={}	#Now create a new dictionary inside that one!

	stid[id][year]["line"]=line		#Assign the entire line as the value for this key

#We now have sets of dictionaries within dictionaries.  Think of this like a truck full
# of bags, each with a station ID.  Inside each bag is a set of more bags, each labeled
# with a year.  Inside each of those bags is a bag labeled "line" that holds the
# character string with the data. Later, we'll add a bag inside the "year" bag that
# contains a structure called a list that holds the monthly data for that year, for that
# station.

#Initialize some things
minyear=9999
maxyear=-9999

#Now loop through all of the stations and store the data
for id in stid.keys():

	yrcount[id]=0	#Initialize number of years in this station's record

	#Loop through all the years for this station.  There is NO ordering when looping
	# through dictionary keys, so we have to sort the years on the fly.  Otherwise,
	# our plots will be scrambled!
	for year in sorted(stid[id].keys()):

		#print id,year				#See, now the years are in order.

		#Let's save the largest and smallest years that we encounter (for later)
		if string.atoi(year) < minyear: minyear=string.atoi(year)
		if string.atoi(year) > maxyear: maxyear=string.atoi(year)

		#Make a LIST for each year for this station, assigning the data to each month.
		# There are usually easier ways to read in data, but here we may or may not
		# have a flag, so using the default input is tough.  We'll stick to the formatting
		# detailed in the README file for these data.  
		tavg=[]			#This makes a blank list

		line=stid[id][year]["line"]
		for i in range(12):
			start=19+(8*i)
			end=24+(8*i)
			tavg.append(line[start:end])	#Lists work by appending more items to the end

		#Make a new key/value pair that holds the list of the monthly data for each year
		stid[id][year]["tavg"]=tavg

		#Count the number of years in this station's record
		yrcount[id]+=1


	############################################################################
	#With this station's data stored, we can build arrays to organize the data for
	# calculations and plotting.

	#Create an empty, two-dimensional NumPy ARRAY and put it in our dictionary
	stnarr[id]=np.zeros((yrcount[id],12))
	yr[id]=np.zeros(yrcount[id])	#Save the years for this station as an array

	i=-1		#Initialize a counter for the years
	for year in sorted(stid[id].keys()):	#Loop through the years for each station
		i+=1
		yr[id][i]=string.atoi(year)			#Convert year to a number/Put in array
		for j in range(12):					#Loop through each month in the year
			stnarr[id][i,j]=stid[id][year]["tavg"][j]
	#print stnarr
	#With your chosen station, perform some calculations
	if id==station:                   #Asheville Airport
		print "Hey, I found it! ",id

		#Uncomment to see what the array looks like
		set_printoptions(threshold='nan')	#Prevent truncating the output

################################################################################
################################################################################
#*******************************************************************************
# YOUR TURN (PART I)
# Calculate the monthly mean temperature for all 12 months for your chosen
# station and calculate the mean temperature for the period of record.  Be
# sure to convert your numbers to the correct units and ignore missing values.
# You may want to make use of some NumPy routines that you can learn about
# here: http://docs.scipy.org/doc/numpy/reference/routines.statistics.html.
# Note that with NumPy arrays you can operate on the entire array at once!
# To ignore missing values, replace -9999 elements by setting them equal to
# 'nan', without the quotes. Be sure to indent twice as you continue the code
# below.
#
# HINT 1: This might do something for you...stnarr[id][stnarr[id]<-9000]=nan
# HINT 2: Use the function nanmean, defined above
#
# Your code goes here:


		y={}
		x={}
		mtavg={}
		yravg={}

		stnarr[id][stnarr[id]<-9000]=nan			#find all missing values and assign -9999 = nan
		mtavg[id]=nanmean(stnarr[id],axis=0)/100.0	#Axis 0 will search by colums
		yravg[id]=nanmean(stnarr[id],axis=1)/100.0	#Axis 1 will search by rows
		mean=nanmean(mtavg[id])
		mean=round(mean,3)
		num=np.round(mtavg[id],3)
		y=yravg[id]										
		x=yr[id]									#Assigning X,Y here just makes it easier to remmber which is which
	
################################################################################
################################################################################

		#Use matplotlib to make a PNG file
		plotfile="stntmp.png"

################################################################################
################################################################################
#*******************************************************************************
# YOUR TURN (PART II)
# Add a line to create a plot.  See http://matplotlib.sourceforge.net/gallery.html
# for example code.  It is far easier if you have NumPy arrays for x and y.
# Here, all you need to do is fill in your own array of annual mean temperatures
# in the line below. I did the rest for you.
#
# Your code goes here:
#
		#plot(the_year_array_for_this_station,your_own_array_of_annual_means,linewidth=1.0)
		plot(x,y,linewidth=1.0)



################################################################################
################################################################################
		xlim(yr[id][0],yr[id][-1])
		xlabel('Year')
		ylabel('Temperature ($^\circ$C)')
		title('Annual Mean Temperature for Station '+id)
		savefig(plotfile)
		os.chmod(plotfile,0644) #Set file permissions
		plt.clf()	#Close the current figure

#Calculate global statistics. Some of these calculations could be done above,
# but as a learning tool, it seems best to do it separately.
nstations=len(stid.keys())			#Find the number of stations
nyr=maxyear-minyear+1				#Determine the number of available years in all data
#print nyr+minyear
tavgarr=np.zeros((nyr,nstations))	#Create a new NumPy array (nyears x nstations)
tavgarr.fill(np.nan)				#Fill the new array with missing data

#CG FIX numst=np.zeros((nyr,nstations))			#This does not work since numst will only be a 1-d not 2-d since each year will be replaced with nstations
numst=np.zeros((nyr))				#This is to allow for each year in nyr to be replaced by nstations[yr] 
#print nstations,nyr					#Prints off 7280, 316
#print tavgarr
n=-1
for id in stid.keys():
	n+=1							#An index for the station (i.e., 0 to nstations-1)
################################################################################
################################################################################
#*******************************************************************************
# YOUR TURN (PART III)
# Fill in the tavgarr NumPy array with the annual means for each station for
# each year.  Then calculate the annual mean global temperature for each year
# and the number of stations used in each annual average. You may end up using
# some of the same code that you wrote for PART I. If you already converted your
# particular station's data to degrees C, make sure you don't do it again when
# analyzing the global data!
#
# HINT 1: Some stations have data gaps that span several years, so yrcount[id] is
# not a reliable way to find the starting and stopping years and assign annual
# means to the elements of the tavgarr NumPy array.  We therefore need to tie
# the annual means to the elements that correspond with their respective years.
# You will want to use the following after you find the annual average for
# each year and each station:
#	#Assign the annual mean for each year to the tavgarr array, making sure it's in the right spot
#
#    for i in range(size(annave)):
#        tavgarr[yr[id][i]-minyear,n]=annave[i]
#        print yr[id][i]-minyear
#
#	#Test your calculations.  These annual means should match what you found for
#	# your chosen station in Part I.
#	if id=="stid":
#		print tavgarr[yr[id][0]-minyear:yr[id][size(yravg[id])-1]-minyear,n]
#
# Here, annave is an array that contains the annual means for each year in the
# station's record.  If any month in the year is missing, annave[i] is nan.
# You probably already found annave in part I.
#
# HINT 2: You may find this useful:
#		if not math.isnan(tavgarr[i,j]): ...
# I found it easiest just to create a new array with only valid data.
#
# Your code goes here:
	
	stnarr[id][stnarr[id]<-9000]=nan			#find all missing values and assign -9999 = nan
	if id==station:
		pass
	else:
		stnarr[id]=stnarr[id]/100.0
	annave=np.mean(stnarr[id],axis=1)
	for i in range(size(annave)):
		#print i			#prints off years for each station 
		tavgarr[yr[id][i]-minyear,n]=annave[i]
		#print tavgarr[yr[id][i]-minyear,n],i
		#x2[i]=len(tavgarr)
		#x2[i]=np.array(tavgarr.shape[1])	#shape.0 is years to nyr(316)
globeavg=nanmean(tavgarr,axis=1)

n=-1
year=np.zeros(nyr)
for i in range(tavgarr.shape[0]):   #For every year...
	n+=1
	year[i]=1+minyear					#Add for every year i plus the smallest year. Ret- Actual year for x-axis on graph
	dat=[]                          #Open a list
	for j in range(tavgarr.shape[1]):   #For every station in that year...
		if not math.isnan(tavgarr[i,j]):

    # if not (-) math isnan(-), ie for each number that is a number [ (/) NaN], used for NaN
	# ie * if num != NaN: * over i (years [in i.shape is (a,b) so i.shape is a]) by j (stations)
    # remember that i has (a) rows and (b) columns!
	
			dat.append(tavgarr[i,j])    #Add that data point
	if len(dat)!=0:			#if dat actually has info, making it have data and !=0:
		numst[i]=len(dat)	#the 1d array numst[i] where i is everything by the year with len(dat) where

######################################################################################################
#*	From the Python reference: len(s) : Return the length (the number of items) of an object.		*#
#*  The argument may be a sequence (string, tuple or list) or a mapping (dictionary). count() :		*#
#*  Return the number of times x appears when used in the context of a list.####					*#
######################################################################################################

allyr=np.zeros(nyr)
for i in range(nyr):
	allyr[i]=minyear+i

time=np.sort(year)

################################################################################
################################################################################

plotfile="globalavg.png"
import matplotlib.pyplot as plt
import pylab
fig = plt.figure()
ax1= fig.add_subplot(111)

ax1.plot(allyr,globeavg,'r-',label='Temperature')
ax2 = ax1.twinx()
ax2.plot(allyr, numst, 'b-', label='Number of Stations')
ax2.set_xlim(allyr[0],allyr[-1])
ax2.set_ylabel('Number of Stations')

#Ask matplotlib for the plotted objects and their labels
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax2.legend(lines + lines2, labels + labels2, loc=0)
ax1.set_xlabel("Year")
ax1.set_xlim(1700,nyr+minyear-2)
ax1.set_ylabel(r"Temperature ($^\circ$C)")
ax2.set_ylabel(r"Number of Stations")
ax2.set_ylim((0,6000))
ax1.set_ylim(np.nanmin(globeavg)-.5,np.nanmax(globeavg)+.5)

title('Unadjusted Global Annual Mean Temperature')
savefig(plotfile)
plt.clf()   #Close the current figure

###############################################################################
#################################################################################

#To create some output that will look nice in a Web browser, we'll need to write
# our results embedded within some HTML.
output="""<html>
<head>
<style>
  h1 {color:firebrick; text-align:center}
  h2 {color:black; text-align:center}
  table {border: 2px solid black;
				 border-collapse:collapse;
				}
  body {background-color: #E5F0FA; width:800px; margin: 5px auto}
</style>
</head>
<body>"""

################################################################################
################################################################################
#*******************************************************************************
# YOUR TURN (PART IV)
# Add HTML code to present your results. The variable 'output' is a character
# string, so any numbers will need to be converted to characters.  You can see
# an example below.

#Modify this

output=output+"""<h1>Temperature Report for Asheville Municipal Airport, NC</h1>
<h2>GHCN-M Station ID: """+station+"""</h2>
<h3>The mean temperature for the period of record is """+str(mean)+"""</h3>
<b style="font-size:20px";>Monthly mean temperature (&#8451) </b>
<table style="width:35%">"""

import calendar
a=list(calendar.month_name[1:])
for i in range(12):
	output=output+"""
	<tr>
		<td><b>"""+str(a[i])+"""</b></td>
		<td>"""+str(num[i])+"""</td>
	</tr>
"""
output=output+"""</table>
<br>
<center>
	<img src="stntmp.png">
</center>
<h1>Global Annual Mean Temperature</h1>
<p>The figure below show the correlation between the annual global mean temperature and the number
of stations from the given time period. Notice how as the number of stations increased so did the 
annual temperature.</p>
<br>
<center>
	<img src="globalavg.png">
</center>"""

################################################################################
################################################################################

output=output+"\n</body></html>"

#Now write the output file
outfile=open("ghcnm.html","w")
print >> outfile, output
outfile.close()
