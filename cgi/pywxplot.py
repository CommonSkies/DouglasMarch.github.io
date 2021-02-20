#!/usr/share/enthought/epd_py25-4.1.30101-rh5-x86/bin/python
#Note this link to python (it's not /usr/bin/python)

#Thanks to Brian Fiedler for most of this code.  Modified by C. Godfrey
#Please change the "cgodfrey" below.  See the task defined at the end.

#Note that if your browser asks what to do with wxplot.cgi, there is probably a problem
# with your script.  Run it at the command line (./wxplot.cgi) to locate the error.

import sys, urllib2,os,cgi,time, glob, math
import cgitb; cgitb.enable()
verbose=1 #verbose=0 will turn off some printing of helpful debugging information
print "Content-type: text/html\n"  #Required first line to send to client

#Provide a place for matlplotlib to write files in the directory .matplotlib.  View this in
# your visit directory with ls -la.
os.environ['HOME']="/home/dmarch/public_html/cgi/visit" #Make this your directory!!

###########################################################
import matplotlib  #For the purpose of the following statement:
matplotlib.use('Agg') #Prevent matplotlib from preparing to open a GUI (and crashing)
###########################################################

###########################################################
#Import necessary libraries
from pylab import *
#import matplotlib.numerix.ma as M
import numpy as np
import numpy.ma as ma
import matplotlib.dates as mdates
from matplotlib.dates import YearLocator, MonthLocator, DayLocator, DateFormatter, HourLocator
import datetime
###########################################################

###########################################################
#The Web address for the data file(s)
file="http://www.mesonet.org/data/public/mesonet/mts/YYYY/MM/DD/YYYYMMDDSTID.mts"
###########################################################

###########################################################
#Process the parameters passed to this script from the HTML form.  You may want to clean
# up the print statements for your final plot.

try:
	form=cgi.FieldStorage()
	print "The CGI form has keys:",form.keys(),"<p>"
	for key in form.keys():
		print key,':', form[key].value,'<br>'
	print "<p>"
	site=form['stid'].value
	site2=form['stid2'].value
	degrees=form['scale'].value
#	yyyymmdd=form['thedate'].value
	startdate=form['startdate'].value
	enddate=form['enddate'].value
except: #Exception as e:
	#print e
	yyyymmdd="20090324" #Default date
	site="NRMN" #Default site
	site2="----"
	degrees="Fahrenheit" #Default temperature scale
###########################################################

###########################################################
#Use user input to make the Mesonet file name, then go get it.
#Syear=startdate[0:4]
#Eyear=enddate[0:4]
#Smonth=startdate[4:6]
#Emonth=enddate[4:6]
#Sday=startdate[6:8]
#Eday=enddate[6:8]

#YyyyMmDd=Syear+Smonth+Sday
#YyyyMmDd=Syear+'-'+Smonth+'-'+Sday
#yyyYmMdD=Eyear+'-'+Emonth+'-'+Eday			#Capitalization is for start or end

#print YyyyMmDd,yyyYmMdD

#**************************

#startdate=str(20090524)
startdate=str(startdate)
#enddate=str(20090625)
enddate=str(enddate)
#print type(startdate) is str				#Easy way to test the type ie int, long, list, tuple, etc *Returns boolean function
#print startdate,enddate

from datetime import datetime,timedelta,date
import time
#from time import strftime

Sdt_obj=datetime.strptime(startdate,"%Y%m%d")
Edt_obj=datetime.strptime(enddate,"%Y%m%d")

f=0
delta=timedelta(days=1)
while Sdt_obj <= Edt_obj:
	f+=1
	Sdate=Sdt_obj.strftime('%Y%m%d')
	file="http://www.mesonet.org/data/public/mesonet/mts/YYYY/MM/DD/YYYYMMDDSTID.mts"	
	file=file.replace('YYYY',Sdate[0:4])		
	file=file.replace('MM',Sdate[4:6])
	file=file.replace('DD',Sdate[6:8])		
	file=file.replace('STID',site.lower())	#Make station ID lower case; put in file name
	if site2 != '----':
		file2="http://www.mesonet.org/data/public/mesonet/mts/YYYY/MM/DD/YYYYMMDDSTID.mts"       
		file2=file.replace('YYYY',Sdate[0:4])
		file2=file.replace('MM',Sdate[4:6])
		file2=file.replace('DD',Sdate[6:8])    
		file=file.replace('STID',site2.lower())	#Make station ID lower case; put in file name
	Sdt_obj += delta
	
#	if f==1:
#		startfile=file
#	else:
#		pass
	if Sdt_obj==Edt_obj:
#		endfile=file
#		print 'Retrieving file(s) from date: <a href="',startfile,'">',startfile,'</a>''To date:<a href="',endfile,'">',endfile,'</a>'
		print 'Retrieving file(s) from date: ',startdate, 'to date: ',enddate, 'for stations: ',site,' & ', site2[0:4]
	else:
		pass

	try:
		content=urllib2.urlopen(file).readlines() # Read the text at the URL "file"
	except:
		print "<p>Uh-oh...something went wrong reading the Mesonet data file"
		sys.exit()

	#print content



#Sdate=datetime.strftime(Sdt_obj,'%Y, %m, %d')
#Edate=datetime.strftime(Edt_obj,'%Y, %m, %d')
#print (Edate),(Sdate)

#for i in range(delta.days+1):
#	print Sdate+timedelta(days=i)

#def datespan(Sdate,Edate,delta=timedelta(days=1)):   #define datespan(start,end,timedelta,split)
#	print datespan
#	currentdate=Sdate						#=Startdate
#	print currentdate
#	while currentdate < Edate:				#Startdat<Enddate
#		yield currentdate
#		currentdate +=delta
#
#		for Day in datespan (date(Sdate),date(Edate),delta=timedelta(days=1)):
#			print day
#			file=file.replace('MM','Mon')
#			file=file.replace('DD','Day')
#			file=file.replace('YYYY','Year')		
#			file=file.replace('STID',site.lower())	#Make station ID lower case; put in file name
#			type(file)

#year=int(Syear)
#for i in range(int(Syear),int(Eyear)):
#	file=file.replace('YYYY',str(i))
#	print file
#	print str(i)
#	for j in range (int(Smonth),int(Emonth)):
#		print str(j)
#		for k in range 
#file=file.replace('MM',Smonth)
#file=file.replace('MM',Emonth)
#file=file.replace('DD',Sday)
#file=file.replace('DD',Eday)
#for i in range(int(Syear),int(Eyear)):
#	print i
#print range (int(Smonth),int(Emonth))
#print 'Retrieving file: <a href="',file,'">',file,'</a>'
#try:
#	content=urllib2.urlopen(file).readlines() # Read the text at the URL "file"
#except:
#	print "<p>Uh-oh...something went wrong reading the Mesonet data file"
#	sys.exit()
###########################################################
#print file	
###########################################################


	#Manipulate the data in the file
	nl=0
	tairs=[]
	dates=[]
	satvpres=[]
	vpres=[]
	dwpts=[]
	nummissing=0
	for line in content:
		nl+=1
		if nl==1 : continue #Ignore the copyright line
		if nl==2 : #Parse the time header
			try:
				line=line.strip()
				year,month,day=line.split()[1:4]
				yr=int(year)
				mn=int(month)
				dy=int(day)
			except:
				print "Something went horribly wrong with the time header!"
				sys.exit()
			continue
		if nl==3 : continue #Ignore the column labels
		line=line.strip()
		items=line.split()
		try:
			stid,stnm,minutes,relh,tair,wspd=items[0:6]
		except:
			print "Oh dear, The line did not split into items correctly!"
			sys.exit()
		thedate = date(yr,mn,dy)
		dnum=date2num(thedate)+float(minutes)/1440. #Add partial day to matplotlib's date
		dates.append(dnum)
		tairfloat=float(tair)
		if tairfloat > -990.:
			satvpres=6.112*exp((17.67*tairfloat)/(tairfloat+243.5))
			vpres=float(relh)*satvpres
			dwpt=((243.5*log(vpres/6.112))/(17.67-log(vpres/6.112)))
			dwpt=(dwpt-32.)/1.8
		if tairfloat < -990.:
			nummissing+=1
		elif  degrees=='Fahrenheit':
			tairfloat=tairfloat*1.8+32.
			dwpt=dwpt*1.8+32.
		tairs.append(tairfloat)
		dwpts.append(dwpt)
print "<p>There are",nummissing,"missing values.<br>"
	
#print dates
#print dwpts,tairs,degrees

###########################################################

###########################################################
#Test behavior for missing values
#tairs[10]=-991. #Uncomment to test with artificial missing value
#tairs[20]=-991. #Uncomment to test with artificial missing value
#tairs[30:40]=[-991.]*10 #Uncomment to test with artificial missing value
###########################################################

###########################################################
#Use matplotlib to make a PNG file in the visit/ directory
figure(figsize=(12,6))

#Define tick marks
years=YearLocator()		#Every year
yearsFmt=DateFormatter('%Y')
months=MonthLocator()	#Every month
monthsFmt=DateFormatter('%m')
days=DayLocator()		#Every day 
daysFmt=DateFormatter('%d')
hours=HourLocator()		#Every hour
hoursFmt=DateFormatter('%H Z')
hours3=HourLocator(range(0,24,3))	#Every 3 hours  
hours6x=HourLocator(range(0,24,6))	#Every 6 hours  

#Try these commands for testing:
#datesx=[x-dates[0] for x in dates]
#plot(datesx,dwpts,'k') #This uses the raw date in "days" on the x-axis
#plot_date(dates,tairs,'k') #This works nicely as long as you don't have missing values

y_maskedi=ma.MaskedArray(tairs)
y_masked=ma.masked_where(y_maskedi<-990.0,y_maskedi) #Ignore data with missing values
plot_date(dates,y_masked,'k',color='k',marker='.') #Plot the data

#y2_maskedi=ma.MaskedArray(dwpt)
#y2_masked=ma.masked_where(y2_maskedi<-990.0,y2_maskedi) #Ignore data with missing values
#plot_date(dates,y_masked+2.,'b',color='b',marker='.') #Plot the data
###########################################################
#These lines might help you with your assignment. Each command plots a second curve.
###########################################################
plot(dates,y_masked,'k',dates,y_masked+2.,'b') #This works for "plot", but not for "plot_date"
plot_date(dates,y_masked+2.,'b',color='b',marker='.') #Draw a second curve
###########################################################

###########################################################
#Set up axes and labels
xlim(dates[0],dates[-1])  
if degrees=="Celsius":
	ylabel("Temperature ($^\circ$C)", size=20, rotation=90)
else:
	ylabel("Temperature ($^\circ$F)", size=20, rotation=90)
xlabel("Date", size=20, rotation=0)
title("TAIR and DWPT at mesonet site: "+site+"")
ax=gca() #gca() gets the currrent axes
if f <= 1:
	ax.xaxis.set_minor_locator(hours)
	ax.xaxis.set_major_locator(hours3)
#	ax.xaxis.set_major_formatter(daysFmt)
if (f > 1) or (f <= 31):
	ax.xaxis.set_minor_locator(days)
	ax.xaxis.set_major_locator(months)
	ax.xaxis.set_minor_formatter(monthsFmt)
if f > 31: # or <=365:
	ax.xaxis.set_minor_locator(months)
	ax.xaxis.set_major_locator(years)
	ax.xaxis.set_minor_formatter(yearsFmt)
	
for tick in ax.xaxis.get_major_ticks(): tick.set_pad(16)
#ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d')) #Show the date
ax.xaxis.set_major_formatter(DateFormatter('')) #Hide the date
#ax.xaxis.set_minor_formatter(DateFormatter('%H Z'))

#Make a file name
plotfile='visit/'+`os.getpid()`+'.png' #Create a unique file name using the process ID
dotsperinch=72
#Log all visits to your plotter
try:
	log=open('visit/log.dat','a')
	log.write(plotfile+" , "+os.environ["REMOTE_ADDR"]+"\n")
	log.close()
except:
	print "Oops...can't write to log file."

#Create the hardcopy plot
try:
	savefig(plotfile, dpi=dotsperinch, facecolor='w', edgecolor='w', orientation='portrait')
	os.chmod(plotfile,0644) #Set file permissions
except:
	print "Uh-oh, Blizzard can't save ",plotfile

#HTML source to show the plot
print '<hr><img src="'+plotfile+'"><p>'
###########################################################

###########################################################
#Clean up old plots in your visit/ directory
if verbose: print "<hr>Searching for old files:<p>"
visitfiles=glob.glob('visit/*.png') #List the files in the visit/ directory
ct=time.time()
for f in visitfiles:
	stats=os.stat(f)
	ctime=ct-stats[-1]
	if verbose>0: print f,ctime,"<br>"
	if (ctime>1000.): os.remove(f) #Remove files older than 1000 seconds
###########################################################

###########################################################
# Your job:
# Improve wxplot.cgi to accomplish the following:
# 1) Plot more than one day of data (i.e., from a "start date" to an "end date")
#    with the dates chosen by the user.
# 2) Overlay the time series for temperature at two specified stations.
# 3) Plot multiple variables from the same site on the same plot (these options
#    MUST include at least air temperature and dewpoint.
# 4) Clean up your page to make it somewhat attractive and useful. Be creative.
###########################################################
