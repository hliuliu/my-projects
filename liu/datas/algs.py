

def ackermann(x,y):
	if type(x)!=int or type(y)!=int:
		raise TypeError
	if x<0 or y<0:
		raise ValueError
	if x==0:
		return y+1
	if y==0:
		return ackermann(x-1,1)
	return ackermann(x-1,ackermann(x,y-1))


def majority(l):
	item,count=None,0
	for i in l:
		if not count:
			item=i
			count+=1
		elif count>0:
			if item==i:
				count+=1
			else:
				count-=1
	count=0
	for i in l:
		if item==i:
			count+=1
	if count>len(l)/2:
		return item
	return None

def distinct(l):
	dis=[]
	for i in l:
		if i not in dis:
			dis.append(i)
	return dis

def partsort(l,k):
	if type(l)!=list or type(k) not in [int,long]:
		raise TypeError
	if not 0<=k<len(l):
		return
	piv=l[-1]
	j=0
	for i in range(len(l)-1):
		if l[i]<piv:
			l[i],l[j]=l[j],l[i]
			j+=1
	l[-1],l[j]=l[j],piv
	if j==k:
		return
	if j<k:
		m=l[j+1:]
		partsort(m,k-j-1)
		l[j+1:]=m
	else:
		m=l[:j]
		partsort(m,k)
		l[:j]=m

def kthsmallest(k,*args):
	args=list(args)
	partsort(args,k)
	return args[k]

def heapsort(l):
	from trees import heap
	h=heap()
	while l:
		h.insert(l.pop(0))
	for i in h:
		l.append(i)

def identical(l):
	has=False
	curr=None
	for i in l:
		if has and i is not curr:
			return False
		has=True
		curr=i
	return True

def same_value(l):
	has=False
	curr=None
	for i in l:
		if has and i != curr:
			return False
		has=True
		curr=i
	return True

def commonelements(*args):
	if not args:
		return []
	from copy import deepcopy
	if len(args)==1:
		return deepcopy(args[0])
	a1=commonelements(*args[:len(args)/2])
	a2=commonelements(*args[len(args)/2:])
	res=[]
	for i in a1:
		if i in a2:
			res.append(deepcopy(i))
	return res


