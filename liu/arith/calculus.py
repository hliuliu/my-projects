import math as _math
import vector as _vector


E=_math.e
PI=_math.pi
EPSILON=1E-12
inf=float('inf')

ROOT_PI=_math.sqrt(PI)
ROOT_2=_math.sqrt(2)


def sin(x):
	return _math.sin(x)

def cos(x):
	return _math.cos(x)

def tan(x):
	return sin(x)/cos(x)

def csc(x):
	return 1.0/sin(x)

def sec(x):
	return 1.0/cos(x)

def cot(x):
	return cos(x)/sin(x)

def sinh(x):
	return 0.5*(_math.pow(E,x)-_math.pow(E,-x))

def cosh(x):
	return 0.5*(_math.pow(E,x)+_math.pow(E,-x))

def tanh(x):
	return sinh(x)/cosh(x)

def csch(x):
	return 1.0/sinh(x)

def sech(x):
	return 1.0/cosh(x)

def coth(x):
	return cosh(x)/sinh(x)

def ln(x):
	return _math.log(x)

def log(x):
	return ln(x)/ln(10)

def lg(x):
	return ln(x)/ln(2)

def logbase(x,base):
	return ln(x)/ln(base)

def approx(a,b):
	return abs(a-b)<EPSILON

class polynomial(object):
	"""docstring for polynomial"""
	def __init__(self, poldict={}):
		self.__powexp={}
		for i in poldict:
			if type(i) is int and i>=0:
				if type(poldict[i]) not in [int,float,long]:
					print type(poldict[i])
					raise TypeError
				if poldict[i]:
					self.__powexp[i]=int(poldict[i]) if int(poldict[i])==poldict[i] else poldict[i]
	def getcoef(self,k):
		if k not in self.__powexp:
			return 0
		return self.__powexp[k]
	def getexps(self,coef):
		res=[]
		for i,j in self.__powexp.items():
			if j==coef:
				res+=[i]
		return res
	def degree(self):
		try:
			return sorted(self.__powexp.keys())[-1]
		except:
			return -1
	def evalat(self,x):
		ans=0
		for i,j in self.__powexp.items():
			ans+=j*x**i
		return int(ans) if int(ans)==ans else ans
	def __str__(self):
		if self.degree()<0:
			return '0'
		return '+'.join([('%#*x^%d'.replace('#','d' if type(j) is int else 'f'))%(j,i) for i,j in sorted(self.__powexp.items(),reverse=True)])\
			.replace('*x^0','').replace('+-','-')
	def __repr__(self):
		return str(self)
	def nonzeropows(self):
		return set(self.__powexp.keys())
	def __add__(self,other):
		if not isinstance(other,polynomial):
			other=polynomial({0:other})
		powslist=list(self.nonzeropows().union(other.nonzeropows()))
		return polynomial(dict([(i,self.getcoef(i)+other.getcoef(i)) for i in powslist]))
	def __sub__(self,other):
		if not isinstance(other,polynomial):
			other=polynomial({0:other})
		powslist=list(self.nonzeropows().union(other.nonzeropows()))
		return polynomial(dict([(i,self.getcoef(i)-other.getcoef(i)) for i in powslist]))
	def __neg__(self):
		return polynomial()-self
	def __mul__(self,other):
		if not isinstance(other,polynomial):
			other=polynomial({0:other})
		ans=polynomial()
		for i in self.nonzeropows():
			for j in other.nonzeropows():
				ans+=polynomial({i+j:self.getcoef(i)*other.getcoef(j)})
		return ans
	def __div__(self,other):
		if not isinstance(other,polynomial):
			other=polynomial({0:other})
		lc=other.leadingcoef()
		odeg=other.degree()
		if odeg<0:
			raise ZeroDivisionError
		ans,cur=polynomial(),self
		while cur.degree()>=odeg:
			term=polynomial({cur.degree()-odeg:float(cur.leadingcoef())/lc})
			ans+=term
			cur-=term*other
		return ans
	def leadingcoef(self):
		return self.getcoef(self.degree())
	def __mod__(self,other):
		if not isinstance(other,polynomial):
			other=polynomial({0:other})
		return self-self/other*other
	def constant(self):
		return self.getcoef(0)
	def __pow__(self,n):
		ans=polynomial({0:1})
		for i in range(n):
			ans*=self
		return ans
	def derivative(self):
		dx={}
		for i,j in self.__powexp.items():
			dx[i-1]=j*i
		return polynomial(dx)
	def todict(self):
		return dict(self.__powexp)
	def taylor(self,a,order):
		fact=1.0
		pol=self
		tyr=polynomial({0:pol.evalat(a)})
		for i in range(1,order+1):
			fact/=i
			pol=pol.derivative()
			tyr+=(polynomial({1:1,0:-a})**i)*(pol.evalat(a)*fact)
		return tyr
	def integral(self,cons=0):
		dx={0:cons}
		for i,j in self.__powexp.items():
			dx[i+1]=j/float(i+1)
		return polynomial(dx)
	def __eq__(self,other):
		if isinstance(other,offsetpolynomial):
			other=other.topolynomial()
		return (self-other).degree()<0
	def __ne__(self,other):
		return not self==other
	def exproffset(self,offset):
		shift=offsetpolynomial(-offset,self.todict())
		return offsetpolynomial(offset,shift.topolynomial().todict())
	def __nonzero__(self):
		return self.degree()>=0

def createpoly(*args):
	return pnomial(range(len(args)),args)

def constvalue(c):
	if type(c) not in [int,long,float]:
		raise TypeError
	return polynomial({0:c})

def pnomial(exps,coefs):
	return polynomial(dict(zip(exps,coefs)))

def unpack(pnom,zero=False):
	'''
	Purpose:
		returns a list of polynomials consisting of each term of pnom in accending order of exponents.
		if zero is set to True, the terms with exponent less than the leading degree and a coefficient of 0 will be included.
	Preconditions:
		pnom is an instance of polynomial
	Examples:
		unpack(2x^4+5x-3) => [-3,5x,2x^4]
		unpack(2x^4+5x-3,True) => [-3,5x,0,0,2x^4]
	'''
	res=[]
	if zero:
		for i in range(pnom.degree()+1):
			res+=[polynomial({i:pnom.getcoef(i)})]
	else:
		for i,j in sorted(pnom.todict().items()):
			res+=[polynomial({i:j})]
	return res

def unpackcoefs(pnom,zero=False):
	return [i.leadingcoef() for i in unpack(pnom,zero)]

def constvect(pnom):
	deg=pnom.degree()
	v=_vector.zeroes(deg+1)
	for i,j in pnom.todict().items():
		v.setcomp(i,j)
	return v

class offsetpolynomial(polynomial):
	"""docstring for offsetpolynomial"""
	def __init__(self, offset, poldict={}):
		if isinstance(poldict,polynomial):
			poldict=poldict.todict()
		super(offsetpolynomial, self).__init__(poldict)
		if type(offset) not in [int,float,long]:
			raise TypeError
		if offset==int(offset):
			offest=int(offset)
		self.__offset = offset
	def getcoef(self,k):
		return super(offsetpolynomial,self).getcoef(k)
	def getexps(self,coef):
		return super(offsetpolynomial,self).getexps(coef)
	def degree(self):
		return super(offsetpolynomial,self).degree()
	def evalat(self,x):
		return super(offsetpolynomial,self).evalat(x-self.__offset)
	def __str__(self):
		expr= super(offsetpolynomial,self).__str__()
		if self.__offset!=0:
			return expr.replace('x','(x#ofs)'.replace('#ofs',('+'+str(-self.__offset) if self.__offset<0 else '-'+str(self.__offset))))
		return expr
	def __repr__(self):
		return str(self)
	def topolynomial(self):
		ans=polynomial()
		for i,j in super(offsetpolynomial,self).todict().items():
			ans+=polynomial({1:0,0:-self.__offset})**i*j
		return ans
	def getoffset(self):
		return self.__offset
	def setoffset(self,offset):
		if type(offset) not in [int,float,long]:
			raise TypeError
		if offset==int(offset):
			offest=int(offset)
		self.__offset = offset
	def derivative(self):
		return offsetpolynomial(self.__offset,super(offsetpolynomial,self).derivative())
	def integral(self,cons=0):
		return offsetpolynomial(self.__offset,super(offsetpolynomial,self).integral(cons))
	def __eq__(self,other):
		if isinstance(other,offsetpolynomial):
			other=other.topolynomial()
		if not isinstance(other,polynomial):
			other=polynomial({0:other})
		return self.topolynomial()==other
	def __add__(self,other):
		return self.topolynomial()+other.topolynomial()
	def __ne__(self,other):
		return not self==other
	def __neg__(self,other):
		sup=super(offsetpolynomial,self)
		return offsetpolynomial(-sup,self.__offset)
	def __mul__(self,other):
		if isinstance(other,offsetpolynomial):
			other=other.topolynomial()
		if not isinstance(other,polynomial):
			other=polynomial({0:other})
		return self.topolynomial()*other
	def __div__(self,other):
		if isinstance(other,offsetpolynomial):
			other=other.topolynomial()
		if not isinstance(other,polynomial):
			other=polynomial({0:other})
		return self.topolynomial()/other
	def __mod__(self,other):
		return self-(self/other)*other
	def taylor(self,a,order):
		return offsetpolynomial(super(offsetpolynomial,self).taylor(a-offset,order),self.__offset)

class complex(object):
	def __new__(cls,real=0,im=0):
		tps=[int,float,long]
		if True in [type(real) not in tps ,type(im) not in tps]:
			raise TypeError
		if approx(int(round(real)),real):
			real=int(round(real))
		if approx(int(round(im)),im):
			im=int(round(im))
		ob=super(complex,cls).__new__(cls)
		ob.__real,ob.__im=real,im
		return ob

	def __str__(self):
		if not self.__im:
			return str(self.__real)
		if not self.__real:
			return str(self.__im)+'i'
		return (str(self.__real)+'+'+str(self.__im)+'i').replace('+-','-')
	def __repr__(self):
		return str(self)
	def norm(self):
		return _math.sqrt(self.__real**2+self.__im**2)
	def isreal(self):
		return self.__im==0
	def arg(self):
		if self.norm()==0:
			raise ZeroDivisionError
		if self.isreal():
			if self.__real>0:
				return 0
			return PI
		
		if self.__real==0:
			if self.__im>0:
				return PI/2.0
			return PI/2.0*3
		ans=_math.atan(float(self.__im/self.__real))
		if self.__real>0:
			if self.__im>0:
				return ans
			return ans+2*PI
		return ans+PI
	def realcomp(self):
		return self.__real
	def imcomp(self):
		return self.__im
	def __add__(self,other):
		if not isinstance(other,complex):
			other=complex(other,0)
		return complex(self.realcomp()+other.realcomp(),self.imcomp()+other.imcomp())
	def __sub__(self,other):
		if not isinstance(other,complex):
			other=complex(other,0)
		return complex(self.realcomp()-other.realcomp(),self.imcomp()-other.imcomp())
	def __neg__(self):
		return complex()-self
	def conjugate(self):
		return complex(self.realcomp(),-self.imcomp())
	def __mul__(self,other):
		if not isinstance(other,complex):
			other=complex(other,0)
		return complex(self.realcomp()*other.realcomp()-self.imcomp()*other.imcomp(),self.realcomp()*other.imcomp()+other.realcomp()*self.imcomp())
	def __div__(self,other):
		if not isinstance(other,complex):
			other=complex(other,0)
		return self*other.conjugate()*(1.0/other.norm()**2)
	def __pow__(self,exp):
		ans=complex(1)
		for i in range(exp):
			ans*=self
		return ans
	def inverse(self):
		return complex(1)/self
	def __eq__(self,other):
		if not isinstance(other,complex):
			other=complex(other,0)
		return self.realcomp()==other.realcomp() and self.imcomp()==other.realcomp()


def polar(r,theta):
	return complex(r*cos(theta),r*sin(theta))

def components(cmpnum):
	return cmpnum.realcomp(),cmpnum.imcomp()

def getvector(cmpnum):
	from vector import vector
	return vector(*components(cmpnum))

class interval(object):
	def __init__(self,numleft,lend,numright,rend):
		ends=[]
		for i in (numleft,numright):
			if type(i) not in [int,float,long]:
				raise TypeError
			if approx(i,round(i,5)):
				ends.append(round(i,5))
			else:
				ends.append(i)
			if approx(ends[-1],int(ends[-1])):
				ends[-1]=int(ends[-1])
		a,b=ends
		if a>b or (a==b and False in [bool(lend),bool(rend)]):
			self.__empty=True
			return
		if a==inf or b==-inf:
			self.__empty=True
			return
		self.__empty=False
		self.__numleft=a
		self.__numright=b
		self.__lend=bool(lend)
		self.__rend=bool(rend)
		if a==-inf:
			self.__lend=False
		if b==inf:
			self.__rend=False
	def __repr__(self):
		if self.__empty:
			return 'interval(0,True,0,False)'
		return 'interval(%s,%s,%s,%s)'%(self.__numleft,self.__lend,self.__numright,self.__rend)
	def __str__(self):
		if self.__empty:
			return '(null)'
		if self.infimum()==self.supremum():
			return str(self.supremum())
		s=''
		if self.__lend:
			s+='[ '
		else:
			s+='( '
		s+=str(self.__numleft)+' , '
		s+=str(self.__numright)
		if self.__rend:
			s+=' ]'
		else:
			s+=' )'
		
		return s
	def supremum(self):
		if self.__empty:
			return -inf
		return self.__numright
	def infimum(self):
		if self.__empty:
			return inf
		return self.__numleft
	def __contains__(self,ans):
		if isinstance(ans,interval):
			if ans.__empty:
				return True
			if self.__empty:
				return False
			if ans.infimum()<self.infimum():
				return False
			if ans.supremum()>self.supremum():
				return False
			if self.isclosed() or ans.isopen():
				return True
			if ans.infimum()>self.infimum() and ans.supremum()<self.supremum():
				return True
			if ans.infimum()==self.infimum():
				if self.isleftopen() and not ans.isleftopen():
					return False
			if ans.supremum()==self.supremum():
				if self.isrightopen() and not ans.isrightopen():
					return False
			return True
		if type(ans) not in [int,float,long]:
			return False
		if self.__empty:
			return False
		if self.infimum()<ans<self.supremum():
			return True
		if self.infimum()==ans:
			return self.__lend
		if self.supremum()==ans:
			return self.__rend
		return False
	def restrictfn(self,f):
		def frestrict(x):
			if x in self:
				return f(x)
			else:
				raise ValueError('input is not in the interval %s'%str(self))
		return frestrict
	def __eq__(self,other):
		if not isinstance(other,interval):
			return False
		return (self in other) and (other in self)
	def isopen(self):
		return not self.__lend and not self.__rend
	def isclosed(self):
		return self.__lend and self.__rend
	def isleftopen(self):
		return not self.__lend
	def isrightopen(self):
		return not self.__rend
	def ishalfopen(self):
		return not self.isopen() and not self.isclosed()
	def size(self):
		if self.__empty:
			return 0
		dif=self.supremum()-self.infimum()
		if dif==int(dif):
			return int(dif)
		return dif
	def closure(self):
		if self.__empty:
			return self
		return interval(self.infimum(),True,self.supremum(),True)
	def shift(self,dx):
		if type(dx) not in [int,float,long]:
			raise TypeError
		if self.__empty:
			return self
		return interval(self.infimum()+dx, not self.isleftopen(),self.supremum()+dx,not self.isrightopen())
	def scale(self,factor):
		if type(factor) not in [int,float,long]:
			raise TypeError
		if self.__empty:
			return self
		return interval(self.infimum()*factor,not self.isleftopen(),self.supremum()*factor,not self.isrightopen())
	def split(self,val=0):
		if self.__empty:
			raise ValueError
		return (interval(self.infimum(), not self.isleftopen(),val,False),
			singleint(val),interval(val,False,self.supremum(),not self.isrightopen()))
	def __nonzero__(self):
		return not self.__empty
	def __and__(self,other):
		if not isinstance(other,interval):
			raise TypeError
		if False in [bool(self),bool(other)]:
			return interval(0,True,0,False)
		lower=max(self.infimum(),other.infimum())
		upper=min(self.supremum(),other.supremum())
		lend=lower in self and lower in other
		uend=upper in self and upper in other
		return interval(lower,lend,upper,uend)


def erfinv(x):
	'''
	Purpose:
		returns the result of the inverse error function evaluated at x.
		this value is a real number y such that erf(y)=x.
		the return value is inf if x=1 and -inf if x=-1
		For more information, see the erf function in the math library.
	Preconditions:
		type(x) is int, long, or float
		-1<=x<=1
	'''
	if type(x) not in [int,float,long]:
		raise TypeError
	if not -1<=x<=1:
		raise ValueError
	if abs(x)==1:
		return x*inf
	cks=[1.0]
	powerterm=ROOT_PI/2.0*x
	ans=0.0
	for k in xrange(250):
		ck=0.0
		if not k:
			ck=1.0
		else:
			for m in xrange(k):
				ck+=cks[m]*cks[k-1-m]/(m+1)/(2*m+1)
			cks.append(ck)
		ans+=ck/(2*k+1)*powerterm
		powerterm*=PI/4.0*(x**2)
	return ans

__all__=['erfinv','interval']



if __name__=='__main__':
	print createpoly(1,4,2)**3


