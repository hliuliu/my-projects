'''
integer_tools module


contains some commonly uesd tools specifically for integers.

constants defined are 
	zero ==> the integer, 0
	one ==> the integer, 1
	dozen ==> the integer, 12
	gross ==> the square of a dozen
	thousand ==> the integer, 1000
	million ==> the integer, 10**6
	billion ==> the integer, 10**9
	trillion ==> the integer, 10**12
	googol ==> the integer, 10**100


'''



import sys,os

sys.path.append(
	os.path.abspath(os.path.join(os.path.split(__file__)[0],os.pardir,os.pardir))
)
from pymath.basics import integer as _integer, py_to_math as _pytm
del sys,os



zero=_integer('0')
one=_integer('1')
dozen=_integer('12')
gross=_integer('144')
thousand=_integer('1000')
million=_integer('1 000 000')
billion=million*thousand
trillion=billion*thousand
googol=_integer('1'+'0'*100)






def iter_digits(n):
	'''
	Purpose:
		iterates through the digits of the integer n, 
			as read from left to right.
		the number, 0, is counted as having one digit.
		if n<0, then -1 is generated, followed by the physical digits.
		the digits are yielded as individual integers 0-9.
	Preconditions:
		type(n) in [int, long, integer]
	Examples:
		iter_digits(0) ==> iter([0])
		iter_digits(3256) ==> iter([3,2,5,6])
		iter_digits(-580) ==> iter([-1,5,8,0])
	'''
	n=_pytm(n)
	if not isinstance(n,_integer):
		raise TypeError('Input must be an integer')
	if n.is_negative():
		yield _integer('-1')
	n=abs(n)
	sn=str(n)
	for d in sn:
		yield _integer(d)


def digits(n):
	'''
	Purpose:
		returns the digits of the integer n, 
			as read from left to right.
		the number, 0, is counted as having one digit.
		if n<0, then -1 is generated, followed by the physical digits.
		the digits are returned, in a list, as individual integers 0-9.
	Preconditions:
		type(n) in [int, long, integer]
	Examples:
		iter_digits(0) ==> [0]
		iter_digits(3256) ==> [3,2,5,6]
		iter_digits(-580) ==> [-1,5,8,0]
	'''
	return list(iter_digits(n))


def integer_xrange(start,stop=None,step=_integer('1')):
	'''
	Purpose:
		generates an arithmetic progression of integers,
		which begins at start and ends before stop,
		adding step at each successive yield.
		Calling integer_xrange(start,None,step) is the same as
			calling integer_xrange(0,start,step).
		The endpoint, stop, is omitted.
	Preconditions:
		type(start),type(step) in [int, long, integer].
		type(stop) in [int, long, integer] or stop==None.
		step!=0.
	Examples:
		integer_xrange(4) ==> iter([0,1,2,3])
		integer_xrange(3,8) ==> iter([3,4,5,6,7])
		integer_xrange(5,1) ==> iter([])
		integer_xrange(2,11,3) ==> iter([2,5,8])
		integer_xrange(4,17,6) ==> iter([4,10,16])
	'''
	start,stop,step=map(_pytm,[start,stop,step])
	if stop==None:
		stop=start
		start=_integer('0')
	for s in [start,stop,step]:
		if not isinstance(s,_integer):
			raise TypeError('Input must all be integers')
	if not step:
		raise ValueError('step argument must be nonzero')
	compare=lambda x,y: x<y if step>0 else x>y
	while compare(start,stop):
		yield start
		start+=step



def integer_range(start,stop=None,step=_integer('1')):
	'''
	same as list(integer_xrange(start,stop,step))
	'''
	return list(integer_xrange(start,stop,step))


def num_digits(n):
	'''
	Purpose:
		returns the number of digits in the integer n.
		if n<0, the negative sign is ignored.
		0 has 1 digit.
	Preconditions:
		type(n) in [int, long, integer]
	Examples:
		num_digits('0') ==> 1
		num_digits('125') ==> 3
		num_digits('-93') ==> 2
	'''
	count=_integer('0')
	n=abs(n)
	for i in iter_digits(n):
		count+=1
	return count

def integer_exp_xrange(base,start,stop=None,step=_integer('1')):
	'''
	Purpose:
		generates a geometric progression of integers, each element
			is of the form base**i, where i>=0 is an integer.
		if type(base)== integer, then this is equvalent to
		(base**i for i in integer_xrange(start,stop,step))
	Preconditions:
		type(base),type(start),type(step) in [int,integer].
		(type(stop) in [int ,integer] and stop>=0) or stop==None.
		start>=0.
	'''
	base=_pytm(base)
	if not isinstance(base,_integer):
		raise TypeError('Input must be an integer')
	ratio=base**abs(step)
	rstart=None
	op=lambda x,y: x*y if step>0 else x//y
	for i in integer_xrange(start,stop,step):
		if rstart==None:
			rstart=base**i
		yield rstart
		rstart=op(rstart,ratio)


def integer_exp_range(base,start,stop=None,step=_integer('1')):
	'''
	same as list(integer_exp_xrange(base,start,stop,step))
	'''
	return list(integer_exp_xrange(base,start,stop,step))


def sum_digits(n):
	'''
	Purpose:
		returns the sum of digits in the integer n.
		if n<0, the negative sign is ignored.
		0 has 1 digit.
	Preconditions:
		type(n) in [int, long, integer]
	Examples:
		sum_digits('0') ==> 0
		sum_digits('125') ==> 8
		sum_digits('-93') ==> 12
	'''
	n=abs(n)
	ans=_integer('0')
	for i in iter_digits(n):
		ans+=i
	return ans



def knuth_arrow(base,exp,num_arrows):
	'''
	Purpose:
		returns the num_arrows times iterate of
			base raised to the exp.
		the n-th iterate of x to the y is denoted as x ->(n) y.
		this is defined, for n>=1, as 
		x ->(n) y = 
			x**y if n==1; and
			( x->(n-1) ( ... ( x ->(n-1) ( x ->(n-1) x ) ) ) ), 
			with 'x->(n-1)' appearing exactly y times, if n>1.
	Preconditions:
		type(arg) in [int, long, integer] for arg in base,exp,num_arrows
		exp>=0
		num_arrows>0
	Note:
		Be careful when calling this function, 
		this can be very slow for small numbers.
	'''
	base,exp,num_arrows=map(_pytm,(base,exp,num_arrows))
	for a in (base,exp,num_arrows):
		if not isinstance(a,_integer):
			raise TypeError('all arguments must be integers')
	if not num_arrows.is_positive():
		raise ValueError('the num_arrows argument must be positive')
	if num_arrows.is_negative():
		raise ValueError('the exp argument must be nonnegative')
	if num_arrows==1:
		return base**exp
	ans=base
	for i in integer_xrange(1,exp):
		ans=knuth_arrow(base,ans,num_arrows-1)
	return ans




