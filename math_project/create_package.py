
import os,sys

path=sys.argv[1]
names= sys.argv[2:]

for name in names:
	pname=os.path.join(path,name)
	if not os.path.exists(pname):
		os.mkdir(pname)
		open(os.path.join(pname,'__init__.py'),'w').close()
	else:
		print '%s exists, no change are made.'%pname



