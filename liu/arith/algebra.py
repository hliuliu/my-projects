
import vector as _vector
from random import random as _random, randrange as _rrange

MILL=1.3063778838630806904686

def gcd(a,b):
	'''
	Purpose:
		returns the gcd of 2 integers, a and b.
		This is an integer d>0 such that d divides a and b,
		and if k>d is an integer, then k does not divde both a and b.
	Preconditions:
		a and b are of type int or long
	Examples:
		gcd(5,7) ==> 1
		gcd(105,14) ==> 7
		gcd(24,0) ==> 24
		gcd(-13,26) ==> 13
		gcd(-12,-15) ==> 3
	'''
	if type(a) not in [int,long] or type(b) not in [int,long]:
		raise TypeError
	a,b=abs(a),abs(b)
	a,b=max(a,b),min(a,b)
	while b:
		a,b=b,a%b
	return a

def isrelprime(a,b):
	'''
	Purpose:
		returns whether or not 2 integers, a and b, are relatively prime.
		isrelprime(a,b) <==> gcd(a,b)==1
	Preconditions:
		a and b are of type int or long
	Examples:
		isrelprime(5,7) ==> True
		isrelprime(105,14) ==> False
		isrelprime(24,0) ==> False
		isrelprime(-13,26) ==> False
		isrelprime(22,-15) ==> True
		isrelprime(-18,-25) ==> True
	'''
	return gcd(a,b)==1

def lcm(a,b):
	'''
	Purpose:
		returns the lcm of 2 integers, a and b.
		This is an integer d>0 such that d is a multiple of a and b,
		and if 0<k<d is an integer, then k is not a multiple of both a and b.
	Preconditions:
		a and b are of type int or long
	Examples:
		lcm(5,7) ==> 35
		lcm(105,14) ==> 210
		lcm(24,0) ==> 0
		lcm(-13,26) ==> 26
		lcm(-12,-15) ==> 60
	'''
	return abs(a*b)/gcd(a,b)

def isprime(n):
	'''
	Purpose:
		returns whhether or not an integer n is prime.
		n is prime <==> the only distinct positive divisors of n are 1 and n.
	Preconditions:
		n is of type int or long
		n>=0
	Examples:
		isprime(n) ==> False 
		when n = 0,1,12,18,27,201,343,363
			2 divides 0
			n=1 is not distinct from 1
			3 divides 12 etc..
		isprime(n) ==> True
		when n=2,3,5,17,29,31,101,127,541
	'''
	if type(n) not in [int, long]:
		raise TypeError
	if n<0:
		raise ValueError('input must be nonnegative.')
	if n in [0,1]:
		return False
	x=2
	while x**2<=n:
		x+=1
	sieve=[True]*(x+1)
	x=2
	while x**2<=n:
		if not sieve[x]:
			x+=1
			continue
		if not n%x:
			return False
		for i in xrange(x*2,len(sieve),x):
			if i<len(sieve):
				sieve[i]=False
			if i==n:
				return False
		x+=1
	return True

def isprimepower(n):
	if type(n) not in [int, long]:
		raise TypeError
	if n<0:
		raise ValueError('input must be nonnegative.')
	return 	len(primefactors(n))==1

def euler_phi(n):
	if type(n) not in [int, long]:
		raise TypeError
	if n<=0:
		raise ValueError('input must be positive.')
	count=1
	pf=primefactors(n,True)
	for p,e in pf:
		if e:
			count*=p**(e-1)*(p-1)
	return count

def fact(n):
	if type(n) not in [int, long]:
		raise TypeError
	if n<0:
		raise ValueError('input must be nonnegative.')
	if n==0:
		return 1
	ans=1
	for i in xrange(2,n+1):
		ans*=i
	return ans

def factors(n):
	if type(n) not in [int, long]:
		raise TypeError
	if n<0:
		return factors(-n)
	if n==0:
		raise ValueError('input must be nonzero.')
	fac=set()
	if n==1:
		return {1,-1}
	h=n/2
	while n%h:
		h-=1
	fh=factors(h)
	return fac.union(fh).union({n/i for i in fh})

def primefactors(n,power=False):
	if type(n) not in [int, long]:
		raise TypeError
	if n<0:
		return primefactors(-n)
	if n==0:
		raise ValueError('input must be nonzero.')
	res=factors(n)
	pf=set()
	for i in res:
		if i<0:
			continue
		if isprime(i):
			pf.add(i)
	if not power:
		return pf
	pf=list(pf)
	pp=[]
	for p in list(pf):
		q,s=0,1
		while not n%s:
			q+=1
			s*=p
		pp.append(q-1)
	return set(zip(pf,pp))

def isperfect(n):
	if type(n) not in [int, long]:
		raise TypeError
	if n<0:
		raise ValueError('input must be nonnegative.')
	if n==0:
		return False
	fa,ans=factors(n),0
	for i in fa:
		if 0<i<n:
			ans+=i
	return ans==n

def digits(num,decp='before'):
	if type(num) not in [int,long,float]:
		raise TypeError
	if decp.lower() not in ['before','after','all']:
		raise ValueError('invalid argument decp')
	if decp.lower()=='all':
		return digits(num)+digits(num,'after')
	if num<0:
		return digits(-num,decp)
	inum=int(num)
	num=inum if decp=='before' else num-inum
	dig=[]
	if 0<num<1:
		num=str(num)[2:]
		return [int(i) for i in num]
	while num:
		dig.insert(0,int(num%10))
		num/=10
	return dig

def fib(n):
	if type(n) not in [int, long]:
		raise TypeError
	if n<0:
		raise ValueError('input must be nonnegative.')
	return (matrix([[1,1],[1,0]])**n).get(0,0)

def sumdigits(n,decp='before'):
	ans=0
	for i in digits(n,decp):
		ans+=i
	return ans

def iskeith(n):
	if type(n) not in [int,long]:
		raise TypeError
	if n<10:
		return False
	d,sd=digits(n),sumdigits(n)
	while sd<n:
		d.append(sd)
		sd=2*sd-d[0]
		del d[0]
	return sd==n

def ceil(x):
	if type(x) not in [float,int,long]:
		raise TypeError
	if x==int(x):
		return int(x)
	if x<0:
		x=-x
		return -int(x)
	return int(x)+1

def floor(x):
	return -ceil(-x)

def comb(n,r):
	for i in [n,r]:
		if type(i) not in [int,long]:
			raise TypeError
		if i<0:
			return 0
	if r>n:
		return 0
	if r==n:
		return 1
	nhalf=n/2
	if r<nhalf:
		r=n-r
	ans=1
	for i in xrange(r+1,n+1):
		ans*=i
		ans/=(i-r)
	return ans

def perm(n,r):
	return comb(n,r)*fact(r)

def catalan(n):
	if n<0:
		raise ValueError('input must be nonnegative.')
	return comb(2*n,n)/(n+1)

class fraction(object):
	def __new__(cls,num=0,dem=1):
		if type(num) not in [int,long] or type(dem) not in [int,long] or not dem:
			raise TypeError
		obj=super(fraction,cls).__new__(cls)
		g=gcd(num,dem)
		obj.__num=num/g
		obj.__dem=dem/g
		if obj.__dem<0:
			obj.__num*=-1
			obj.__dem*=-1
		return obj
	def __str__(self):
		return str(self.__num)+('/'+str(self.__dem) if self.__dem!=1 else '')
	def __repr__(self):
		return str(self)
	def __abs__(self):
		return fraction(abs(self.__num),self.__dem)
	def isproper(self):
		return abs(self.__num)<self.__dem
	def __add__(self,other):
		if not isinstance(other,fraction):
			other=fraction(other)
		a,b,c,d=self.__num,self.__dem,other.__num,other.__dem
		return fraction(a*d+b*c,b*d)
	def __neg__(self):
		return fraction(-self.__num,self.__dem)
	def __sub__(self,other):
		return self+(-other)
	def __mul__(self,other):
		if not isinstance(other,fraction):
			other=fraction(other)
		a,b,c,d=self.__num,self.__dem,other.__num,other.__dem
		return fraction(a*c,b*d)
	def __div__(self,other):
		if not isinstance(other,fraction):
			other=fraction(other)
		a,b,c,d=self.__num,self.__dem,other.__num,other.__dem
		return fraction(a*d,b*c)
	def reciprocal(self):
		return fraction(1)/self
	def __pow__(self,exp):
		return fraction(self.__num**exp,self.__dem**exp)
	def __eq__(self,other):
		if not isinstance(other,fraction):
			other=fraction(other)
		return self.__num==other.__num and self.__dem==other.__dem
	def __gt__(self,other):
		if not isinstance(other,fraction):
			other=fraction(other)
		return self.__num*other.__dem>other.__num*self.__dem
	def __ge__(self,other):
		return self==other or self>other
	def __lt__(self,other):
		if not isinstance(other,fraction):
			other=fraction(other)
		return other>self
	def __le__(self,other):
		return self==other or self<other
	def isint(self):
		return self.__dem==1
	def __int__(self):
		if not self.isint():
			raise TypeError
		return self.__num
	def isegyptian(self):
		return self.reciprocal().isint()
	def __float__(self):
		return float(self.__num)/self.__dem
	def __copy__(self):
		return self+0
	def __abs__(self):
		return -self if self<0 else self
	def numrator(self):
		return self.__num
	def denominator(self):
		return self.__dem

def floattofrac(fl):
	if type(fl)!=float:
		raise TypeError
	factor=1
	while int(fl)!=fl:
		factor*=10
		fl*=10
	return fraction(int(fl),factor)

def brocot(n):
	if type(n) not in [int,long]:
		raise TypeError
	if n<0:
		raise ValueError
	start=[(0,1),(1,1),(1,0)]
	def track(start,n):
		if n==0:
			return
		track(start,(n-1)/2)
		if n%2:
			start.pop(2)
			l,r=start
		else:
			start.pop(0)
			l,r=start
		start.insert(1,[i+j for i,j in zip(l,r)])
	track(start,n)
	return fraction(*(start[1]))


def fracrange(start,stop=None,step=fraction(1)):
	if stop==None:
		start,stop=fraction(),start
	if not isinstance(start,fraction):
		start=fraction(start)
	if not isinstance(stop,fraction):
		stop=fraction(stop)
	if not isinstance(step,fraction):
		step=fraction(step)
	i=start.clone()
	def upperrange(i):
		rval=[]
		while i<stop:
			rval+=[i]
			i+=step
		return rval
	def lowerrange(i):
		rval=[]
		while i>stop:
			rval+=[i]
			i+=step
		return rval
	if step==0:
		raise Exception('step cannot be zero')
	return upperrange(i) if step>0 else lowerrange(i)


class matrix(object):
	__fmt=20
	def __new__(cls,arr):
		from calculus import approx
		obj=super(matrix,cls).__new__(cls)
		obj.__row=len(arr)
		obj.__col=max(0,*[len(a) for a in arr])
		obj.__array=[[0]*obj.__col for i in range(obj.__row)]
		for i,i2 in enumerate(obj.__array):
			for j,j2 in enumerate(i2):
				try:
					if type(arr[i][j]) not in [int,float,long]:
						raise TypeError
					obj.__array[i][j]=arr[i][j] if not approx(arr[i][j],int(round(arr[i][j]))) else int(round(arr[i][j]))
				except TypeError:
					raise TypeError
				except:
					pass
		return obj
	def __str__(self):
		return '\n'.join([''.join([('%fs'.replace('f',str(matrix.__fmt)))%j for j in i]) for i in self.__array])+'\n'
	def __repr__(self):
		return str(self.__array)
	@classmethod
	def setmatrixfmt(cls,space):
		if type(space) == int:
			cls.__fmt=space
	def get(self,r,c):
		return self.__array[r][c]
	def numrows(self):
		return self.__row
	def numcols(self):
		return self.__col
	def transpose(self):
		return matrix(zip(*self.__array))
	def rows(self):
		return [_vector.vector(*i) for i in self.__array]
	def cols(self):
		return self.transpose().rows()
	def __eq__(self,other):
		if not isinstance(other,matrix):
			raise TypeError
		if self.numrows()!=other.numrows() or self.numcols()!=other.numcols():
			return False
		for i,j in zip(self.rows(),other.rows()):
			if i!=j:
				return False
		return True
	def __ne__(self,other):
		return not self==other
	def __add__(self,other):
		if not isinstance(other,matrix):
			raise TypeError
		if self.numrows()!=other.numrows() or self.numcols()!=other.numcols():
			raise TypeError
		sumar=[i+j for i,j in zip(self.rows(),other.rows())]
		return matrix([i.tolist() for i in sumar])
	def __neg__(self):
		return matrix([(-i).tolist() for i in self.rows()])
	def __sub__(self,other):
		return self+(-other)
	def issquare(self):
		return self.numrows()==self.numcols()
	def __mul__(self,other):
		import vector
		if type(other) in [int,float,long]:
			return matrix([(i*other).tolist() for i in self.rows()])
		m,n,p,q=dim(self)+dim(other)
		if n!=p:
			raise TypeError
		rv,cv=self.rows(),other.cols()
		res=[[0]*q for i in range(m)]
		for i,i2 in enumerate(res):
			for j,j2 in enumerate(i2):
				res[i][j]=vector.dot(rv[i],cv[j])
		return matrix(res)
	def submatrix(self,r,c):
		rv=self.rows()
		del rv[r]
		#print [i.tolist() for i in rv]
		ans=matrix([i.tolist() for i in rv])
		cv=ans.cols()
		del cv[c]
		ans=matrix([i.tolist() for i in cv]).transpose()
		return ans
	def tolist(self):
		import copy
		return copy.deepcopy(self.__array)
	def symmetric(self):
		if not self.issquare():
			return False
		return self.transpose()==self
	def antisymmetric(self):
		if not self.issquare():
			return False
		return self.transpose()==-self
	def __pow__(self,n):
		if type(n) not in [int,long]:
			raise TypeError
		if n<0:
			return inv(self)**(-n)
		if n==0:
			return ident(self.numrows())
		if n==1:
			return self+zeroes(*dim(self))
		ans=(self*self)**(n/2)
		if n%2:
			ans*=self
		return ans
	def split(self,i,j):
		if (not 0<=i<self.numrows()) or (not 0<=j<self.numcols()):
			raise ValueError
		mlist=self.tolist()
		if i==self.numrows()-1:
			if j==self.numcols()-1:
				return [[matrix(mlist)]]
			return [[matrix([k[:j+1] for k in mlist]),matrix([k[j+1:] for k in mlist])]]
		if j==self.numcols()-1:
			return [[matrix(mlist[:i+1])],[matrix(mlist[i+1:])]]
		sp=[[None,None],[None,None]]
		sp[0][0]=matrix([k[:j+1] for k in mlist[:i+1]])
		sp[0][1]=matrix([k[j+1:] for k in mlist[:i+1]])
		sp[1][0]=matrix([k[:j+1] for k in mlist[i+1:]])
		sp[1][1]=matrix([k[j+1:] for k in mlist[i+1:]])
		return sp

def dim(mat):
	return mat.numrows(),mat.numcols()

def randmat(r,c):
	z=zeroes(r,c).tolist()
	for i in range(r):
		for j in range(c):
			z[i][j]=_rand()
	return matrix(z)

def ones(r,c):
	res=zeroes(r,c).tolist()
	for i in range(r):
		for j in range(r):
			res[i][j]=1
	return matrix(res)

def zeroes(r,c):
	return matrix([[0]*c]*r)
def ident(size):
	import vector
	return matrix([i.tolist() for i in vector.bases(size)])
def randmatint(rows,cols,maxval):
	m=[]
	for i in range(rows):
		m+=[[_rrange(maxval) for j in range(cols)]]
	return matrix(m)
def det(mat):
	if not mat.issquare():
		raise TypeError('Matrix must be square!')
	if mat.numrows()==1:
		return mat.get(0,0)
	ans=0
	for i,j in enumerate(mat.rows()[0].tolist()):
		ans+=j*(-1)**i*det(mat.submatrix(0,i))
	return int(ans) if ans==int(ans) else ans
def trace(mat):
	if not mat.issquare():
		raise TypeError('Matrix must be square!')
	sums=0
	for i in range(mat.numrows()):
		sums+=mat.get(i,i)
	return int(sums) if sums==int(sums) else sums
def minors(mat):
	if not mat.issquare():
		raise TypeError('Matrix must be square!')
	ans=zeroes(*dim(mat)).tolist()
	for i,i2 in enumerate(ans):
		for j,j2 in enumerate(i2):
			ans[i][j]=det(mat.submatrix(i,j))
	return matrix(ans)
def cof(mat):
	m=minors(mat).tolist()
	m=[[j2*(-1)**(i+j) for j,j2 in enumerate(i2)] for i,i2 in enumerate(m)]
	return matrix(m)
def inv(mat):
	if not isinstance(mat,matrix):
		raise TypeError
	if not mat.issquare():
		raise ValueError
	mat=augment(mat,ident(mat.numrows()))
	mat=rref(mat)
	comps=mat.split(mat.numrows()-1,mat.numrows()-1)[0]
	if comps[0]!=ident(mat.numrows()):
		raise ValueError('matrix is not invertible')
	return comps[1]
	#return cof(mat).transpose()*(1.0/det(mat))

def diag(*args):
	import vector
	v=vector.bases(len(args))
	for i,a in enumerate(args):
		if type(a) not in [int,float,long]:
			raise TypeError
		v[i]*=a
	return matrix([i.tolist() for i in v])
def diagblocks(*args):
	if not args:
		raise ValueError('Must have at least one argument.')
	if len(args)==1:
		return matrix(args[0].tolist())
	b1=diagblocks(*args[:len(args)/2])
	b2=diagblocks(*args[len(args)/2:])
	b1=augment(b1,zeroes(b1.numrows(),b2.numcols()))
	b2=augment(zeroes(b2.numrows(),b1.numcols()-b2.numcols()),b2)
	return matrix(b1.tolist()+b2.tolist())

def jordan(*args):
	blks=[]
	for i,j in args:
		d=diag(*([i]*j)).tolist()
		for k in range(j-1):
			d[k][k+1]=1
		blks.append(matrix(d))
	return diagblocks(*blks)

def scaledrow(scalar,row,mat):
	if not isinstance(mat,matrix):
		raise TypeError
	rv=mat.rows()
	rv[row]*=scalar
	return matrix([i.tolist() for i in rv])

def addedrow(row1,scalar,row2,mat):
	if not isinstance(mat,matrix):
		raise TypeError
	rv=mat.rows()
	rv[row1]+=rv[row2]*scalar
	return matrix([i.tolist() for i in rv])

def swappedrows(row1,row2,mat):
	if not isinstance(mat,matrix):
		raise TypeError
	rv=mat.rows()
	rv[row1],rv[row2]=rv[row2],rv[row1]
	return matrix([i.tolist() for i in rv])

def scaledcol(scalar,col,mat):
	if not isinstance(mat,matrix):
		raise TypeError
	rv=mat.cols()
	rv[col]*=scalar
	return matrix([i.tolist() for i in rv]).transpose()

def addedcol(col1,scalar,col2,mat):
	if not isinstance(mat,matrix):
		raise TypeError
	rv=mat.cols()
	rv[col1]+=rv[col2]
	return matrix([i.tolist() for i in rv]).transpose()

def swappedcols(col1,col2,mat):
	if not isinstance(mat,matrix):
		raise TypeError
	rv=mat.cols()
	rv[col1],rv[col2]=rv[col2],rv[col1]
	return matrix([i.tolist() for i in rv]).transpose()

def ref(mat,ppiv=True):
	if not isinstance(mat,matrix):
		raise TypeError
	mat=matrix(mat.tolist())
	currow,curcol=0,0
	import vector
	while 0<=currow<mat.numrows() and 0<=curcol<mat.numcols():
		rv,cv=mat.rows(),mat.cols()
		while curcol<mat.numcols() and cv[curcol].subvector(currow)==vector.zeroes(mat.numrows()-currow):
			curcol+=1
		if curcol==mat.numcols():
			break
		lead=mat.get(currow,curcol)
		if ppiv:
			leadingrow=currow
			for i in range(currow+1,mat.numrows()):
				if abs(mat.get(i,curcol))>abs(lead):
					#mat=swappedrows(i,currow,mat)
					#rv,cv=mat.rows(),mat.cols()
					lead=mat.get(i,curcol)
					leadingrow=i
			mat=swappedrows(leadingrow,currow,mat)
		elif lead==0:
			for i in range(currow+1,mat.numrows()):
				if mat.get(i,curcol)!=0:
					mat=swappedrows(i,currow,mat)
					rv,cv=mat.rows(),mat.cols()
					lead=mat.get(currow,curcol)
					break;
		if lead!=0:
			for i in range(currow+1,mat.numrows()):
				mat=addedrow(i,-mat.get(i,curcol)/float(lead),currow,mat)
		currow+=1
		curcol+=1
	return mat
def leadingpos(mat):
	if not isinstance(mat,matrix):
		raise TypeError
	mat=mat.tolist()
	restups=[]
	for i,j in enumerate(mat):
		k=0
		while k<len(j) and j[k]==0:
			k+=1
		if k<len(j):
			restups+=[(i,k)]
	return restups
def rref(mat):
	if not isinstance(mat,matrix):
		raise TypeError
	mat=ref(mat)
	for row,col in leadingpos(mat):
		mat=scaledrow(1.0/mat.get(row,col),row,mat)
		for i in range(row):
			mat=addedrow(i,-mat.get(i,col),row,mat)
	return mat
def rank(mat):
	if not isinstance(mat,matrix):
		raise TypeError
	return len(leadingpos(ref(mat)))
def nullity(mat):
	if not isinstance(mat,matrix):
		raise TypeError
	return mat.numcols()-rank(mat)
def linearindep(*args):
	import vector
	for a in args:
		if not isinstance(a,vector.vector):
			raise TypeError
	m=[a.tolist() for a in args]
	m=matrix(m).transpose()
	return rank(m)==m.numcols()

def vandermonde(numvars,*args):
	if type(numvars)!=int:
		raise TypeError
	vm=[]
	for a in args:
		if type(a) not in [int,float,long]:
			raise TypeError
		row=[]
		x=1.0
		for i in range(numvars):
			row.append(x)
			x*=a
		vm.append(row)
	return matrix(vm)

def hilb(n):
	hblist=zeroes(n,n).tolist()
	for i,i2 in enumerate(hblist):
		for j,j2 in enumerate(i2):
			hblist[i][j]=1.0/(i+j+1)
	return matrix(hblist)

def augment(*mats):
	newmat=[]
	for i in mats:
		if not isinstance(i,matrix):
			raise TypeError
		if newmat==[]:
			newmat=i.tolist()
		else:
			l=i.tolist()
			bigger=newmat if len(newmat)>len(l) else l
			smaller= l if bigger==newmat else newmat
			for j in range(len(smaller),len(bigger)):
				smaller.append([0]*len(smaller[0]))
			for j,(k0,k1) in enumerate(zip(newmat,l)):
				newmat[j]=k0+k1
	return matrix(newmat)


class vectorspace(object):
	def __new__(cls,*args):
		import vector
		obj=super(vectorspace,cls).__new__(cls)
		obj.__spacemat=[]
		for a in args:
			if not isinstance(a,vector.vector):
				raise TypeError
			obj.__spacemat.append(a.tolist())
		obj.__spacemat=matrix(obj.__spacemat)
		obj.__spacemat=rref(obj.__spacemat)
		return obj

	def __contains__(self,vec):
		import vector
		if not isinstance(vec,vector.vector):
			raise TypeError
		if vec.dimensions()!=self.__spacemat.numcols():
			return False
		for i in rref(augment(self.__spacemat.transpose(),matrix([vec.tolist()]).transpose())).rows():
			j=i.tolist()
			if j[-1]!=0 and j[:-1]==[0]*(len(j)-1):
				return False
		return True
	def dimensions(self):
		import vector
		r=self.__spacemat.rows()
		for i in list(r):
			if i==vector.zeroes(i.dimensions()):
				r.remove(i)
		return len(r)
	def issubspaceof(self,other):
		if not isinstance(other,vectorspace):
			raise TypeError
		for i in self.__spacemat.rows():
			if not (i in other):
				return False
		return True
	def __eq__(self,other):
		return self.issubspaceof(other) and other.issubspaceof(self)
	def __ne__(self,other):
		return not self==other
	def isbasis(self,*args):
		if self.dimensions()!=len(args):
			return False
		other=span(*args)
		return self==other
	def __str__(self):
		import vector
		res='Span {'
		r=[str(i) for i in self.__spacemat.rows() if i!=vector.zeroes(i.dimensions())]
		res+=', '.join(r)+'}'
		return res
	def __repr__(self):
		return str(self)
	def genmat(self,zero=False):
		import vector
		m=self.__spacemat.rows()
		if zero:
			return matrix([i.tolist() for i in m])
		while len(m)>1 and m[-1]==vector.zeroes(m[-1].dimensions()):
			del m[-1]
		return matrix([i.tolist() for i in m])
	def getbasis(self):
		return self.genmat().rows()
	def __add__(self,other):
		if not isinstance(other,vectorspace):
			raise TypeError
		if self.__spacemat.numcols()!=other.__spacemat.numcols():
			raise ValueError
		return span(*(self.getbasis()+other.getbasis()))
	def __nonzero__(self):
		return bool(self.dimensions())
	def __and__(self,other):
		if not isinstance(other,vectorspace):
			raise TypeError
		if self.__spacemat.numcols()!=other.__spacemat.numcols():
			raise ValueError
		nself=nullspace(self.genmat())
		nother=nullspace(other.genmat())
		return nullspace((nself+nother).genmat())



def span(*args):
	return vectorspace(*args)

def rowspace(mat):
	if not isinstance(mat,matrix):
		raise TypeError
	return span(*mat.rows())

def colspace(mat):
	if not isinstance(mat,matrix):
		raise TypeError
	return span(*mat.cols())

def solve(mat,vec):
	import vector
	if not isinstance(mat,matrix) or not isinstance(vec,vector.vector):
		raise TypeError
	if mat.numrows()!=vec.dimensions() or not mat.issquare() or rank(mat)<mat.numrows():
		raise ValueError
	return rref(augment(mat,matrix([vec.tolist()]).transpose())).cols()[-1]

def nullspace(mat):
	import vector
	if not isinstance(mat,matrix):
		raise TypeError
	mat=rref(mat)
	lp=leadingpos(mat)
	leadrows,leadcols=[i for i,j in lp],[j for i,j in lp]
	freevars=[i for i in range(mat.numcols()) if i not in leadcols]
	vecs=[]
	colv=[i.tolist() for i in mat.cols()]
	lp =dict(lp)
	for i in freevars:
		vlst=[0]*mat.numcols()
		vlst[i]=1
		for j,j2 in enumerate(colv[i]):
			if lp[j]>i:
				break
			vlst[lp[j]]=-j2
		vecs.append(vector.vector(*vlst))
	if not vecs:
		vecs.append(vector.zeroes(mat.numcols()))
	return span(*vecs)

class relation(object):
	def __init__(self,somelist,rels=[]):
		self.__onlist=[]
		from copy import deepcopy
		for i in somelist:
			if i not in self.__onlist:
				self.__onlist+=[deepcopy(i)]
		self.__rels=[]
		for i,j in rels:
			self.relate(deepcopy(i),deepcopy(j))
	def relate(self,a,b):
		if (a,b) in self.__rels:
			return
		for i in (a,b):
			if i not in self.__onlist:
				raise ValueError
		self.__rels+=[(a,b)]
	def unrelate(self,a,b):
		if (a,b) in self.__rels:
			self.__rels.remove((a,b))
	def togglerelate(self,a,b):
		{True:self.unrelate,False:self.relate}[(a,b) in self.__rels](a,b)
	def __str__(self):
		return str(sorted(self.__onlist))+' '+str(sorted(self.__rels))
	def isreflexive(self):
		for i in self.__onlist:
			if (i,i) not in self.__rels:
				return False
		return True
	def issymmetric(self):
		for i,j in self.__rels:
			if (j,i) not in self.__rels:
				return False
		return True
	def istransitive(self):
		for i,j in self.__rels:
			for k,l in self.__rels:
				if j!=k:
					continue
				if (i,l) not in self.__rels:
					return False
		return True
	def tolist(self):
		from copy import deepcopy
		return sorted(deepcopy(self.__onlist)),sorted(deepcopy(self.__rels))
	def isrelated(self,a,b):
		return (a,b) in self.__rels
	def isirreflexive(self):
		for i in self.__onlist:
			if (i,i) in self.__rels:
				return False
		return True
	def isantisymmetric(self):
		for i,j in self.__rels:
			if i==j:
				continue
			if (j,i) in self.__rels:
				return False
		return True
	def isequiv(self):
		return all([self.isreflexive(),self.issymmetric(),self.istransitive()])
	def ispartialorder(self):
		return all([self.isreflexive(),self.isantisymmetric(),self.istransitive()])
	def leftrels(self,a):
		retlist=[]
		for i,j in self.__rels:
			if i==a:
				retlist+=[j]
		return retlist
	def rightrels(self,b):
		retlist=[]
		for i,j in self.__rels:
			if j==b:
				retlist+=[i]
		return retlist

def equivclasses(rel):
	if not isinstance(rel,relation):
		raise TypeError
	if not rel.isequiv():
		raise ValueError('must be an equivalence relation.')
	ol,r=rel.tolist()
	res=[]
	for i in list(ol):
		if i not in ol:
			continue
		res+=[rel.leftrels(i)]
		for j in res[-1]:
			ol.remove(j)
	return res

def reflrel(vals):
	return relation(vals,zip(vals,vals))

def fullrel(vals):
	r=relation(vals)
	for i in r:
		for j in r:
			r.relate(i,j)
	return r

class intmod(int):
	def __new__(cls,val,n):
		if not isinstance(val,int) or type(n)!=int:
			raise TypeError
		if n<=0:
			raise ValueError('value must be modulo a positive number')
		obj=super(intmod,cls).__new__(cls,val%n)
		obj.__n=n
		return obj
	def modval(self):
		return self.__n
	def __add__(self,other):
		if not isinstance(other,int):
			raise TypeError
		if isinstance(other,intmod) and self.__n!=other.__n:
			raise ValueError('+ can only be used on 2 ints modulo the same number')
		return intmod(int(self)+int(other),self.__n)
	def __sub__(self,other):
		if not isinstance(other,int):
			raise TypeError
		if isinstance(other,intmod) and self.__n!=other.__n:
			raise ValueError('- can only be used on 2 ints modulo the same number')
		return self+(-other)
	def __mul__(self,other):
		if not isinstance(other,int):
			raise TypeError
		if isinstance(other,intmod) and self.__n!=other.__n:
			raise ValueError('* can only be used on 2 ints modulo the same number')
		return intmod(int(self)*int(other),self.__n)
	def __eq__(self,other):
		if isinstance(other,intmod):
			return False if self.__n!=other.__n else int(self)==int(other)
		return False
	def __nonzero__(self):
		return int(self)!=0
	def __div__(self,other):
		if not isinstance(other,int):
			raise TypeError
		if isinstance(other,intmod) and self.__n!=other.__n:
			raise ValueError('/ can only be used on 2 ints modulo the same number')
		for i in range(self.__n):
			i=intmod(i,self.__n)
			if i*other==self:
				return i
		raise ArithmeticError('%d / %d is invalid modulo %d' %(self,other,self.__n))
	def __pow__(self,other):
		if type(other) !=int:
			raise TypeError
		if other==0:
			return intmod(1,self.__n)
		if other<0:
			return (self**0)/self**(-other)
		if other==1:
			return self
		x= self**(other/2)
		if other%2:
			return x*x*self
		return x*x

def genmodadd(imod):
	if not isinstance(imod,intmod):
		raise TypeError
	gen=[imod*0]
	jmod=imod
	while jmod not in gen:
		gen.append(jmod)
		jmod+=imod
	return gen

def genmodmult(imod,allowgcderr=True):
	if not isinstance(imod,intmod):
		raise TypeError
	if allowgcderr and not isrelprime(int(imod),imod.modval()):
		raise ValueError('%d and %d are not relatively prime.'%(imod,imod.modval()))
	if not imod:
		return [imod]
	gen=[imod**0]
	jmod=imod
	while jmod not in gen:
		gen.append(jmod)
		jmod*=imod
	return gen

def magic(n):
	if type(n) not in [int,long]:
		raise TypeError
	if n<=0 or n==2:
		raise ValueError
	if n%2:
		mag=zeroes(n,n).tolist()
		x,y=0,n/2
		for i in range(1,n**2+1):
			mag[x][y]=i
			xt,yt=(x-1)%n,(y+1)%n
			if mag[xt][yt]:
				x=(x+1)%n
			else:
				x,y=xt,yt
		return matrix(mag)
	if not n%4:
		mag=zeroes(n,n).tolist()
		for i in range(n):
			for j in range(n):
				mag[i][j]=i*n+j+1
				i4,j4=i%4,j%4
				if i4==j4 or i4+j4==3:
					mag[i][j]=n**2+1-mag[i][j]
		return matrix(mag)
	mag=zeroes(n,n).tolist()
	m=(n-2)/4
	mag2=magic(n/2)
	lux=[]
	lux+=[['L']*(n/2) for i in range(m+1)]
	lux+=[['U']*(n/2)]
	lux+=[['X']*(n/2) for i in range(m-1)]
	lux[m][m],lux[m+1][m]='U','L'
	for i in range(n/2):
		for j in range(n/2):
			ll=(2*i,2*j)
			lr=(2*i,2*j+1)
			rl=(2*i+1,2*j)
			rr=(2*i+1,2*j+1)
			if lux[i][j]=='L':
				seq=(lr,rl,rr,ll)
			elif lux[i][j]=='U':
				seq=(ll,rl,rr,lr)
			else:
				seq=(ll,rr,rl,lr)
			for k1,k2 in enumerate(seq,4*(mag2.get(i,j)-1)+1):
				x,y=k2
				mag[x][y]=k1
	return matrix(mag)

def permmat(*args):
	if not args:
		raise ValueError
	if set(args)!=set(range(len(args))):
		for a in args:
			if type(a) not in [int,long]:
				raise TypeError
		raise ValueError
	p=zeroes(len(args),len(args)).tolist()
	for i,j in enumerate(args):
		p[i][j]=1
	return matrix(p)

def rot90(mat):
	'''
	Purpose:
		returns the 90 degrees ccw rotation of the matrix mat.
	Preconditions:
		mat is of type matrix
		mat is m by n where m,n>0
	Examples:
		if mat is the matrix
			1	2
			3	4
		then rot90(mat) is the matrix
			2	4
			1	3
		if mat is the matrix
			1	2	0
			3	5	-1
		then rot90(mat) is the matrix
			0	-1
			2	5
			1	3
	'''
	if not isinstance(mat,matrix):
		raise TypeError
	mat=mat.transpose()
	mat=mat.tolist()
	mat.reverse()
	return matrix(mat)

def rot180(mat):
	return rot90(rot90(mat))
def rot270(mat):
	return rot90(rot180(mat))

def ismagic(mat):
	if not isinstance(mat,matrix):
		raise TypeError
	if not mat.issquare():
		return False
	cons=None
	found=[]
	for i in mat.tolist():
		for j in i:
			if j in found:
				return False
			found.append(j)
		if cons==None:
			cons=sum(i)
		elif cons!=sum(i):
			return False
	for i in mat.transpose().tolist():
		if cons!=sum(i):
			return False
	if trace(mat)!=cons:
		return False
	return trace(rot90(mat))==cons



##########################################################
if __name__=='__main__':
	pass

