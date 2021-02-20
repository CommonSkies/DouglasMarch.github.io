#!/usr/bin/env python
import sys, cPickle, struct, string, re, getopt 
options, args= getopt.getopt(sys.argv[1:],'sv')
splitAtSpace=False
verbose=False
for theopt,thearg in options:
	if theopt=='-s': 
		splitAtSpace=True
	elif theopt=='-v': 
		verbose=True
	else:
		print "what are these??? ", theopt, thearg
		sys.exit()

for infile in args:
	outfile=infile
	outfile=re.sub(r'^.*/',r'pickleMaps/',outfile)
	if re.search(r'.mapdata',outfile):
		outfile=re.sub(r".mapdata",r".pickle",outfile)
	else:
		outfile=outfile+".pickle"
	print "\nwill read data file= ", infile
	print "will write to pickle file= ", outfile
	if outfile==infile:
		print "something went wrong with pickle file name"
		sys.exit()
	inf=open(infile,'r')
	lines=[]
	heads=[]
	pairs=[]
	nl=0
	while 1:
		nl+=1
		a=inf.readline()
		if not a: break
		if a[0]=="#":
			if verbose: print a,
			continue
		a=a.rstrip()
		if verbose: print nl
		if a[0:4]=="    ": #found next line
			if pairs: lines.append(pairs) #dump out previous line
			pairs=[]
			inhead=a.strip().split()
			rectype=int(inhead[1])
			if splitAtSpace: #values separated by spaces
				v=inhead
			else:  #exactly 8 characters per value
				num=len(a)/8
				v=list(struct.unpack('8s'*num,a))
			if verbose: print rectype, v
			if rectype>0:
				heads.append(v)
			else:
				break # rectype<=0 means and of file 
		else:
			if splitAtSpace: #values seperated by spaces
				v=a.strip().split()
			else:  #exactly 8 characters per value
				num=len(a)/8
				v=list(struct.unpack('8s'*num,a))
			for i in range(0,len(v),2): # make order longitude, latitude
				v[i],v[i+1]=v[i+1],v[i]
			pairs+=[eval(x) for x in v]
	maplines={}
	maplines['heads']=heads
	maplines['lines']=lines
	oup=open(outfile,'w')
	print "will write heads and lines arrays of lengths:", len(heads),len(lines)
	print "opening pickle file",outfile
	cPickle.dump(maplines,oup)
	print "pickle file",outfile,"was written"
