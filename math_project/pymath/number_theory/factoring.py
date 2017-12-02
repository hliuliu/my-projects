'''
factoring module

utilities for factoring integers.
This module includes many classic number theoretic functions, 
such as isprime, which detemines whether or not an intger is prime.

'''


import os,sys
sys.path.append(
	os.path.abspath(
		os.path.join(os.path.split(__file__)[0],os.pardir,os.pardir)
	)
)
from pymath.basics import integer as _integer, py_to_math as _pytm
from pymath.basics.integer_tools import \
	integer_xrange as _ixrng, one as _one
del os,sys




_prime_sieve={
	_integer(2):True
}

_max_prime_sieve_len=10000

_prime_sieve_insert_order=list(_prime_sieve)

_smallest_prime_factor={
	_integer(2):_integer(2)
}

def isprime(n):
	'''
	Purpose:
		returns whhether or not an integer n is prime.
		n is prime <==> the only distinct 
			positive divisors of n are 1 and n.
		the above definition already exclude the posibility that n=1

		if n<0, then the function returns whether or not -n is prime
	Preconditions:
		type(n) in [int, long, integer]
	Examples:
		isprime(n) ==> False 
		when n = 0,1,12,18,27,201,343,363
			2 divides 0
			n=1 is not distinct from 1
			3 divides 12 etc..
		isprime(n) ==> True
		when n=2,3,5,17,29,31,101,127,541
	'''
	n=_pytm(n)
	if not isinstance(n,_integer):
		raise TypeError('the argument n must be an integer')
	n=abs(n)
	if n in _prime_sieve:
		return _prime_sieve[n]
	if n in [0,1]:
		return False
	x=_integer(2)
	sieve=_prime_sieve
	if len(sieve)==_max_prime_sieve_len:
		half=len(sieve)/2
		for el in _prime_sieve_insert_order[:half]:
			del _prime_sieve[el]
			del _smallest_prime_factor[el]
	while x**2<=n:
		if x in sieve and not sieve[x]:
			x+=1
			continue
		# if x not in sieve:
		# 	sieve[x]=True
		if not n%x:
			_prime_sieve_insert_order.append(n)
			sieve[n]=False
			_smallest_prime_factor[n]=x
			return False
		# xsqrt=_integer(2)
		# while xsqrt**2<=x:
		# 	xsqrt+=1
		# for i in _ixrng(x*2,n,x):
		# 	sieve[i]=False
		# 	if i==n:
		# 		return False
		x+=1
	sieve[n]=True
	_prime_sieve_insert_order.append(n)
	_smallest_prime_factor[n]=n
	return True



def factorization(n):
	'''
	Purpose:
		returns the prime factorization of the integer n.
		this is represented by a list of pairs(tuples) of integers,
			(p,e) where p is prime and e is the largest nonnegative 
			integer such that p**e divides n.
		the (p,e) pairs in the list are sorted by p in accending order.
		We count the prime factorization of 0 as 0**1;
		and 1 as an empty factorization.
		if n<0 then factorization(n) returns [(-1,1)]+factorization(-n).
	Preconditions:
		type(n) in [int, long, integer]
	'''
	n=_pytm(n)
	if not isinstance(n,_integer):
		raise TypeError('the argument n must be an integer')
	pfact={}
	if n<0:
		pfact[-_one]=_one
		n=-n
	if not n:
		return [(_integer(0),_one)]
	while n>1:
		isprime(n)
		factor=_smallest_prime_factor[n]
		pfact[factor]=pfact.get(factor,_integer(0))+1
		n//=factor
	return [(i,pfact[i]) for i in sorted(pfact)]


def iter_divisors(n):
	'''
	Purpose:
		generates the postive divisors of the integer n in asscending order.
		if n=0, only 0 is generated.
	Preconditions:
		type(n) in [int, long, integer]
	'''
	n=_pytm(n)
	if not isinstance(n,_integer):
		raise TypeError('the argument n must be an integer')
	n=abs(n)
	if not n:
		yield _integer(0)
	else:
		yield _one
		for i in _ixrng(2,n+1):
			if not n%i:
				yield i
		
def divisors(n):
	'''
	same as list(iter_divisors(n))
	'''
	return list(iter_divisors(n))


def isprime_power(n):
	n=_pytm(n)
	if not isinstance(n,_integer):
		raise TypeError('the argument n must be an integer')
	if not n.is_positive():
		return False
	spf=None
	while n>1:
		isprime(n)
		if not spf:
			pass
		elif spf!=_smallest_prime_factor[n]:
			return False
		spf=_smallest_prime_factor[n]
		n//=spf
	return True



def gcd(a,b):
	'''
	Purpose:
		returns the gcd of 2 numbers, a and b.
	Preconidtions:
		type(a),type(b) in [int, integer, rational]
	'''
	a=_pytm(a)
	b=_pytm(b)
	a,b=sorted(map(abs,[a,b]))
	while b:
		r=a%b
		a,b=b,r
	return a





