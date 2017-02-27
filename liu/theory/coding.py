

class word(object):
	def __init__(self,bits):
		for b in bits:
			if b not in ['0','1']:
				raise ValueError ('Only the 0 or 1 character is allowed')
		self.__length=len(bits)
		self.__bits=str(bits)
	def __len__(self):
		return self.__length
	def __add__(self,other):
		if not isinstance(other,word):
			raise TypeError
		if len(self)!=len(other):
			raise ValueError
		res=''
		for i,j in zip(self.__bits,other.__bits):
			if i==j:
				res+='0'
			else:
				res+='1'
		return word(res)
	def __sub__(self,other):
		return self+other
	def __str__(self):
		return self.__bits
	def __repr__(self):
		return word.__name__+'(%s)'%repr(str(self))
	def __nonzero__(self):
		return '1' in str(self)
	def support(self):
		ans=[]
		for i,j in enumerate(str(self)):
			if j=='1':
				ans.append(i)
		return ans
	def weight(self):
		return len(self.support())
	def __eq__(self,other):
		if not isinstance(other,word):
			return False
		return not (self-other)
	def __ne__(self,other):
		return not self==other

def same_length(*args):
	if not args:
		return True
	if not isinstance(args[0],word):
		raise TypeError
	if len(args)==1:
		return True
	a1=args[:len(args)/2]
	a2=args[len(args)/2:]
	return len(a1[0])==len(a2[0]) and same_length(*a1)\
		and same_length(*a2)

def logand(*args):
	if not args or not same_length(*args):
		raise ValueError
	ans=''
	for i in zip(*[str(a) for a in args]):
		if '0' in i:
			ans+='0'
		else:
			ans+='1'
	return word(ans)

def logor(*args):
	if not args or not same_length(*args):
		raise ValueError
	ans=''
	for i in zip(*[str(a) for a in args]):
		if '1' in i:
			ans+='1'
		else:
			ans+='0'
	return word(ans)

def logxor(*args):
	if not args or not same_length(*args):
		raise ValueError
	if len(args)==1:
		return args[0]
	a1=args[:len(args)/2]
	a2=args[len(args)/2:]
	w1,w2=logxor(*a1),logxor(*a2)
	return w1+w2

def hamdist(u,v):
	for i in [u,v]:
		if not isinstance(i,word):
			raise TypeError
	return (u-v).weight()

def zeroword(n):
	return word('0'*n)

def allwords(n):
	if type(n) not in [int,long]:
		raise TypeError
	if n==0:
		return ['']
	if n%2:
		res=allwords(n-1)
		return [i+j for i in ['0','1'] for j in res]
	res=allwords(n/2)
	return [i+j for i in res for j in res]

def ball(r,u):
	if not isinstance(u,word):
		raise TypeError
	if type(r) not in [int,long]:
		raise TypeError
	if r<0:
		return []
	if r==0:
		return [u]
	if r==1:
		res=[u]
		for i in range(len(u)):
			s=list(str(u))
			s[i]={'0':'1','1':'0'}[s[i]]
			s=''.join(s)
			res.append(word(s))
		return res
	prev=ball(r-1,u)
	res=[i for i in prev if hamdist(i,u)==r-1]
	for i in res:
		ans=ball(1,i)
		for j in ans:
			if j not in prev:
				prev.append(j)
	return prev

def inverted(w):
	if not isinstance(w,word):
		raise TypeError
	return w+word('1'*len(w))

def leftshift(w,times=1):
	if not isinstance(w,word):
		raise TypeError
	if type(times) not in [int,long]:
		raise TypeError
	times%=len(w)
	if not times or not str(w):
		return word(str(w))
	shift=str(w)
	shift=word(shift[1:]+shift[0])
	return leftshift(shift,times-1)

def rightshift(w,times=1):
	if not isinstance(w,word):
		raise TypeError
	if type(times) not in [int,long]:
		raise TypeError
	times%=len(w)
	if not times or not str(w):
		return word(str(w))
	shift=str(w)
	shift=word(shift[-1]+shift[:-1])
	return rightshift(shift,times-1)

def shifts(w,drn='left'):
	if drn not in ['left','right']:
		raise ValueError('the direction must be left or right')
	if not isinstance(w,word):
		raise TypeError
	res=[]
	for i in range(len(w)):
		res.append(w)
		w=leftshift(w)
	if drn=='right':
		res.append(res.pop(0))
		res.reverse()
	return res

class code(object):
	def __init__(self,*args):
		for a in args:
			if not isinstance(a,word):
				raise TypeError
		if not same_length(*args):
			raise ValueError('arguments must be words of equal length')
		def remdup(args):
			r=[]
			for i in args:
				if i not in r:
					r.append(i)
			return tuple(r)
		args=remdup(args)
		self.__codewords=tuple(sorted(args,key=lambda(x):str(x)))
		self.__mindist=0
	def __len__(self):
		return len(self.__codewords)
	def __contains__(self,x):
		return x in self.__codewords
	def mindist(self):
		if not self.__mindist:
			if len(self)<=1:
				self.__mindist='infinity'
				return self.__mindist
			d=len(self.__codewords[0])
			for i in self:
				for j in self:
					if i!=j:
						h=hamdist(i,j)
						if h<d:
							d=h
			self.__mindist=d
		return self.__mindist
	def __iter__(self):
		for i in self.__codewords:
			yield i
	def detects(self,e):
		for u in self:
			if u+e in self:
				return False
		return True
	def corrects(self,e):
		for i in self:
			for j in self:
				if i!=j and hamdist(i+e,i)>=hamdist(i+e,j):
					return False
		return True
	def detcap(self):
		return self.mindist()-1
	def corrcap(self):
		return (self.mindist()-1)/2
	def wordlength(self):
		if not len(self):
			raise ValueError
		return len(self.__codewords[0])
	def codewords(self):
		return self.__codewords
	def __repr__(self):
		s='code('
		s+=','.join([repr(i) for i in self])
		s+=')'
		return s
	def __str__(self):
		return str([str(i) for i in self])
	def __eq__(self,other):
		if not isinstance(other,code):
			return False
		return self.codewords()==other.codewords()
	def __add__(self,other):
		if not isinstance(other,code):
			raise TypeError
		codes=[]
		for i in self:
			for j in other:
				codes.append(i+j)
		return code(*codes)
	def union(self,other):
		if not isinstance(other,code):
			raise TypeError
		codes=self.codewords()+other.codewords()
		return code(*codes)
	def intersect(self,other):
		if not isinstance(other,code):
			raise TypeError
		codes=[]
		for i in self:
			if i in other:
				codes.append(i)
		return code(*codes)
	def __sub__(self,other):
		if not isinstance(other,code):
			raise TypeError
		codes=[]
		for i in self:
			if i not in other:
				codes.append(i)
		return code(*codes)

def isperfect(c):
	if not isinstance(c,code):
		raise TypeError
	if len(c)==0:
		return False
	if len(c)==1:
		return True
	import os
	cwd=os.getcwd()
	os.chdir('..')
	from arith.algebra import comb
	os.chdir(cwd)
	n=c.wordlength()
	size=2**n
	ballsize=0
	for i in range(c.corrcap()+1):
		ballsize+=comb(n,i)
	if size%ballsize:
		return False
	return len(c)==size/ballsize

def translated(c,w):
	if not isinstance(c,code):
		raise TypeError
	if not isinstance(w,word):
		raise TypeError
	return code(*[i+w for i in c])

class lincode(code):
	def __init__(self,*args):
		self.__genmat=list(args)
		if not args:
			raise ValueError
		self.__rref(self.__genmat)
		self.__mindist=0
		self.__parcheck=None
		self.__haswts={0:True}
		if not self.__genmat:
			super(lincode,self).__init__(zeroword(len(args[0])))
		else:
			super(lincode,self).__init__(*self.__genmat)
	def __rref(self,mat):
		k=len(mat)
		if not k:
			return
		n=len(mat[0])
		if not n:
			while mat:
				mat.pop(0)
			return
		i,j=0,0
		pivs=[]
		#lor=logor(*mat)
		#slor=str(lor)
		while i<k and j<n:
			lor=logor(*mat[i:])
			slor=str(lor)
			while j<n and slor[j]=='0':
				j+=1
			if j==n:
				break
			while str(mat[i])[j]=='0':
				mat.append(mat.pop(i))
			row=i+1
			while row<k:
				if str(mat[row])[j]=='1':
					mat[row]-=mat[i]
				row+=1
			pivs.append((i,j))
			#print i,j
			#print '\n'.join([str(l) for l in mat])
			i+=1
			j+=1
			
		while mat and not mat[-1]:
			del mat[-1]
		if not mat:
			return
		for i,j in pivs:
			row=i-1
			while row>=0:
				if str(mat[row])[j]=='1':
					mat[row]-=mat[i]
				row-=1
	def __iter__(self):
		def matit(this,mat):
			if not mat:
				yield zeroword(self.wordlength())
			else:
				for i in matit(this,mat[:-1]):
					yield i
					yield i+mat[-1]
		for i in matit(self,self.__genmat):
			yield i
	def __len__(self):
		return 2**len(self.__genmat)
	def dimensions(self):
		return len(self.__genmat)
	def codewords(self):
		return tuple(iter(self))
	def __contains__(self,w):
		if not isinstance(w,word):
			return False
		if len(w)!=self.wordlength():
			return False
		if not w:
			return True
		for i in self.__genmat:
			pos1=0
			while str(i)[pos1]=='0':
				pos1+=1
			if str(w)[pos1]=='1':
				return w-i in self
		return False
	def genmat(self):
		return list(self.__genmat)
	def __repr__(self):
		s='lincode('
		s+=','.join([repr(i) for i in self.__genmat])
		s+=')'
		return s
	def __str__(self):
		return '\n'.join([str(i) for i in self.__genmat])+'\n'
	def mindist(self):
		if not self.__mindist:
			if not self.__genmat:
				self.__mindist='infinity'
				return self.__mindist
			if self.dimensions()==1:
				self.__mindist=self.__genmat[0].weight()
				return self.__mindist
			i=1
			while not self.haswt(i):
				i+=1
			self.__mindist=i
		return self.__mindist
	def parcheckmat(self):
		if self.__parcheck==None:
			pivs=[]
			freevars=range(self.wordlength())
			for i in self.__genmat:
				for j,j2 in enumerate(str(i)):
					if j2=='1':
						pivs.append(j)
						freevars.remove(j)
						break
			self.__parcheck=[]
			def getval(piv,free,gmat):
				i=pivs.index(piv)
				return str(gmat[i])[free]
			for i in freevars:
				s=''
				for j in range(self.wordlength()):
					if j==i:
						s+='1'
					elif j in pivs:
						s+=getval(j,i,self.__genmat)
					else:
						s+='0'
				self.__parcheck.append(word(s))
			#self.__rref(self.__parcheck)
		return list(self.__parcheck)
	def dual(self):
		return \
		lincode(*(self.parcheckmat()+[zeroword(self.wordlength())]))
	def __add__(self,other):
		if not isinstance(other,lincode):
			return super(lincode,self).__add__(other)
		return lincode(*(self.genmat()+other.genmat()+\
			[zeroword(self.wordlength())]))
	def __eq__(self,other):
		if not isinstance(other,code):
			return False
		if len(self)!=len(other):
			return False
		if isinstance(other,lincode):
			return self.genmat()==other.genmat()
		return super(lincode,self).__eq__(other)
	def haswt(self,wt):
		if type(wt) not in [int,long]:
			raise TypeError
		if wt<0:
			return False
		if wt in self.__haswts:
			return self.__haswts[wt]
		import os
		cwd=os.getcwd()
		os.chdir('..')
		from datas.algs import commonelements as cels
		os.chdir(cwd)
		del os
		def codelists(n):
			if n==1:
				for i in self.__genmat:
					self.__haswts[i.weight()]=True
				if 1 not in self.__haswts:
					self.__haswts[1]=False
				return [[i] for i in self.__genmat]
			if n%2:
				sub=codelists(n-1)
				res=[]
				for i in sub:
					for j in self.__genmat:
						if j not in i:
							i.append(j)
							res.append(i)
				for i in res:
					self.__haswts[logxor(*i)]=True
				if n not in self.__haswts:
					self.__haswts[n]=False
				return res
			sub=codelists(n/2)
			res=[]
			for i in list(sub):
				for j in list(sub):
					if not cels(i,j) and i+j not in res:
						res.append(i+j)
			for i in res:
				self.__haswts[logxor(*i)]=True
			if n not in self.__haswts:
				self.__haswts[n]=False
			return res
		codelists(wt)
		return self.__haswts[wt]

def fullcode(n):
	if type(n) not in [int,long]:
		raise TypeError
	if n==0:
		return lincode(word(''))
	base='1'+'0'*(n-1)
	base=word(base)
	base=shifts(base)
	return lincode(*base)

def hamming(r):
	if type(r) not in [int,long]:
		raise TypeError
	if r<0:
		raise ValueError('argument must be nonnegative')
	n=2**r-1
	par=fullcode(r)
	if not n:
		return par.dual()
	h=[]
	for i in range(r):
		h.append('')
	cols=iter(par)
	next(cols)
	for i in cols:
		for j, j2 in enumerate(str(i)):
			h[j]+=j2
	h=[word(i) for i in h]
	return lincode(*h).dual()

def extgolay():
	N=shifts(word('01011100010'))
	jn=[inverted(i) for i in N]
	b=['1'+str(i) for i in jn]
	b.insert(0,'0'+'1'*11)
	I=shifts(word('1'+'0'*11),'right')
	I=[str(i) for i in I]
	ib=[word(i+j) for i,j in zip(I,b)]
	return lincode(*ib)

def golay():
	g=extgolay().genmat()
	g=[str(i) for i in g]
	g=[word(i[:-1]) for i in g]
	return lincode(*g)

