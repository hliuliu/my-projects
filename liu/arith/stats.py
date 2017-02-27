'''
stats module

Utilities for computing various statistical summaries
	and performing data analysis.

'''

from calculus import approx as _approx, interval as _itv, ROOT_2 as _root2, ROOT_PI as _rootpi, erfinv as _erfi
from algebra import comb as _comb
import math as _math
import random as _rand

import imp,os
f,n,d=imp.find_module('datas',[os.path.join(os.path.dirname(__file__),os.pardir)])
_datas=imp.load_module('datas',f,n,d)
f,n,d=imp.find_module('algs',_datas.__path__)
_algs=imp.load_module('datas.algs',f,n,d)
del imp,f,n,d,os



_partsort=_algs.partsort
_kthsmallest=_algs.kthsmallest




def runifstd(incl_endpts=True):
	'''
	Purpose:
		returns a random number x between 0 and 1.
		if incl_endpts is True then x lies in [0 , 1]
		else x lies in (0 , 1)
	Preconditions:
		none
	'''
	sample=_rand.random()
	if incl_endpts:
		if not sample:
			return 0.0
		inv=1.0/sample
		if _approx(inv,round(inv,10)):
			inv=round(inv,10)
		if inv==int(inv):
			return 1.0/(inv-1)
		return sample
	sample=1-sample
	inv=1.0/sample
	if _approx(inv,round(inv,10)):
		inv=round(inv,10)
	if inv==int(inv):
		return 1.0/(inv+1)
	return sample


def runif(n,a=0,b=1):
	if type(n) not in [int,long]:
		raise TypeError
	if b<a:
		raise ValueError
	ls=[]
	for i in xrange(n):
		ls.append(runifstd()*(b-a)+a)
	return ls


def rbinom(n,size,p):
	if type(size) not in [int,long]:
		raise TypeError
	if size<=0 or not 0<=p<=1:
		raise ValueError
	ls=[]
	for i in xrange(n):
		k=0
		for j in xrange(size):
			k+=int(runifstd()<=p)
		ls.append(k)
	return ls


def rnorm(n,mu=0,sd=1):
	ls=[]
	for i in xrange(n):
		ls.append(qnorm(runifstd(False),mu,sd))
	return ls





def mean(*args):
	'''
	Purpose:
		computes and returns the arithmetic mean (or average) of the values in args.
		The average of values in a dataset (x_1,...,x_n) is given by 
			x_bar=(x_1+...+x_n)/n
	Preconditions:
		There is at least one element in args.
		each element in args is of type int, float, or long.
	'''
	ans=0
	for i in args:
		if type(i) not in [int,float,long]:
			raise TypeError
		ans+=i
	ans=float(ans)/len(args)
	if _approx(ans,round(ans,10)):
		ans=round(ans,10)
	if _approx(ans,int(ans)):
		ans=int(ans)
	return ans

def geomean(*args):
	ans=1
	for i in args:
		ans*=i
	ans=float(ans)**(1.0/len(args))
	if _approx(ans,round(ans,10)):
		ans=round(ans,10)
	if _approx(ans,int(ans)):
		ans=int(ans)
	return ans

def median(*args):
	'''
	Purpose:
		computes and returns the median of the values in args.
		The median of values in a dataset (x_1,...,x_n) is given by
			x_tilde =
				x_((n+1)/2) if n is odd and
				mean(x_(n/2),x_((n+2)/2)) if n is even
			where (x_(1),...,x_(n)) is the dataset with values in sorted accending order
	Preconditions:
		There is at least one element in args.
		each element in args is of type int, float, or long.
	'''
	if len(args)%2:
		return _kthsmallest((len(args)-1)/2,*args)
	return mean(_kthsmallest(len(args)/2,*args),_kthsmallest(len(args)/2-1,*args))

def quartile1(*args):
	args=list(args)
	_partsort(args,len(args)/2)
	return median(*args[:len(args)/2])

def quartile3(*args):
	args=list(args)
	_partsort(args,len(args)/2)
	if len(args)%2:
		return median(*args[len(args)/2+1:])
	return median(*args[len(args)/2:])

def iqr(*args):
	res=quartile3(*args)-quartile1(*args)
	if _approx(res,round(res,5)):
		res=round(res,5)
	if res==int(res):
		res=int(res)
	return res

def outliers(k,*args):
	if len(args)<4:
		return []
	rng=_itv(quartile1(*args)-iqr(*args)*k,True,quartile3(*args)+iqr(*args)*k,True)
	res=[]
	for i in args:
		if i not in rng:
			res.append(i)
	return res


def sum_squares(*args):
	ans=0
	for a in args:
		ans+=a**2
	if type(ans)==float:
		if _approx(ans,round(ans,10)):
			ans=round(ans,10)
		if _approx(ans,int(ans)):
			ans=int(ans)
	return ans


def variance(*args):
	n=len(args)
	return sum_squares(*args)/float(n-1)-sum(args)**2/float(n)/(n-1)

def stdev(*args):
	return _math.sqrt(variance(args))

def pop_variance(*args):
	n=len(args)
	return (n-1)*variance(*args)/float(n)

def pop_stdev(*args):
	return _math.sqrt(pop_variance(*args))


def freqs(data,hashable=True):
	if hashable:
		fs={}
		for d in data:
			fs[d]=fs.get(d,0)+1
		return fs
	fs=[]
	fskeys=[]
	for d in data:
		i=fskeys.index(d)
		if i>=0:
			x,y=fs[i]
			fs[i]=(x,y+1)
		else:
			fskeys.append(d)
			fs.append((d,1))
	return fs

def pnorm(x,mu=0,sd=1):
	x=(x-mu)/float(sd)
	if _approx(x,round(x,10)):
		x=round(x,10)
	return (1+_math.erf(x/_root2))/2.0

def dnorm(x,mu=0,sd=1):
	x=(x-mu)/float(sd)
	if _approx(x,round(x,10)):
		x=round(x,10)
	return _math.exp(-x*x/2.0)/float(sd)/_root2/_rootpi

def qnorm(x,mu=0,sd=1):
	return mu+sd*_root2*_erfi(2*x-1)

def dunif(x,a=0,b=1):
	if b<a:
		raise ValueError
	if a<=x<=b:
		return 1.0/(b-a)
	return 0.0

def punif(x,a=0,b=1):
	if b<a:
		raise ValueError
	if x<=a:
		return 0.0
	if x>=b:
		return 1.0
	return (x-a)*dunif(x,a,b)

def qunif(p,a=0,b=1):
	if b<a or not 0<=p<=1:
		raise ValueError
	x=p*(b-a)+a
	return x

def dbinom(x,size,p):
	if type(size) not in [int,long]:
		raise TypeError
	if size<=0 or not 0<=p<=1:
		raise ValueError
	if x!=int(x):
		return 0.0
	x=int(x)
	if x>size or x<0:
		return 0.0
	return _comb(size,x)*(p**x)*((1-p)**(size-x))

def pbinom(x,size,p):
	if type(size) not in [int,long]:
		raise TypeError
	if size<=0 or not 0<=p<=1:
		raise ValueError
	if x>=size:
		return 1.0
	if x<0:
		return 0.0
	pr=0.0
	i=0
	while i<=x:
		pr+=dbinom(i,size,p)
		i+=1
	return pr



