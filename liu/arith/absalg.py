'''

absalg module

For computations performed using abstract algebra. 
For example: groups, permutations, rings, etc.

The field module supports various operations on fields.

'''


from algebra import lcm as _lcm



class permutation(object):
	def __new__(cls,fxs,xs=None,n=None):
		if xs==None:
			pairs=True
			fxslist=[]
			fxs=iter(fxs)
			for f in fxs:
				try:
					fxslist.append(f)
					k,v=f
				except:
					pairs=False
					break
			if pairs:
				fxs,xs=[],[]
				for k,v in fxslist:
					fxs.append(v)
					xs.append(k)
			else:
				for f in fxs:
					fxslist.append(f)
				fxs,xs=fxslist,range(len(fxslist))
		xs=list(xs)
		fxs=list(fxs)
		if len(xs)!=len(fxs):
			raise ValueError
		xscopy=list(xs)
		found=[]
		for f in fxs:
			if f in found:
				raise ValueError
			found.append(f)
			i=xscopy.index(f)
			if i>=0:
				xscopy.pop(i)
			else:
				raise ValueError
		if n==None:
			n=len(xs)
		if type(n) not in [int,long]:
			raise TypeError
		if n<len(xs):
			n=len(xs)
		permfn=range(n)
		for i,f in enumerate(fxs):
			permfn[i]=xs.index(f)
		obj=super(permutation,cls).__new__(cls)
		obj.__permfn=permfn
		return obj
	def __iter__(self):
		for i in self.__permfn:
			yield i
	def __len__(self):
		return len(self.__permfn)
	def isidentity(self):
		for i,j in enumerate(self):
			if i!=j:
				return False
		return True
	def inverse(self):
		piinv=range(len(self))
		for i,j in enumerate(self):
			piinv[j]=i
		return permutation(piinv)
	def __repr__(self):
		return 'permutation(%s)'%list(self)
	def __str__(self):
		return '[ '+', '.join(['%d -> %d'%(i,j) for i,j in enumerate(self)])+' ]'
	def get(self,x):
		if type(x) not in [int,long]:
			raise TypeError
		if not 0<=x<len(self):
			raise ValueError
		return self.__permfn[x]
	def __eq__(self,other):
		if not isinstance(other,permutation):
			return False
		return list(self)==list(other)
	def __ne__(self,other):
		return not self==other
	def __lt__(self,other):
		if not isinstance(other,permutation):
			return NotImplemented
		if len(self)!=len(other):
			return len(self)<len(other)
		return list(self)<list(other)
	def __gt__(self,other):
		if not isinstance(other,permutation):
			return NotImplemented
		return other<self
	def __le__(self,other):
		return self<other or self==other
	def __ge__(self,other):
		return self>other or self==other
	def orbit(self,x):
		orb=[x]
		x0=x
		x=self.get(x)
		while x!=x0:
			orb.append(x)
			x=self.get(x)
		return tuple(orb)
	def cycles(self,rem_singletons=False):
		unused=set(range(len(self)))
		cyc=set()
		while unused:
			m=min(unused)
			morb=self.orbit(m)
			for i in morb:
				unused.discard(i)
			if not rem_singletons or len(morb)>1:
				cyc.add(morb)
		return cyc
	def order(self):
		ans=1
		for c in self.cycles(True):
			ans=_lcm(ans,len(c))
		return ans
	def __mul__(self,other):
		ol=list(other)
		olcopy=list(ol)
		for i,j in enumerate(self):
			olcopy[i]=ol[j]
		if isinstance(other,permutation):
			return permutation(olcopy)
		return olcopy
	def __div__(self,other):
		if not isinstance(other,permutation):
			raise TypeError
		return self*other.inverse()
	def change_length(self,n):
		if n==len(self):
			return permutation(list(self))
		if n>len(self):
			p=list(self)+range(len(self),n)
			return permutation(p)
		start=n
		curr=start
		while curr<len(self):
			if start>self.get(curr):
				raise ValueError
			curr+=1
		return permutation(list(self)[:start])





perm=permutation



def cycle_perm(*args):
	'''
	Purpose:
		Returns an instance of permutation based on the cycle implied by args.
		This is precisely the permutation (args[0], args[1], ..., args[k-1])
			as expressed in cycle notation, where k=len(args).
		The number of elements being permutated (the 'n' parameter or the length the the returned permutation)
			is n=max(args)+1 if args is not empty else 0
	Preconditions:
		For i=0,1,2,...,len(args)-1:
			type(args[i])==int
			args[i]>=0
		args[i]!=args[j] whenever i!=j
	Examples:
		cycle_perm(0,1) ==> permutation([0->1, 1->0])
		cycle_perm(1,4,3) ==> permutation([0->0, 1->4, 2->2, 3->1, 4->3])
	'''
	if not args:
		return permutation([])
	for a in args:
		if type(a)!=int:
			raise TypeError
		if a<0:
			raise ValueError
	shifted_args=args[1:]+(args[0],)
	p=range(max(args)+1)
	for i,j in zip(args,shifted_args):
		p[i]=j
	return permutation(p)







