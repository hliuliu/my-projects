

class currency(object):
	def __init__(self,value=0):
		if type(value) not in [int,float,long]:
			raise TypeError
		self.__value=round(value,2)
	def __repr__(self):
		return 'currency('+str(self.__value)+')'
	def __str__(self):
		return '$%d'%self.__value
	def __add__(self,other):
		if not isinstance(other,currency):
			raise TypeError
		return currency(self.__value+other.__value)
	def amount(self):
		return self.__value
	def __neg__(self):
		return currency(-self.__value)
	def __sub__(self,other):
		return self+(-other)
	def __mul__(self,num):
		if type(num) not in [int,float,long]:
			raise TypeError
		return currency(self.__value*num)
	def __div__(self,num):
		return self*(1.0/num)
	def __nonzero__(self):
		return bool(self.__value)
	def __eq__(self,other):
		if not isinstance(other,currency):
			return False
		return not (self-other)
	def __lt__(self,other):
		if not isinstance(other,currency):
			return currency<type(other)
		return self.amount()<other.amount()
	def __gt__(self,other):
		if not isinstance(other,currency):
			return currency>type(other)
		return self.amount()>other.amount()
	def __le__(self,other):
		return self<other or self==other
	def __ge__(self,other):
		return self>other or self==other
	def __ne__(self,other):
		return not (self==other)
	def isgain(self):
		return self>currency()
	def isloss(self):
		return self<currency()

class period(object):
	def __init__(self,factor):
		self.__factor=factor
	def factor(self):
		return self.__factor

year_op=period(1)

month_op=period(12)

del period

