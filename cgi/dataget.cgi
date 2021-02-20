#!/usr/bin/python
#Thanks to Brian Fiedler for much of this script.  Modified by Christopher Godfrey.
import sys, urllib2,os,cgi
import cgitb; cgitb.enable()
print "Content-type: text/html\n"
print """\n<html>\n<head>\n<link rel=stylesheet href="style.css" type=text/css>\n</head>\n<body>"""
file="http://www.mesonet.org/data/public/mesonet/latest/latest.mdf"

try:
	form=cgi.FieldStorage()
#	print "The CGI form has keys:",form.keys(),"<p>"
#	for key in form.keys():
#		print key,':', form[key].value,'<br>'
#	print "<p>"
	site=form['stid'].value
	degrees=form['scale'].value
except:
	site="NRMN" #Default site
	degrees="Celsius" #Default temperature scale
try:
	content=urllib2.urlopen(file).readlines() # This reads the text at the URL "file"
except:
	print "Uh-oh, the script can't open the latest mesonet data file!"
	print "</body></html>"	
	sys.exit()
nl=0
for line in content:
	nl+=1
	if nl==1 : continue #Copyright line
	if nl==2 : #Time header
		try:
			line=line.strip()
			year,month,day=line.split()[1:4]
		except:
			print "Problem parsing the time information."
			print "</body></html>"	
			sys.exit()
	if nl==3 : continue #Column labels  
	line=line.strip()
	items=line.split()
	try:
		stid,stnm,minutes,relh,tair,wspd=items[0:6]
	except:
		print "Problem splitting the text into separate items."
		print "</body></html>"	
		sys.exit()
	
	if stid==site:
		hour=int(minutes)/60
		minu=int(minutes)%60
		clock="%2.2d:%2.2d" % (hour,minu)
		timestring=month+'/'+day+'/'+year+' at '+clock+' UTC'
		deg='&#176;C'
		if degrees=="Fahrenheit":
			tfar=float(tair)*1.8+32.
			tair='%5.1f' % tfar
			deg='&#176;F'
		print "<font size='7'><b>"+"The latest mesonet data for "+site+" is from "+timestring+"</b></font>"+"<br>"
		print "<br>"
		print "<b>"+"The air temperature for "+site+" at that time was:",tair,deg+"</b>"+"<br>"
		print "<br>"
		print "<b>"+"The relative humidity for "+site+" at that time was:",relh+"%"+"</b>"+"<br>"
		print "<br>"
		print "<b>"+"The windspeed for ",site, " at that time was:",wspd+" mph"+"</b>"+"<br>"
		print "<br>"+"<br>"+"<br>"+"<br>"+"<br>"+"<br>"+"<br>"+"<br>"+"<br>"+ "<br>"+"<br>"+"<br>"
		print "<center><img src='http://i.imgur.com/iiqD7OI.jpg' alt='Oklahoma' height='300' width='400'></center>"
		print "</body></html>"	
		sys.exit()
print "Uh-oh. There is no information for "+site+" in the data file!"
