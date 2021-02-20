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
from matplotlib import pylab
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
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
#	print form
#	print "The CGI form has keys:",form.keys(),"<p>"
#	for key in form.keys():
#		print key,':', form[key].value,'<br>'
#	print "<p>"
	site=form['stid'].value
	site2=form['stid2'].value
	degrees=form['scale'].value
	startdate=form['startdate'].value
	enddate=form['enddate'].value
	dewpoint="on"
	dewpoint=form['dewpoint'].value
#except:# Exception as e:
except Exception as e:
#	print "There was an exception for: ", e
#	startdate="20090324" #Default date
#	enddate="20090325" #Default date
#	site="NRMN" #Default site
#	site2="----"
	dewpoint="off"
	#degrees="Fahrenheit" #Default temperature scale
	degrees=form['scale'].value

###########################################################

###########################################################
#Use user input to make the Mesonet File name, then go get it.
#Syear=startdate[0:4]
#Eyear=enddate[0:4]
#Smonth=startdate[4:6]
#Emonth=enddate[4:6]
#Sday=startdate[6:8]
#Eday=enddate[6:8]
#**************************

#startdate=str(20090524)
startdate=str(startdate)
#enddate=str(20090528)
enddate=str(enddate)
#print type(startdate) is str				#Easy way to test the type ie int, long, list, tuple, etc *Returns boolean function

from datetime import datetime as dt,timedelta,date
import time
from time import strftime

Sdt_obj = dt.strptime(startdate,"%Y%m%d")		#Converts to obj
#Sdt_obj = Sdt_obj.strftime("%Y%m%d")			#Converts to str
Edt_obj = dt.strptime(enddate,"%Y%m%d")
#Edt_obj = Edt_obj.strftime("%Y%m%d")

datelist=[startdate]
hours=mdates.HourLocator() #every hour

newdt=startdate
for i in range(0,(Edt_obj - Sdt_obj).days):
		newtime=dt.strptime(newdt,'%Y%m%d')      	#Convert the date to a datetime object
		newt=newtime+timedelta(days=1.0)  			#Subtract tzoffset hours
		newdt=newt.strftime('%Y%m%d')               #Convert date to YYYYMMDDHH format
		datelist.append(newdt)
x=np.asarray(datelist)

daylist=[]
majorlist=[]
newlist=[]
midnightlist=[]
for d in datelist:
	daylist.append(d[0:8])
daylist=set(daylist)

for m in daylist:
	majorlist.append(m+"0000")
	majorlist.append(m+"0300")
	majorlist.append(m+"0600")
	majorlist.append(m+"0900")
	majorlist.append(m+"1200")
	majorlist.append(m+"1500")
	majorlist.append(m+"1800")
	majorlist.append(m+"2100")
    #Avoid blank areas outside the bounds of the period under consideration


for m in majorlist:
	majorlist=newlist
	if int(m) >= int(datelist[0]) and int(m) <= int(datelist[-1]):
		 newlist.append(m)
	myticks=np.array([datetime.strptime(d,"%Y%m%d%H%M") for d in majorlist])

content=[]
for d in datelist:
	file="http://www.mesonet.org/data/public/mesonet/mts/YYYY/MM/DD/YYYYMMDDSTID.mts"
	year=d[0:4]
	month=d[4:6]
	day=d[6:8]	
	file=file.replace('YYYY',year)
	file=file.replace('MM',month)
	file=file.replace('DD',day)
	file=file.replace('STID',site.lower())  #Make station ID lower case; put in file name
#	Print 'Retrieving file: <a href="',file,'">',file,'</a>'
	try:
		content.append(urllib2.urlopen(file).readlines()) # Read the text at the URL "file"
	except:
		print "<p>Uh-oh...something went wrong reading the Mesonet data file"
		sys.exit()

if site2 != '----':
	content2=[]
	for d in datelist:
		file2="http://www.mesonet.org/data/public/mesonet/mts/YYYY/MM/DD/YYYYMMDDSTID.mts"
		year=d[0:4]
		month=d[4:6]
		day=d[6:8]
		file2=file2.replace('YYYY',year)
		file2=file2.replace('MM',month)
		file2=file2.replace('DD',day)
		file2=file2.replace('STID',site2.lower())  #Make station ID lower case; put in file name
#		print 'Retrieving file: <a href="',file2,'">',file2,'</a>'
		try:
			content2.append(urllib2.urlopen(file2).readlines()) # Read the text at the URL "file"
		except:
			print "<p>Uh-oh...something went wrong reading the Mesonet data file"
			sys.exit()
###########################################################
###########################################################


#Manipulate the data in the file
tairs=[]
dates=[]
#satvpres=[]
#vpres=[]
dwpts=[]
nummissing=0

for d in range (len(content)): 
	nl=0
	for line in content[d]:
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
		relhfloat=float(relh)
		relhfloat=relhfloat/100.
		if tairfloat > -990.:
			satvpres=float(6.112*exp((17.67*tairfloat)/(tairfloat+243.5)))
			vpres=(relhfloat*satvpres)
			dwpt=((243.5*log(vpres/6.112))/(17.67-log(vpres/6.112)))
			dwptfloat=float(dwpt)
		if tairfloat < -990.:
			nummissing+=1
		elif degrees=='Fahrenheit':
			tairfloat=tairfloat*1.8+32.
			dwptfloat=dwptfloat*1.8+32.
		tairs.append(tairfloat)
		dwpts.append(dwptfloat)
if nummissing > 0:
	print "<p>There are/is",nummissing,"missing value(s) from",site,".","<br>"
###########################################################
#Lazy code for station 2
if site2 != '----':
	tairs2=[]
	dates2=[]
	satvpres=[]
	vpres=[]
	dwpts2=[]
	nummissing=0
	for d in range (len(content2)):
		nl=0
		for line in content2[d]:
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
			dates2.append(dnum)
			tairfloat=float(tair)
			relh=float(relh)/100
			if tairfloat > -990.:				#Could add this to compare dwpts over graph
				satvpres=6.112*exp((17.67*tairfloat)/(tairfloat+243.5))
				vpres=float(relh/100.)*satvpres
				dwpt=((243.5*log(vpres/6.112))/(17.67-log(vpres/6.112)))
				dwptfloat=float(dwpt)
			if tairfloat < -990.:
				nummissing+=1
			elif degrees=='Fahrenheit':
				tairfloat=tairfloat*1.8+32.
				dwptfloat=dwptfloat*1.8+32.
			tairs2.append(tairfloat)
			dwpts2.append(dwptfloat)
	if nummissing > 0:
		print "<p>There are",nummissing,"missing values from",site2,".","<br>"
###########################################################
#Test behavior for missing values
#tairs[10]=-991. #Uncomment to test with artificial missing value
#tairs[20]=-991. #Uncomment to test with artificial missing value
#tairs[30:40]=[-991.]*10 #Uncomment to test with artificial missing value
###########################################################

from matplotlib.lines import Line2D
from matplotlib.text import Text
import matplotlib.dates as mdates
from matplotlib.dates import HourLocator
from matplotlib.ticker import FixedLocator

###########################################################
#Use matplotlib to make a PNG file in the visit/ directory
figure(figsize=(12,6))

#Define tick marks

years=mdates.YearLocator()				#Every year
months=mdates.MonthLocator()			#Every month
weeks=mdates.DayLocator(range(0,365,7))	#Every week
#days7x=mdates.DayLocator(0,365,7)
days=mdates.DayLocator()				#Every day 
hours=mdates.HourLocator()				#Every hour
hours3=HourLocator(range(0,24,3))		#Every 3 hours  
hours6x=HourLocator(range(0,24,6))		#Every 6 hours  

#Try these commands for testing:
datesx=[x-dates[0] for x in dates]
#plot(datesx,dwpts,'k') #This uses the raw date in "days" on the x-axis
#plot_date(dates,tairs,'k') #This works nicely as long as you don't have missing values

y_maskedi=ma.MaskedArray(tairs)
y_masked=ma.masked_where(y_maskedi<-990.0,y_maskedi) #Ignore data with missing values

if dewpoint == 'off' and site2 == '----':
	pylab.plot_date(dates,y_masked,'k',color='k',marker='.',label="Temperature") #Plot the data

if dewpoint == 'on':
	y2_maskedi=ma.MaskedArray(dwpts)
	y2_masked=ma.masked_where(y2_maskedi<-990.0,y2_maskedi) #Ignore data with missing values
	pylab.plot_date(dates,y_masked,'k',color='k',marker='.',label="Temperature") #Plot the data
	pylab.plot_date(dates,y2_masked,'b',color='b',marker='.',label="Dewpoint") #Draw a second curve. Changed y2_masked+2

if site2 != '----' and dewpoint != 'on':
	y2_maskedi=ma.MaskedArray(tairs2)
	y2_masked=ma.masked_where(y2_maskedi<-990.0,y2_maskedi) #Ignore data with missing values

###########################################################
#These lines might help you with your assignment. Each command plots a second curve.
###########################################################
#plot(dates,y_masked,'k',dates,y_masked+2.,'b') #This works for "plot", but not for "plot_date"

	pylab.plot_date(dates,y_masked,'k',color='k',marker='.',label=site) #Plot the data
	pylab.plot_date(dates,y2_masked,'b',color='b',marker='.',label=site2) #Draw a second curve

###########################################################
if dewpoint == 'on' and site2 != '----':
	print "<b>Uncheck Dewpoint or leave Station 2 blank</b>"
	sys.exit(0)
###########################################################

#plt.gcf().autofmt_xdate()
#Plot data
ax=gca() #gca() gets the currrent axes

#Set up axes and labels
xlim(dates[0],dates[-1])  
if degrees=="Celsius":
	ylabel("Temperature ($^\circ$C)", size=20, rotation=90)
else:
	ylabel("Temperature ($^\circ$F)", size=20, rotation=90)

xlabel("Date", size=20, rotation=0)
#pylab.legend(loc=9, bbox_to_anchor=(0.5,-0.15),ncol=2)
pylab.legend(loc=9, ncol=2)

if dewpoint == 'on' or site2 != '----':
	ylim((np.min(y2_masked)-2),(np.max(y_masked)+2))

if dewpoint=='on':
	ax2 = ax.twinx()
	ylim((np.min(y2_masked)-2),(np.max(y_masked)+2))
	#ax2.plot(dates,y2_masked,'b',color='b',marker='.',label=site2) #Draw a second curve
	if degrees=="Celsius":
		ax2.set_ylabel("Dewpoint ($^\circ$C)", size=20, rotation=90)
	else:
		ax2.set_ylabel("Dewpoint ($^\circ$F)", size=20, rotation=90)

if dewpoint != 'on':
	if site2 == '----':
		title("Temperature at mesonet site: "+site)
	else:
		title("Temperature at mesonet site: "+site+" & "+site2)
else:
	title("Temperature and Dewpoint at mesonet site: "+site)

#Set ticks
ax.xaxis.set_ticks(myticks)
#ax.xaxis.set_major_formatter(mdates.DateFormatter('%-I:%M %p\n%-m/%-d/%Y'))

for tick in ax.xaxis.get_major_ticks(): tick.set_pad(16)
#ax.xaxis.set_major_formatter(DateFormatter('')) #Hide the date
#ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H Z'))


#Set up axes and labels
#If statement for each day, week, month, etc

datesx = round(max(datesx))
if (datesx <= 3.0):
	ax.xaxis.set_minor_locator(hours3)
	ax.xaxis.set_major_locator(days)
	for tick in ax.xaxis.get_major_ticks(): tick.set_pad(16)
	#ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d')) #Show the date
	ax.xaxis.set_major_formatter(DateFormatter('')) #Hide the date
	ax.xaxis.set_minor_formatter(DateFormatter('%HZ'))

if (datesx >  3.0 and datesx <= 6.0):
    ax.xaxis.set_minor_locator(hours6x)
    ax.xaxis.set_major_locator(days)
    for tick in ax.xaxis.get_major_ticks(): tick.set_pad(16)
    #ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d')) #Show the date
    ax.xaxis.set_major_formatter(DateFormatter('')) #Hide the date
    ax.xaxis.set_minor_formatter(DateFormatter('%HZ'))

if (datesx > 6.0 and datesx <= 15.0):
    ax.xaxis.set_minor_locator(days)
    ax.xaxis.set_major_locator(weeks)
    for tick in ax.xaxis.get_major_ticks(): tick.set_pad(16)
    #ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d')) #Show the date
    ax.xaxis.set_major_formatter(DateFormatter('')) #Hide the date
    ax.xaxis.set_minor_formatter(DateFormatter('%m-%d'))

if (datesx > 15.0 and datesx <= 40.0):
    ax.xaxis.set_minor_locator(days)
    ax.xaxis.set_major_locator(months)
    for tick in ax.xaxis.get_major_ticks(): tick.set_pad(16)
    #ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d')) #Show the date
    ax.xaxis.set_major_formatter(DateFormatter('%B')) #Hide the date
    ax.xaxis.set_minor_formatter(DateFormatter('%d'))

if (datesx > 40.0):
    ax.xaxis.set_minor_locator(weeks)
    ax.xaxis.set_major_locator(months)
    for tick in ax.xaxis.get_major_ticks(): tick.set_pad(16)
    #ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d')) #Show the date
    ax.xaxis.set_major_formatter(DateFormatter('%B')) #Hide the date
    ax.xaxis.set_minor_formatter(DateFormatter('%U'))

if (datesx > 200.0):
	print "Why are you printing this off? Its not gonna work!"


#Format the dates on the x axis
#xax = ax.get_xaxis() # get the x-axis
#ax.xaxis.set_major_locator(months)
#ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d')) #Show the date
#ax.xaxis.set_minor_locator(hours3)
#ax.fmt_xdata=mdates.DateFormatter(hours3)
#ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H')) #Show the hour
#ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M')) #Show the hour
#ax.tick_params(axis='x', labelsize=9,)# pad=15)
#labels = ax.get_xticklabels()
#plt.setup(labels,rotation=30,fontsize=10)

#Beautify the x-labels
plt.gcf().autofmt_xdate()

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




class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#print color.BOLD + 'Hello World !' + color.END




if (datesx > 40.0 and datesx <= 100.0):
	print "*************************************************************************************************"
	print "***************************************These Ticks are Weeks in a Month******************************"
	print "***********************************The Numbers are in Units of Weeks per Year**************************"
	print "*************************************************************************************************"

###########################################################
#Clean up old plots in your visit/ directory
#if verbose: print "<hr>Searching for old files:<p>"
visitfiles=glob.glob('visit/*.png') #List the files in the visit/ directory
ct=time.time()
for f in visitfiles:
	stats=os.stat(f)
	ctime=ct-stats[-1]
	#if verbose>0: print f,ctime,"<br>"
	if (ctime>1000.): os.remove(f) #Remove files older than 1000 seconds
###########################################################
#There are several things I would like to improve upon this
#Mostly the plot: There are ticks on the other x-axis, The size of the x-axis numbers, Minor ticks on the y-axis, move the legend to the outside of the plot, etc
#Another thing would be to change the site itself. I would love a dynamic picture for the homepage or just a picture you can interact with. 
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
