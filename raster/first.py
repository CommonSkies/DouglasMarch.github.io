#!/usr/bin/python

#This program produces a PPM image, given
#a green value for all pixels.

width=256
height=256
comment='You can write a comment here'
ftype='P3' #use 'P3' for ascii, 'P6' for binary
 
#Get input for green value
green=int(raw_input("Enter a green value between 0 and 255: "))
print "Setting green =",green

#Open PPM file
ppmfile=open('first.ppm','wb')

#Write header
ppmfile.write("%s\n" % (ftype)) 
ppmfile.write("#%s\n" % comment ) 
ppmfile.write("%d %d\n" % (width, height)) 
ppmfile.write("255\n")
 
#Write RGB triplets
for i in range(width):
	for j in range(height):
		red=i
		blue=j
		if ftype=='P3':
			ppmfile.write("%d %d %d\n" % (red,green,blue)) 
		elif ftype=='P6': #print 1 byte per color
			ppmfile.write("%c%c%c" % (red,green,blue))
 
#Clean up
ppmfile.close()
print """Wrote first.ppm.  View it with "eog first.ppm"."""

