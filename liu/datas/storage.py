

class sortedlist(object):
	def __init__(self,it=[]):
		from copy import deepcopy
		self.__store=list(deepcopy(it))
		self.__store.sort()
	def __len__(self):
		return len(self.__store)
	def __nonzero__(self):
		return bool(len(self))
	def add(self,el):
		from copy import deepcopy
		if not self:
			self.__store.append(deepcopy(el))
			return
		low,high=0,len(self)
		while low<high:
			mid=(low+high)/2
			if el<self.__store[mid]:
				high=mid
			else:
				low=mid+1
		self.__store.insert(low,el)
	def __contains__(self,el):
		from copy import deepcopy
		el=deepcopy(el)
		low,high=0,len(self)
		while low<high:
			mid=(low+high)/2
			if self.__store[mid]==el:
				return True
			if self.__store[mid]<el:
				low=mid+1
			else:
				high=mid
		return False
	def index(self,el):
		low,high=0,len(self)
		while low<high:
			mid=(low+high)/2
			if self.__store[mid]<el:
				low=mid+1
			else:
				high=mid
		return low
		raise ValueError('%s not in sortedlist'%el)
	def remove(self,el):
		try:
			i=self.index(el)
			self.__store.pop(i)
		except ValueError:
			raise ValueError('%s not in sortedlist'%el)
	def __iter__(self):
		from copy import deepcopy
		for i in self.__store:
			yield deepcopy(i)
	def get(self,index):
		from copy import deepcopy
		return deepcopy(self.__store[index])
	def delat(self,index):
		self.__store.pop(index)
	def sublist(self,start=None,stop=None,step=1):
		if start==None:
			start=0
		if stop==None:
			stop=len(self)
		res=sortedlist(list(self)[start:stop:step])
		return res
	def __eq__(self,other):
		if not isinstance(other,sortedlist):
			return False
		return self.__store==other.__store
	def __repr__(self):
		return str(self)
	def __str__(self):
		return str(self.__store)
	def __lt__(self,other):
		if not isinstance(other,sortedlist):
			return NotImplemented
		return self.__store<other.__store
	def __gt__(self,other):
		if not isinstance(other,sortedlist):
			return NotImplemented
		return self.__store>other.__store
	def __le__(self,other):
		return self<other or self==other
	def __ge__(self,other):
		return self<other or self==other
	def __ne__(self,other):
		return not (self==other)
	def __add__(self,other):
		if not isinstance(other,sortedlist):
			raise TypeError
		return sortedlist(self.__store+other.__store)
	def __mul__(self,n):
		return sortedlist(self.__store*n)
	def extend(self,it):
		for i in it:
			self.add(i)


class valueset(object):
	def __init__(self,it=[]):
		self.__content=sortedlist()
		for i in it:
			self.add(i)
	def __len__(self):
		return len(self.__content)
	def add(self,el):
		if el not in self.__content:
			self.__content.add(el)
	def __contains__(self,el):
		return el in self.__content
	def remove(self,el):
		if el in self:
			self.__content.remove(el)
		else:
			raise ValueError('%s not in valueset'%el)
	def __repr__(self):
		return 'valueset(%s)'%(self.__content)
	def __iter__(self):
		return iter(self.__content)
	def __eq__(self,other):
		if not isinstance(other,valueset):
			return False
		return self.__content==other.__content
	def __lt__(self,other):
		if not isinstance(other,valueset):
			return NotImplemented
		return self.__content<other.__content
	def __gt__(self,other):
		if not isinstance(other,valueset):
			return NotImplemented
		return self.__content>other.__content
	def __le__(self,other):
		return self<other or self==other
	def __ge__(self,other):
		return self>other or self==other
	def issubset(self,other):
		if not isinstance(other,valueset):
			return False
		def issub(self,other,start,end,startother,endother):
			if start==end:
				return True
			if endother-startother<end-start:
				return False
			if start+1==end:
				el=self.__content.get(start)
				low,high=startother,endother
				other=other.__content
				while low<high:
					mid=(low+high)/2
					if el==other.get(mid):
						return True
					if el<other.get(mid):
						high=mid
					else:
						low=mid+1
				return False
			midother=startother+endother
			midother/=2
			el=other.__content.get(midother)
			self_=self.__content
			low,high=start,end
			mid=0
			while low<high:
				mid=low+high
				mid/=2
				if self_.get(mid)==el:
					break
				if self_.get(mid)<el:
					low=mid+1
				else:
					if mid==start or self_.get(mid-1)<el:
						break
					high=mid
			if low==high==end:
				mid=end
			return issub(self,other,start,mid,startother,midother) and issub(self,other,mid,end,midother,endother)
		return issub(self,other,0,len(self),0,len(other))
	def __str__(self):
		return '{%s}'%', '.join([repr(i) for i in self])
	def __or__(self,other):
		if not isinstance(other,valueset):
			raise TypeError
		return valueset(sortedlist(self)+sortedlist(other))
	def __sub__(self,other):
		if not isinstance(other,valueset):
			raise TypeError
		v=valueset(self)
		for i in other:
			if i in self:
				v.remove(i)
		return v
	def __and__(self,other):
		if not isinstance(other,valueset):
			raise TypeError
		return self-(self-other)


def cartesian(*args):
	if not args:
		return valueset()
	if len(args)==1:
		if not isinstance(args[0],valueset):
			raise TypeError
		return valueset([(i,) for i in args[0]])
	c1=cartesian(*(args[:len(args)/2]))
	c2=cartesian(*(args[len(args)/2:]))
	ans=valueset()
	for i in c1:
		for j in c2:
			ans.add(i+j)
	return ans

def powerset(s):
	if not isinstance(s,valueset):
		raise TypeError
	if not s:
		return valueset([valueset()])
	if len(s)==1:
		ans=valueset([valueset()])
		for i in s:
			ans.add(valueset([i]))
		return ans
	l=sortedlist(s)
	s1=powerset(valueset(l.sublist(0,len(s)/2)))
	s2=powerset(valueset(l.sublist(len(s)/2)))
	ans=valueset()
	for i in s1:
		for j in s2:
			ans.add(i | j)
	return ans


class stringdict(object):
	def __init__(self,it=[]):
		self.__items={}
		self.__size=0
		for ty in [dict,stringdict]:
			if isinstance(it,ty):
				it=it.iteritems()
				break
		for i,j in it:
			self.add(i,j)
	def add(self,skey,value=None):
		if type(skey)!=str:
			raise TypeError
		items=self.__items
		for i in skey:
			if i not in items:
				items[i]={}
			items=items[i]
		if 'data' not in items:
			self.__size+=1
		items['data']=value
	def __contains__(self,skey):
		if type(skey)!=str:
			return False
		items=self.__items
		for i in skey:
			if i not in items:
				return False
			items=items[i]
		return 'data' in items
	def __recitemiter(self,items,s):
		if 'data' in items:
			yield s
		for i in items:
			if i!='data':
				for j in self.__recitemiter(items[i],s+i):
					yield j
	def __iter__(self):
		return self.__recitemiter(self.__items,'')
	def __len__(self):
		return self.__size
	def remove(self,skey):
		if type(skey)!=str:
			raise TypeError
		items=self.__items
		for i in skey:
			if i not in items:
				return
			items=items[i]
		if 'data' in items:
			del items['data']
			self.__size-=1
	def get(self,skey,defualt=None):
		if type(skey)!=str:
			raise TypeError
		items=self.__items
		for i in skey:
			if i not in items:
				return defualt
			items=items[i]
		return items.get('data',defualt)
	def iteritems(self):
		for i in self:
			yield (i,self.get(i))
	def items(self):
		return list(self.iteritems())
	def __nonzero__(self):
		return bool(len(self))
	def empty(self):
		self.__items={}
		self.__size=0
	def __eq__(self,other):
		if not isinstance(other,stringdict):
			return False
		if len(self)!=len(other):
			return False
		for (si,sj),(oi,oj) in zip(self.iteritems(),other.iteritems()):
			if si!=oi or sj!=oj:
				return False
		return True
	def todict(self):
		d={}
		for i,j in self.iteritems():
			d[i]=j
		return d
	def __repr__(self):
		return 'stringdict(%s)'%str(self.todict())
	def __lt__(self,other):
		if not isinstance(other,stringdict):
			return NotImplemented
		for (si,sj),(oi,oj) in zip(self.iteritems(),other.iteritems()):
			if si<oi:
				return True
			if si==oi and sj<oj:
				return True
			if si>oi:
				return False
			if si==oi and sj>oj:
				return False
		return len(self)<len(other)
	def __gt__(self,other):
		if not isinstance(other,stringdict):
			return NotImplemented
		return other<self
	def __ge__(self,other):
		return not self<other
	def __le__(self,other):
		return not self>other
	def hasprefix(self,p):
		if type(p)!=str:
			raise TypeError
		items=self.__items
		for i in p:
			if i not in items:
				return False
			items=items[i]
		return True
	def update(self,it,overwrite=True):
		for ty in [dict,stringdict]:
			if isinstance(it,ty):
				it=it.iteritems()
				break
		for i,j in it:
			if i in self and not overwrite:
				continue
			self.add(i,j)
	def findprefixitemsiter(self,p):
		if type(p)!=str:
			raise TypeError
		items=self.__items
		res=True
		for i in p:
			if i not in items:
				res=False
				break
			items=items[i]
		if res:
			for i in zip(self.__recitemiter(items,p)):
				yield (i,self.get(i))
	def findprefixiter(self,p):
		if type(p)!=str:
			raise TypeError
		items=self.__items
		res=True
		for i in p:
			if i not in items:
				res=False
				break
			items=items[i]
		if res:
			return self.__recitemiter(items,p)
		return iter(())
	def findprefix(self,p):
		return set(self.findprefixiter())
	def findprefixitems(self,p):
		return set(self.findprefixitemsiter())




