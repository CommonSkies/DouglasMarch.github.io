#!/usr/bin/env python 
import cgi,sys,string
import cgitb; cgitb.enable()
print "Content-Type: text/html\n\n"
print dir(cgi),"<br><br>"
The_Form = cgi.FieldStorage()
if The_Form.has_key("pickme"):
	print "You checked it out!<br>"
else:
	print "You didn't check it out!<br>"
for name in The_Form.keys():
	print "Input: " + name + " value: " + The_Form[name].value + "<BR>"

try:
	bigline=The_Form['sometext'].value
except:
	bigline=""
lines=string.splitfields(bigline,'\r')
num=len(lines)-1
print "<hr><b>Python can parse the input</b><br>"
print """We can split "sometext" into """,  num ,""" lines:<br>"""
for line in lines:
	print line + "<br>"

print "<hr><b>Test error messages:</b><br>"
print "Deliberate mistake" + num 
