* Run this GrADS script from the Unix command line with: grads -blc "run plots.gs"
* The original script produces three PNG images.
* To complete the assignment, modify the script to produce the following four plots:
*   1) 850-mb heights and wind vectors (colored by magnitude) for 00Z 30 August 2005
*   2) 850-mb relative vorticity for 00Z 30 August 2005
*   3) 850-mb divergence for 00Z 30 August 2005
*   4) 24-hour 850-mb height tendency (dZ/dt) centered on 00Z 30 August 2005
* Make all plots
*   a) on a white background, 
*   b) centered on the area of interest,
*   c) on a latitude-longitude map projection
*   d) with an appropriate title, and 
*   e) on a high-resolution base map showing the U.S. states.

*Open these control files for all plots
***'open /REANALYSIS/1974/ctl/at00z12z/hgt.prs'
'open /REANALYSIS/2005/ctl/at00z12z/hgt.prs'
'open /REANALYSIS/2005/ctl/at00z12z/ugrd850.prs'
'open /REANALYSIS/2005/ctl/at00z12z/vgrd850.prs'
************************
'set grads off'
'set lev 850'
'set lat 24.0 45.0'
'set lon -105.0 -75.0'
'set t 483' 
*#####Time is in #12-hour intervals beginning at 00 UTC 1 Jan
*#####Set time to "value" time in data set
'q time'
timeinfo=result
timelab=substr(timeinfo,8,12)
'set display color white'
*#####Set background color to white(1) default is black (0)
'set cthick 7'
*#####Set contour thickness
'set clopts -1 3 0.09'
*#####Set contour label <thickness <size>>
timelab='850 mb wind field and heights for 'timelab
'set gxout contour'
*#####Graphics out
'set mproj latlon'
*#'set mproj nps'
*#####Maps Projection/North Pole Sterographic
'set mpdset hires'
*#'set mpdset r5.dat'
*#####Set map with imported mapdata
'set mpt 5 1 1 1'
*#####Distinguished map lines between boarder or coast and states
'draw map'
'set mpt 3 1 1 12'
'draw map'
'd hgt'
*'d ugrd.2'
*#####Adds u wind vector
*'d vgrd.3'
*#####Adds v wind vector
'set gxout vector'
*'set ccolor rainbow'
*#####Sets color of the arrows
'set cmax 100'
'set arrscl .25 10'
*#####Sets arrow size and magnitude of each arrow
'set arrowhead -0.4'
*#####Sets arrowhead size <0 scale >0 all same =0 no head
'set arrlab on'
*#####Shows legend on base
'set cthick 6'
'd ugrd.2;vgrd.3;mag(ugrd.2,vgrd.3)'
*#####The mag adds color to the arrows
'set string 1'
'set strsiz 0.20'
*#####'draw string 3.5 0.85 Stuff and such'
'draw title 'timelab
'printim a.png'
'clear'
************************
'set grads off'
'set grid on'
'set lev 850'
'set lat 24.0 45.0'
'set lon -105.0 -75.0'
'set t 483'
'q time'
timeinfo=result
timelab=substr(timeinfo,8,12)
timelab='850 mb relative vorticity (s`a-1`n) for 'timelab
'set gxout vector'
'set mproj latlon'
*#'set mproj mollweide'
'set mpdset hires'
*#'set mpdset lowres' ###Low resolution
'd hcurl(ugrd.2,vgrd.3)'
**'d ugrd.2'
'draw title 'timelab
'printim b.png'
'clear'
************************
'/usr/local/lib/grads/white.gs'
'set grads off'
'set grid on'
'set lev 850'
'set lat 24.0 45.0'
'set lon -105.0 -75.0'
'set t 483'
'q time'
timeinfo=result
timelab=substr(timeinfo,8,12)
timelab='850 mb divergence (s`a-1`n) for ' timelab
'set gxout contour'
*#####Originaly set with shaded
'set mproj latlon'
*#'set mproj robinson'
'd hdivg(ugrd.2,vgrd.3)'
*#Heights at another time
'set gxout contour'
***'d hgt(t=380)'
'/usr/local/lib/grads/cbarn.gs'
'draw title 'timelab
'printim c.png'
'clear'
************************
'set lev 850'
'set lat 24.0 45.0'
'set lon -105.0 -75.0'
*Time is in #12-hour intervals beginning at 00 UTC 1 Jan
'set t 483'
'q time'
****tloop(hgt) ***For looping animation
timeinfo=result
timelab=substr(timeinfo,8,12)
'set display color white'
'set clopts -1 3 0.09'
timelab='850 mb height tendency (gpm) for 'timelab
'set gxout contour'
'set mproj latlon'
'set mpdset hires'
'set mpt 5 1 1 1'
'draw map'
'set mpt 3 1 1 12'
'draw map'
'd hgt (t=484)-hgt(t=482)'
**'d hgt (t=484)-hgt(t=482)'
**'d hgt(t+2) - hgt'
**'d hgt'
*#####Draws hgt or hgt between two times and averaged 
'set gxout vector' 
'set string 1'
'set strsiz 0.20'
****'draw string 3.5 0.85 Stuff and such'
'draw title 'timelab
'printim d.png'
'clear'

'quit'
