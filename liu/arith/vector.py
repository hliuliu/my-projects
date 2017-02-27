

class vector(object):
	def __init__(self,*args):
		for i in args:
			if type(i) not in [int,float,long]:
				raise TypeError
		from calculus import approx
		args=(int(round(a)) if approx(a,int(round(a))) else a for a in args)
		self.__comps=list(args)
	def dimensions(self):
		return len(self.__comps)
	def tolist(self):
		return list(self.__comps)
	def length(self):
		import math
		ans=0
		for i in self.__comps:
			ans+=i**2
		ans=math.sqrt(ans)
		if ans==int(ans):
			ans=int(ans)
		return ans
	def totuple(self):
		return tuple(self.__comps)
	def __str__(self):
		return str(self.totuple())
	def get(self,pos):
		return self.__comps[pos]
	def setcomp(self,pos,val):
		if type(pos) not in [int,float]:
			raise TypeError
		if val==int(val):
			val=int(val)
		self.__comps[pos]=val
	def subvector(self,start=0,stop=None,step=1):
		if stop == None:
			stop=self.dimensions()
		return vector(*self.tolist()[start:stop:step])
	def __repr__(self):
		return str(self)
	def __add__(self,other):
		if not isinstance(other,vector):
			raise TypeError
		if self.dimensions()!=other.dimensions():
			raise ValueError('cannot add vectors of diffrent number of components')
		return vector(*[i+j for i,j in zip(self.tolist(),other.tolist())])
	def __sub__(self,other):
		if not isinstance(other,vector):
			raise TypeError
		if self.dimensions()!=other.dimensions():
			raise ValueError('cannot subtract vectors of diffrent number of components')
		return vector(*[i-j for i,j in zip(self.tolist(),other.tolist())])
	def __mul__(self,c):
		if type(c) not in [int,float,long]:
			raise TypeError
		return vector(*[i*c for i in self.tolist()])
	def __eq__(self,other):
		if not isinstance(other,vector):
			return False
		if self.dimensions()!=other.dimensions():
			return False
		for i,j in zip(self.tolist(),other.tolist()):
			if i!=j:
				return False
		return True
	def __ne__(self,other):
		return not self==other
	def __neg__(self):
		return vector(*[-i for i in self.tolist()])


def zeroes(size):
	return vector(*([0]*size))

def ones(size):
	return vector(*([1]*size))

def add(*args):
	for i in args:
		if not isinstance(i,vector):
			raise TypeError
	res=[]
	for i in zip(*[a.tolist() for a in args]):
		x=0
		for j in i:
			x+=j
		res+=[x]
	return vector(*res)

def mult(v,scale):
	if not isinstance(v,vector) or type(scale) not in [int,float,long]:
		raise TypeError
	return vector(*[i*scale for i in v.tolist()])

def compmult(*args):
	if not args:
		raise ValueError
	if len(args)==1:
		if not isinstance(args[0],vector):
			raise TypeError
		return args[0]+zeroes(args[0].dimensions())
	a1=compmult(*args[:len(args)/2])
	a2=compmult(*args[len(args)/2:])
	if a1.dimensions()!=a2.dimensions():
		raise ValueError
	return vector(*[i*j for i,j in zip(a1.tolist(),a2.tolist())])

def dot(v1,v2):
	if not isinstance(v1,vector) or not isinstance(v2,vector):
		raise TypeError
	ans=0
	for i,j in zip(v1.tolist(),v2.tolist()):
		ans+=i*j
	if ans==int(ans):
		ans=int(ans)
	return ans

def concat(*args):
	a=[]
	for i in args:
		if not isinstance(i,vector):
			raise TypeError
		a+=i.tolist()
	return vector(*a)

def subtract(v1,v2):
	return add(v1,mult(v2,-1))

def cross(v1,v2):
	if not isinstance(v1,vector) or not isinstance(v2,vector) or v1.dimensions()!=3 or v2.dimensions()!=3:
		raise TypeError
	x1,y1,z1,x2,y2,z2=v1.tolist()+v2.tolist()
	x=y1*z2-y2*z1
	y=z1*x2-x1*z2
	z=x1*y2-x2*y1
	return vector(x,y,z)

def bases(size):
	b=[zeroes(size) for i in range(size)]
	for i,j in enumerate(b):
		j.setcomp(i,1)
	return b

def basis(size,pos):
	return bases(size)[pos]

def unit(v):
	return mult(v,1.0/v.length())

def projonto(u,v):
	return mult(v,float(dot(u,v))/v.length()**2)

def perponto(u,v):
	return subtract(u,projonto(u,v))

def orthogonal(*args):
	from calculus import approx
	for a in args:
		if not isinstance(a,vector):
			raise TypeError
	if len(args) in [0,1]:
		return True
	if not orthogonal(*(args[:-1])):
		return False
	lastvec=args[-1]
	args=args[:-1]
	return False not in [approx(dot(i,lastvec),0) for i in args]

def granschmidt(*args):
	args=list(args)
	for i,a in enumerate(args):
		for j in args[:i]:
			args[i]=perponto(a,j)
			a=args[i]
	return args

def normalize(*args):
	res=[]
	for a in args:
		res+=[unit(a)]
	return res

def prob(size,*args):
	from calculus import approx
	p=zeroes(size)
	init=1.0
	for i,a in enumerate(args):
		if type(a) not in [int,float]:
			raise TypeError
		if not 0<=a<=init:
			raise ValueError
		p.setcomp(i,a)
		init-=a
	if approx(init,round(init,4)):
		init=round(init,4)
	if init and len(args)==size:
		raise ValueError
	for i in range(len(args),size):
		p.setcomp(i,init/(size-len(args)))
	return p

