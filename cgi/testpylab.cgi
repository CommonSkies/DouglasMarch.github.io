#!/usr/bin/python
#This script looks best when executed by a Web browser. Visit
#http://yourserver/directory/testpylab.cgi

#Thanks to Brian Fiedler for most of this code. Modified by C. Godfrey.
#Please change the "cgodfrey" below.

import sys,os
import cgitb; cgitb.enable()
print "Content-type: text/html\n"
pid=os.getpid()
os.environ['HOME']="/home/dmarch/public_html/cgi/visit" #Make this your directory!!
import matplotlib
matplotlib.use('Agg')  #Prevent matplotlib from preparing to open GUI (and crashing)
testfile= "visit/test"+`pid`+".png"
print "<p>The purpose of this script is to try to make "+testfile+" in the visit directory with matplotlib.</p>"
try:
	import pylab
except:
	print "Oops...could not import pylab."
pylab.plot([3,6,8,1,6,3,5,4],[8,2,5,3,6,8,6,4])
pylab.savefig(testfile)
print "View the file here:<br>"
print '<img src="'+testfile+'"><br>'
print "I guess it worked."
