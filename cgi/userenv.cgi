#!/usr/bin/python 
import sys,os,time,cgi
import cgitb; cgitb.enable()
print "Content-type: text/html"
print """\n<html>\n<head>\n<link rel=stylesheet href="style.css" type=text/css>\n</head>\n<body>"""
print "<pre>"
print "Time on the server:",time.asctime()
print "Process id for this script:",os.getpid()

print "The QUERY_STRING is:", os.environ['QUERY_STRING'] 
print "The STDIN is:", sys.stdin.readline()
print "The ARGV is:", sys.argv

try:
	form=cgi.FieldStorage()
	print "\nThe CGI form has the following keys:",form.keys()
	for key in form.keys():
		print key,':', form[key].value
except:
	print "No Field Storage"
	print "\n\n"

print "\nInformation about your server:"
keys=os.environ.keys()
for key in keys:
	print key,":",os.environ[key]
print "</pre>"
print "</body></html>"
