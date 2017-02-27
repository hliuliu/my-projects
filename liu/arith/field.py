
from algebra import intmod as _imd


class galfield(object):
	def __new__(cls,n):
		if cls==primefield:
			return super(galfield,cls).__new__(cls)
		from algebra import isprimepower as ipp,isprime as ip
		if not ipp(n):
			raise ValueError
		if ip(n):
			return primefield(n)
		obj=super(galfield,cls).__new__(cls)
		obj.__order=n
		return obj
	pass

class primefield(galfield):
	'''
	Purpose:
		To implement the properties of a finite field of prime order
	Preconditions:
		Constructor takes one argument n, with type int or long
		n is prime
	'''
	def __new__(cls,n):
		if type(n) not in [int,long]:
			raise TypeError
		if n<=0:
			raise ValueError
		from algebra import isprime
		if not isprime(n):
			raise ValueError
		obj=super(primefield,cls).__new__(cls,n)
		obj.__order=n
		return obj
	def order(self):
		return self.__order
	def element(self,el):
		return fieldelement(el,self)
	def _validateelement(self,el):
		if isinstance(el,int):
			return _imd(el,self.order())
	def add(self,*args):
		ans=_imd(0,self.order())
		for i in args:
			el=self.element(i)
			ans+=el.value()
		return self.element(ans)
	def mult(self,*args):
		ans=_imd(1,self.order())
		for i in args:
			el=self.element(i)
			ans*=el.value()
		return self.element(ans)
	def __iter__(self):
		for i in range(self.order()):
			yield self.element(i)
	def addident(self):
		return self.element(0)
	def multident(self):
		return self.element(1)
	def __eq__(self,other):
		if not isinstance(other,primefield):
			return False
		return self.order()==other.order()
	def __ne__(self,other):
		return not (self==other)
	def addorder(self,el):
		if self.element(el)!=self.addident():
			return self.order()
		return 1
	def multorder(self,el):
		el=self.element(el)
		if el==self.addident():
			raise ValueError('Argument must be nonzero')
		ans=1
		target=el
		while el!=self.multident():
			el*=target
			ans+=1
		return ans
	def __repr__(self):
		return 'primefield(%d)'%self.order()
	def __str__(self):
		return 'finite field of order %d '%self.order()
	def addinv(self,el):
		el=self.element(el)
		return self.element(-el.value())
	def power(self,el,n):
		m=n
		n=int(_imd(n,self.order()-1))
		if self.element(el)==self.addident():
			if m<0:
				raise ValueError
			return self.addident()
		return self.mult(*([el]*n))
	def multinv(self,el):
		el=self.element(el)
		return self.power(el,-1)
	def subt(self,el1,el2):
		return self.add(el1,self.addinv(el2))
	def divide(self,el1,el2):
		return self.mult(el1,self.multinv(el2))
	def __lt__(self,other):
		if not isinstance(other, primefield):
			return NotImplemented
		return self.order()<other.order()
	def __gt__(self,other):
		if not isinstance(other, primefield):
			return NotImplemented
		return self.order()>other.order()
	def __ge__(self,other):
		return self>other or self==other
	def __le__(self,other):
		return self<other or self==other



class fieldelement(object):
	def __new__(cls,val,field):
		if isinstance(val,fieldelement):
			if field.order()!=val.field().order():
				raise ValueError
			return val
		if not isinstance(field,galfield):
			raise TypeError
		v=field._validateelement(val)
		if v==None:
		 	raise TypeError
		obj=super(fieldelement,cls).__new__(cls)
		obj.__val=v
		obj.__field=field
		return obj
	def __repr__(self):
		return 'fieldelement(%s,%r)'%(self.value(),self.field())
	def __str__(self):
		return str(self.__val)
	def __add__(self,other):
		return self.__field.add(self,other)
	def __mul__(self,other):
		return self.__field.mult(self,other)
	def field(self):
		return self.__field
	def value(self):
		return self.__val
	def __eq__(self,other):
		if not isinstance(other,fieldelement):
			return False
		return self.__field==other.__field and self.__val==other.__val
	def __ne__(self,other):
		return not (self==other)
	def __mul__(self,other):
		return self.__field.mult(self,other)
	def __div__(self,other):
		return self.__field.divide(self,other)
	def __pow__(self,p):
		return self.__field.power(self,p)
	def __gt__(self,other):
		if not isinstance(other,fieldelement):
			return NotImplemented
		return self.__val>other.__val
	def __lt__(self,other):
		if not isinstance(other,fieldelement):
			return NotImplemented
		return self.__val<other.__val
	def __le__(self,other):
		return self<other or self==other
	def __ge__(self,other):
		return self>other or self==other
	def __nonzero__(self):
		return bool(self.__val)


