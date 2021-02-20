#!/usr/bin/python
#Usage: vegimg.py fvegMOD15A2.txt
import sys,string
from math import *

### MAKE PRETTY COLORS
#########################################
# YOUR TURN (PART I): Assign several appropriate colors for vegetation (usually
# brown->yellow->green).  Search Google for HTML color tables to find the
# colors that you want and then experiment with them.  
#########################################

hex="35181B 3F2620 4A3527 55432C 635531 736934 837E36 949436 A5AB37 B5C035 C5D92F D6E040 A4CE39 9EC03B 7BB742 73A541 69913D 4A8E41 2C7C3F 007741 00794A 006941 005838 014B31  004839 083C31 0D332B 0D2E27 000000  0A4d88 742158 E1DFDF 02C3F3 666666 EA098B ".split()
rgb=[] #Will contain three-byte strings describing colors

for code in hex:
	#NOTE: int(x,radix) converts a string 'x' to an integer,
	#where 'radix' is the base for the conversion (e.g., base 16)
	triplet=[int(code[col*2:col*2+2],16) for col in range(3)]
	c3="%c%c%c" % tuple(triplet) #Convert to binary
	rgb.append(c3) #Store the color as 3 bytes

#Make a color bar
cbar=open("vegcolors.ppm",'wb')
cbar.write('P6\n')
cbar.write('#Vegetation colors\n')
cbar.write("1 %d\n" % len(rgb))
cbar.write("255\n")
rgb.reverse()
cbar.write("".join(rgb)) #Concatenate a list of strings
rgb.reverse()
cbar.close()
print "Wrote color bar in vegcolors.ppm" 

##### RASTERIZE THE DATA 
#Open data file
try:
	filename=sys.argv[1]
except:
	filename=raw_input("Enter name of vegetation data file => ")
infile=open(filename,'r')

#Read the four header lines with x-y dimensions
header={}
for i in range(4):
	header[i]=infile.readline().strip()
ydim=string.atoi(header[1])
xdim=string.atoi(header[3])

print "The x-dimension is "+repr(xdim)+" and the y-dimension is "+repr(ydim)+"."

#Read the rest of the lines in the data file
lines=infile.readlines()

image=open("vegimg.ppm",'wb')
image.write('P6\n')
image.write('#MOD15A2 MODIS/Terra Gridded 1-km Fraction of Photosynthetically Active Vegetation (8-Day Composite)\n')
image.write("%d %d\n" % (xdim,ydim)) 
image.write("255\n")
print "Reading data from "+filename

#########################################
# YOUR TURN (PART II): There are special values in the data file that represent
# unclassified pixels, urban areas, wetlands, snow, barren land, and water, in
# addition to the vegation fraction values from 0% to 100%.  Use the information
# in format.txt to assign special colors to each of these types of land cover.
# Water, for example, might look nice in blue.
#
# When you are satisfied with your color scheme, use inkscape to combine your
# images and add annotation.  Then post your finished plot on your Web page. 
#########################################
for line in lines:
	#Assign a hexadecimal color value to each pixel using the "rgb" array
	if string.atoi(line) > 200:
		######
		#Change this block of code to assign different colors to special values
		if string.atoi(line)==255:
			c=rgb[len(hex)-7]   #Fill is Black
		elif string.atoi(line)==254:
			c=rgb[len(hex)-6]   #Water is Blue
		elif string.atoi(line)==253:
			c=rgb[len(hex)-5]   #Barren is Burgandy
		elif string.atoi(line)==252:
			c=rgb[len(hex)-4]   #Snow and Ice is Light Gray
		elif string.atoi(line)==251:
			c=rgb[len(hex)-3]   #Wetlands is Lighter Blue
		elif string.atoi(line)==250:
			c=rgb[len(hex)-2]   #Urban is Medium Gray
		elif string.atoi(line)==249:
			c=rgb[len(hex)-1]	#Unclassified is Pink
#		c=rgb[len(hex)-1]	#Assign last color in scale to values > 200
		######
	else:
		c=[rgb[int(string.atoi(line)/(100./float(len(hex))))-8]]
	image.write("".join(c))

image.close()
print "Wrote image file vegimg.ppm" 
