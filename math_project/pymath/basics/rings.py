'''
rings Module:

contains the basic numerical datatypes such as integer, 
	real, and rational.

These datatypes are considered rings and fields, so their lattices
	appropriately inherit the ring or field classes.



'''



import sys,os
from sys import maxint as _maxint
sys.path.append(os.path.join(os.path.split(__file__)[0],os.pardir,os.pardir))
from pymath.basics import py_to_math as _pytm, math_to_py as _mtop, is_math_type as _imt



class ring(object):
	'''
	ring class

	used for creating an instance for a specific ring.
	Ex. integers
	The parameter eltype, is the class used to create an instance
		of an element of the created ring. 
	Hence eltype must be None, if no such class exists, 
	or a subclass of ring_element.
	'''
	def __new__(cls,name='ring',label='',eltype=None):
		obj=super(ring,cls).__new__(cls)
		obj.__name=name
		obj.__label=label
		if eltype!=None and not issubclass(eltype,ring_element):
			raise TypeError('%s is not None and does not inherit ring_element'%eltype)
		obj.__eltype=eltype
		return obj
	def label(self):
		'''
		returns the label of the ring.
		'''
		return self.__label
	def __str__(self):
		'''
		returns the name of the ring.
		'''
		return self.__name
	def __contains__(self,el):
		'''
		returns whether or not  el in self.
		el in self <==> 
			el can be converted to an equivalent value of type 
			self.element_type() 
		'''
		el=_pytm(el)
		if type(el)==self.element_type():
			return True
		elconvert=self.element_type()(el)
		return elconvert==el
	def element_type(self):
		'''
		return the element type associated with self.
		'''
		return self.__eltype


class field(ring):
	'''
	field class

	used for creating an instance for a specific field.
	Ex. rationals
	Note that a field is a ring, so field is a subclass of ring.
	The parameter eltype, is the class used to create an instance
		of an element of the created field. 
	Hence eltype must be None, if no such class exists, 
	or a subclass of field_element.
	'''
	def __new__(cls,name='field',label='',eltype=None):
		if eltype!=None and not issubclass(eltype,field_element):
			raise TypeError('%s is not None and does not inherit field_element'%eltype)
		obj=super(field,cls).__new__(cls,name,label,eltype)
		return obj



class LatticeError(Exception):
	pass



class ring_element(object):
	'''
	ring_element class

	For creating a ring element with a given 
		value, typically represented as a string;
		and lattice, which must be an instance of a ring.


	'''
	def __new__(cls,value,lattice):
		obj=super(ring_element,cls).__new__(cls)
		obj.__value=value
		if not isinstance(lattice,ring):
			raise LatticeError('The lattice must be a ring')
		obj.__lattice=lattice
		return obj
	def lattice(self):
		'''
		returns the lattice of the ring_element.
		'''
		return self.__lattice
	def value(self):
		'''
		returns the value of the ring_element.
		'''
		return self.__value
	def __str__(self):
		'''
		returns the value of the ring_element as a string.
		'''
		return str(self.value())



class field_element(ring_element):
	'''
	field_element class

	For creating a field element with a given 
		value, typically represented as a string;
		and lattice, which must be an instance of a field.


	'''
	def __new__(cls,value,lattice):
		obj=super(field_element,cls).__new__(cls,value,lattice)
		if not isinstance(lattice,field):
			raise LatticeError('The lattice must be a field')
		return obj



class integer(ring_element):
	'''
	integer class

	A class to store the integer datatype.
	the __new__ method creates the integer taking a parameter num,
		where either num has the '__integer__' attriblute or
		str(num) must be a vaild literal representing an integer.

	There is no limit to how large or small the integer, provided
		that there is enough memory to store its string representation.

	'''
	def __new__(cls,num):
		if hasattr(num,'__integer__'):
			return num.__integer__()
		num=str(num)
		num=''.join(num.split())
		numabs=num
		if num and num[0] in ['+','-']:
			numabs=num[1:]
		if not numabs:
			raise TypeError('Invaild literal for an integer: %s'%num)
		for c in numabs:
			if not '0'<=c<='9':
				raise TypeError('Invaild literal for an integer: %s'%num)
		index=0
		while index<len(numabs)-1 and numabs[index]=='0':
			index+=1
		numabs=numabs[index:]
		if numabs=='0':
			num='0'
		else:
			num=('-' if num[0]=='-' else '')+numabs
		obj=super(integer,cls).__new__(cls,num,integers)
		obj.__prods=None
		return obj
	def is_zero(self):
		'''
		Purpose:
			Determine whether or not self is zero.
			returns True if so, False if not.
		Preconditions:
			none
		'''
		return str(self)=='0'
	def is_positive(self):
		'''
		Purpose:
			Determine whether or not self is positive.
			returns True if so, False if not.
		Preconditions:
			none
		'''
		return not (self.is_zero() or self.is_negative())
	def is_negative(self):
		'''
		Purpose:
			Determine whether or not self is negative.
			returns True if so, False if not.
		Preconditions:
			none
		'''
		return str(self)[0]=='-'
	def __neg__(self):
		'''
		Purpose:
			Computes -self. That is, self*(-1), where -1
				denotes the additive inverse of 1
		Preconditions:
			none
		'''
		v=str(self)
		if v.startswith('-'):
			v=v[1:]
		else:
			v='-'+v
		return integer(v)
	def __eq__(self,other):
		'''
		self.__eq__(other) <==> self==other

		Purpose:
			compare self with other
			returns True if self , other both 
				correspond to the same integer. 
				In such a case, type(other) must be either a pymath
				datatype or one of [int,long,float]
			returns false otherwise.
		Preconditions:
			none

		'''
		other=_pytm(other)
		if _imt(other):
			if isinstance(other,integer):
				return str(self)==str(other)
			if isinstance(other,rational):
				return other==self
		return False
	def __ne__(self,other):
		'''
		returns True iff self.__eq__(other) returns False
		'''
		return not self==other
	def __gt__(self,other):
		other=_pytm(other)
		if _imt(other):
			if isinstance(other,integer):
				if self.is_negative():
					if not other.is_negative():
						return False
					return -other>-self
				if self.is_zero():
					return other.is_negative()
				if not other.is_positive():
					return True
				self,other=map(str,[self,other])
				ls,lo=map(len,[self,other])
				if ls!=lo:
					return ls>lo
				self=reversed(str(self))
				other=reversed(str(other))
				status=0
				for i,j in zip(self,other):
					if i>j:
						status=1
					if i<j:
						status=-1
				return status>0
			return other<self
		return NotImplemented
	def __ge__(self,other):
		return self==other or self>other
	def __lt__(self,other):
		other=_pytm(other)
		if _imt(other):
			if isinstance(other,integer):
				return not self>=other
			return other>self
		return NotImplemented
	def __le__(self,other):
		return self<other or self==other
	def __add__(self,other):
		other=_pytm(other)
		if _imt(other):
			if not isinstance(other,integer):
				return other+self
			if self.is_negative():
				return -((-self)+(-other))
			if other.is_negative():
				return self-(-other)
			sself=str(self)
			sother=str(other)
			sl,ol=map(len,[sself,sother])
			m,M=[f(sl,ol) for f in [min,max] ]
			sself='0'*(M-sl)+sself
			sother='0'*(M-ol)+sother
			sd=reversed(sself)
			od=reversed(sother)
			carry=0
			digstr=''
			for i,j in zip(sd,od):
				d=int(i)+int(j)+carry
				carry=d/10
				d%=10
				digstr=str(d)+digstr
			if carry==1:
				digstr='1'+digstr
			return integer(digstr)
		return TypeError('Cannot add integer to %s.'%(type(other).__name__))
	def __abs__(self):
		if self.is_negative():
			return -self
		return self
	def __sub__(self,other):
		other=_pytm(other)
		if _imt(other):
			if not isinstance(other,integer):
				return -(other-self)
			if other.is_negative():
				return self+(-other)
			if self<other:
				return -(other-self)
			sself=str(self)
			sother=str(other)
			sother='0'*(len(sself)-len(sother))+sother
			digstr=''
			borrow=0
			sd=reversed(sself)
			od=reversed(sother)
			for i,j in zip(sd,od):
				d=int(i)-int(j)-borrow
				if d<0:
					borrow=1
					d+=10
				else:
					borrow=0
				digstr=str(d)+digstr
			return integer(digstr)
		return TypeError('Cannot subtract integer to %s.'%(type(other).__name__))
	def __nonzero__(self):
		return str(self)!='0'
	def __mul__(self,other):
		other=_pytm(other)
		if _imt(other):
			if not isinstance(other,integer):
				return other*self
			if map(lambda x: x.is_negative(),[self,other]).count(True)==1:
				return -(abs(self)*abs(other))
			self,other=map(abs,[self,other])
			other,self=sorted([self,other],key=lambda x: len(str(x)))
			od=reversed(str(other))
			zeroes=''
			ans=integer('0')
			if self.__prods==None:
				prods=[integer('0')]
				for i in xrange(1,10):
					prods.append(prods[-1]+self)
				self.__prods=prods
			prods=self.__prods
			for i in od:
				times=int(i)
				dm=prods[times]
				dm=str(dm)+zeroes
				ans+=integer(dm)
				zeroes+='0'
			return ans
		raise TypeError('Cannot multply integer to %s.'%(type(other).__name__))
	def __floordiv__(self,other):
		other=_pytm(other)
		if isinstance(other,integer):
			if not other:
				raise ZeroDivisionError
			if not self:
				return integer('0')
			if other.is_negative():
				self,other=-self,-other
			if self.is_negative():
				return -((-self-1)//other)-1
			sself=str(self)
			sother=str(other)
			digs=[0]*max(len(sself)-len(sother)+1,1)
			if other.__prods==None:
				prods=[integer('0')]
				for i in xrange(1,10):
					prods.append(prods[-1]+other)
				other.__prods=prods
			prods=other.__prods
			while len(sself)>=len(sother) and \
			  not (len(sself)==len(sother) and integer(sself)<other):
			  	portion=sself[:len(sother)]
			  	if integer(portion)<other:
			  		portion+=sself[len(sother)]
			  	#print 'portion',portion
			  	pos=len(sself)-len(portion)
			  	iportion=integer(portion)
			  	i=9
			  	while prods[i]>iportion:
			  		i-=1
			  	digs[pos]=i
			  	rem=iportion-prods[i]
			  	rem='' if not rem else str(rem)
			  	sself=rem+sself[len(portion):]
			digstr=''.join(map(str,reversed(digs)))
			return integer(digstr)
		if isinstance(other,rational):
			return (self/other).floor()
		raise TypeError('Cannot use floor division with integer over %s'%(type(other).__name__))
		
	def __mod__(self,other):
		other=_pytm(other)
		if not isinstance(other,integer):
			raise TypeError('Cannot mod with integer over %s'%(type(other).__name__))
		if not other:
			raise ZeroDivisionError
		return self-(self//other*other)
	def __pow__(self,other):
		other=_pytm(other)
		if _imt(other):
			if not isinstance(other,integer):
				raise NotImplementedError
			if other.is_negative():
				return rational(1,self**(-other))
			return self.__recpow(other)
		raise TypeError('Cannot take rational to the power of %s'
			%type(other).__name__)
	def __recpow(self,other):
		if not other:
			return integer('1')
		selfsq=self*self
		return selfsq.__recpow(other//2)* \
			(self if other%integer('2') else integer('1'))
	def __hash__(self):
		return int(self%(integer(_maxint)+1))
	def __repr__(self):
		return str(self)
	def __integer__(self):
		return self
	def __rational__(self):
		return rational(self)
	def __int__(self):
		return int(str(self))
	def __float__(self):
		return float(str(self))
	def __div__(self,other):
		other=_pytm(other)
		if _imt(other):
			if isinstance(other,integer) or isinstance(other,rational):
				q=rational(self,other)
				if q==integer(q):
					return integer(q)
				return q
			raise NotImplementedError
		raise TypeError(
			'Cannot use division with integer over %s'
			%type(other).__name__)
	def reciprocal(self):
		if self in [1,-1]:
			return self
		return rational(1,self)




integers=ring('integers','Z',integer)



def _gcd(a,b):
	a=abs(a)
	b=abs(b)
	while b:
		r=a%b
		a,b=b,r
	return a

def _str_to_rational(s):
	if '/' not in s:
		try:
			return integer(s)
		except:
			raise TypeError('Invalid literal for a rational: %s'%s)
	num,_,dem=s.partition('/')
	try:
		num,dem=map(integer,[num,dem])
		return rational(num,dem)
	except TypeError:
		raise TypeError('Invalid literal for a rational: %s'%s)

def _conv_rat_type(r):
	if r==integer(r):
		return integer(r)
	return r



class rational(field_element):
	'''
	rational class

	A class to store the rational datatype.
	The __new__ method creates the rational number by taking 
		2 parameters num and dem.
		the num parameter is required.
		the dem parameter is optional and defaults to 1
	num and dem must each be at least one of the following:
		- A string that is a valid literal representing a rational number
		- A value that on input to the py_to_math function, returns a value
			of which has the __rational__ attribute. An integer satisfies
			this condition
	A valid literal is either one that represents an integer, or has 
		the form x+'/'+y where x,y are vaild literals each representing 
		an integer, with y nonzero.
	Returns a rational number that is the result of num/dem.
	The numerator and denominator are reduced to the lowest form, and
		the denominator is set to be positive always.
	'''
	def __new__(cls,num,dem=integer('1')):
		if type(num)==str:
			num=_str_to_rational(num)
		if type(dem)==str:
			dem=_str_to_rational(dem)
		num,dem=map(_pytm,[num,dem])
		if not dem:
			raise ZeroDivisionError
		if type(num)==integer and type(dem)==integer:
			d=_gcd(num,dem)
			num,dem=num//d,dem//d
			if dem.is_negative():
				num,dem=-num,-dem
			if not num:
				dem=integer('1')
		elif hasattr(num,'__rational__') and hasattr(dem,'__rational__'):
			return num.__rational__()/dem.__rational__()
		else:
			raise TypeError('Invaild type(s) %s/%s'%(type(num).__name__, 
				type(dem).__name__))
		obj=super(rational,cls).__new__(cls,
			str(num)+('/'+str(dem) if dem!=1 else ''),rationals)
		obj.__num=num
		obj.__dem=dem
		return obj
	def __rational__(self):
		'''
		self.__rational__() <==> rational(self)

		Purpose:
			returns the rational number, self.
		Preconditions:
			none
		'''
		return self
	def __integer__(self):
		'''
		self.__integer__() <==> integer(self)

		Purpose:
			returns the integer representation of the 
				rational number, self.
			the returned integer is equivalent to the decimal expansion
				of self, but with all digits after the decimal point
				truncated.
		Preconditions:
			none
		Examples:
			integer(rational(0)) ==> 0
			integer(rational(15)) ==> 15
			integer(rational(1,2)) ==> 0
			integer(rational(17,4)) ==> 4
			integer(rational(-1,2)) ==> 0
			integer(rational(-17,4)) ==> -4
		'''
		selfabs=abs(self)
		ans=selfabs.floor()
		if self.numerator()<0:
			return -ans
		return ans
	def numerator(self):
		'''
		returns the numerator of self.
		'''
		return self.__num
	def denominator(self):
		'''
		returns the denominator of self.
		'''
		return self.__dem
	def num_dem_pair(self):
		'''
		returns the (numerator,denominator) pair of self as a tuple.
		'''
		return self.numerator(),self.denominator()
	def __float__(self):
		return float(self.__num)/float(self.__dem)
	def __add__(self,other):
		other=_pytm(other)
		if _imt(other):
			if isinstance(other,integer):
				other=rational(other)
			if isinstance(other,rational):
				return _conv_rat_type(rational(
					self.numerator()*other.denominator()+
					self.denominator()*other.numerator(),
					self.denominator()*other.denominator()
					))
			return other+self
		raise TypeError('Cannot add rational to %s'
			%type(other).__name__)
	def __eq__(self,other):
		other=_pytm(other)
		if _imt(other):
			if isinstance(other,integer):
				other=rational(other)
			if isinstance(other,rational):
				return self.numerator()==other.numerator() and \
					self.denominator()==other.denominator()
			return other==self
		return False
	def __gt__(self,other):
		other=_pytm(other)
		if _imt(other):
			if isinstance(other,integer):
				other=rational(other)
			if isinstance(other,rational):
				return self.numerator()*other.denominator() \
					> self.denominator()*other.numerator()
			return other<self
		return NotImplemented
	def __neg__(self):
		return rational(-self.numerator(),self.denominator())
	def __lt__(self,other):
		other=_pytm(other)
		if _imt(other):
			if isinstance(other,integer):
				other=rational(other)
			return other>self
		return NotImplemented
	def __ge__(self,other):
		return self>other or self==other
	def __le__(self,other):
		return self<other or self==other
	def __sub__(self,other):
		try:
			return self+(-other)
		except TypeError:
			raise TypeError('Cannot subtract rational to %s'
				%(type(other).__name__))
	def __mul__(self,other):
		other=_pytm(other)
		if _imt(other):
			if isinstance(other,integer):
				other=rational(other)
			if isinstance(other,rational):
				if other==1:
					return self
				return _conv_rat_type(
					rational(self.numerator()*other.numerator(),
					self.denominator()*other.denominator())
					)
			return other*self
		raise TypeError('Cannot multply rational by %s'
			%(type(other).__name__))
	def reciprocal(self):
		'''
		Purpose:
			returns the reciprocal of the rational number, self.
				that is, 1/self.
		Preconditions:
			self is nonzero
		'''
		if not self:
			raise ZeroDivisionError
		return rational(self.denominator(),self.numerator())
	def __div__(self,other):
		other=_pytm(other)
		if _imt(other):
			if isinstance(other,integer):
				other=rational(other)
			if isinstance(other,rational):
				return self*other.reciprocal()
			raise NotImplementedError
		raise TypeError('Cannot divide rational by %s'
			%(type(other).__name__))
	def floor(self):
		'''
		Purpose:
			returns the floor of the rational number self, which is an 
			integer, precisely the largest integer n such that n<=self.
		Preconditions:
			none
		'''
		return self.__num//self.__dem
	def ceiling(self):
		'''
		Purpose:
			returns the ceiling of the rational number self, which is an 
			integer, precisely the smallest integer n such that n>=self.
		Preconditions:
			none
		'''
		return -((-self).floor())
	def __nonzero__(self):
		return bool(self.__num)
	def __abs__(self):
		return rational(abs(self.numerator()),self.denominator())
	def __floordiv__(self,other):
		other=_pytm(other)
		if _imt(other):
			if isinstance(other,integer):
				other=rational(other)
			if isinstance(other,rational):
				ans=self/other
				if isinstance(ans,rational):
					return ans.floor()
				return ans
		raise TypeError('Cannot use floor division with rational over %s'
			%type(other).__name__)
	def __mod__(self,other):
		try:
			return self-(self//other)*other
		except TypeError:
			raise TypeError('Cannot use modulo with rational over %s'
				%type(other).__name__)
	def __pow__(self,other):
		try:
			return _conv_rat_type(
						rational(self.numerator()**other,
							self.denominator()**other))
		except NotImplementedError:
			raise NotImplementedError
		except TypeError:
			raise TypeError('Cannot take rational to the power of %s'
				%type(other).__name__)
	def mixed_number_decomp(self):
		'''
		Purpose:
			returns a mixed number decomposition of self, a tuple 
				containing 2 elements, an integer, followed by
				a rational.
			if self has (a+b/c) as a mixed number representation,
				that is, a,b,c are integers, c nonzero, and
				0<=abs(b/c)<1, then self.mixed_number_decomp()
				returns (a,b/c)
		Preconditions:
			none
		Examples:
			rational(0).mixed_number_decomp() ==> (0,0)
			rational(3,5).mixed_number_decomp() ==> (0,3/5)
			rational(17,8).mixed_number_decomp() ==> (2,1/8)
			rational(-3,5).mixed_number_decomp() ==> (0,-3/5)
			rational(-17,8).mixed_number_decomp() ==> (-2,-1/8)
		'''
		iself=integer(self)
		rem=self-iself
		return iself,rem
	def is_positive(self):
		return self>0
	def is_negative(self):
		return self<0
	def is_zero(self):
		return self==0




rationals=field('rationals','Q',rational)




class real(field_element):
	def __new__(cls,num):
		if type(num)==float:
			num=str(num)
		num=_pytm(num)
		if hasattr(num,'__real__'):
			return num.__real__()
		if type(num)==str:
			bfdec,_,afdec=num.partition('.')
			if not afdec:
				afdec='0'
			try:
				bfdecn,afdecn=map(integer,[bfdec,afdec])
			except TypeError:
				raise TypeError('Invaild literal for a real %s'%(num))
				afdec=list(afdec)
			while len(afdec)>1 and afdec[-1]=='0':
				afdec.pop()
			obj=super(real,cls).__new__(cls,bfdec+'.'+''.join(afdec),reals)
			obj.__bfdec=list(bfdec)
			obj.__afdec=list(afdec)
			return obj
		raise TypeError('Invaild literal for a real %s'%(num))





















reals=field('reals','R')
complex_nums=field('complex numbers','C')













_math_types=[integer,rational]
_py_to_math_dict= {int:integer,long:integer}
_math_to_py_dict= {integer:int,rational:float}








