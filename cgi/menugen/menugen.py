/usr/bin/python
# usage: mengen.py > menu
mdf=open('latest.mdf','r')
all=mdf.readlines()
for line in all[3:]:
	v=line.split()
	id=v[0]
	print '<option value="'+id+'">'+id
