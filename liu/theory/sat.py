

def xor(a,b):
	if a and (not b):
		return a
	if b and (not a):
		return b
	if a and b:
		return False
	return b

class cnf(object):
	def __init__(self,*args):
		self.__clauses=[]
		for i in args:
			self.addclause(i)
	def addclause(self,cl):
		for i in cl:
			if type(i)!=int:
				raise TypeError
			if i==0:
				raise ValueError('0 cannot be a propositional variable since it cannot be negated')
		self.__clauses.append(list(cl))
	def __iter__(self):
		return (list(i) for i in self.__clauses)
	def clauses(self):
		return list(self)
	def getclause(self,pos):
		return list(self.__clauses[pos])
	def __len__(self):
		return len(self.__clauses)
	def variables(self):
		var=set()
		for i in self:
			for j in i:
				var.add(abs(j))
		return var
	def delclause(self,cl):
		if type(cl)==int:
			del self.__clauses[cl]
		else:
			cl=list(cl)
			if cl in self:
				self.__clauses.remove(cl)
	def __contains__(self,cl):
		return cl in self.__clauses
	def delallclause(self,cl):
		cl=list(cl)
		while cl in self:
			self.delclause(cl)
	def __eq__(self,other):
		if not isinstance(other,sat):
			return False
		ol=list(other)
		for i in self:
			if i in ol:
				ol.remove(i)
			else:
				return False
		return ol==[]
	def solve(self,sol):
		if type(sol)!=dict:
			raise TypeError
		for v in self.variables():
			if v not in sol:
				raise ValueError('solution incomplete. missing variable %d'%v)
		def solvevar(sol,var):
			if var>0:
				return sol[var]
			return not sol[-var]
		def solveclause(sol,cl):
			for i in cl:
				if solvevar(sol,i):
					return True
			return False
		for i in self:
			if not solveclause(sol,i):
				return False
		return True
	def __repr__(self):
		s='cnf'
		s+='('+','.join([str(i) for i in self])+')'
		return s
	def __str__(self):
		return ' and '.join(
			['( '+' or '.join(
				[str(j) if j>0 else '( not '+str(-j)+' )' for j in i]
				)+' )' for i in self]
			)
	def solvepart(self,sol):
		if type(sol)!=dict:
			raise TypeError
		cl=self.clauses()
		for i in list(cl):
			for j in list(i):
				if abs(j) not in sol:
					continue
				val=sol[abs(j)]
				if j<0:
					val=not val
				if val:
					cl.remove(i)
					break
				else:
					i.remove(j)
		if cl==[]:
			return True
		if [] in cl:
			return False
		return cnf(*cl)
	def __nonzero__(self):
		return [] not in self
	def __and__(self,other):
		if not self and not isinstance(other,cnf):
			return self
		if not isinstance(other,cnf):
			return other
		return cnf(*(self.clauses()+other.clauses()))
	def __or__(self,other):
		if self and not isinstance(other,cnf):
			return self
		if not isinstance(other,cnf):
			return other
		cl=[]
		for i in self.clauses():
			for j in other.clauses():
				cl.append(list(i)+list(j))
		return cnf(*cl)
	def simplified(self):
		cl=self.clauses()
		if cl==[]:
			return True
		if [] in cl:
			return False
		cl=[list(set(i)) for i in cl]
		change=True
		while change:
			change=False
			cl.sort(key=lambda(x):len(x))
			rem=[]
			for i,j in enumerate(cl):
				for k in j:
					if -k in j:
						rem.insert(0,i)
						change=True
						break
				k=i+1
				for l in list(cl[i+1:]):
					if set(j).issubset(set(l)):
						del cl[k]
						k-=1
						change=True
					k+=1
			for i in rem:
				del cl[i]
			for i in cnf(*cl).variables():
				for j in cl:
					if i not in j:
						continue
					for k in cl:
						if -i in k and (set(j)-{i})==(set(k)-{-i}):
							j.remove(i)
							k.remove(-i)
							change=True
							break
			for i in cl:
				if len(i)==1:
					i,=i
					for j in cl:
						if -i in j:
							j.remove(-i)
							change=True
		if cl==[]:
			return True
		if [] in cl:
			return False
		return cnf(*cl)
	def satisfiable(self):
		this=self.simplified()
		if type(this)==bool:
			return this
		var=this.variables().pop()
		s1=this.solvepart({var:True})
		s2=this.solvepart({var:False})
		if (not s1) and (not s2):
			return False
		if isinstance(s1,cnf):
			s1=s1.satisfiable()
		if isinstance(s2,cnf):
			s2=s2.satisfiable()
		return s1 or s2
	def literals(self):
		lit=set()
		for i in self:
			for j in i:
				lit.add(j)
		return lit



def loadcnf(fname):
	form=[]
	with open(fname,'r') as fh:
		for line in fh:
			line=line.strip()
			form.append([int(i) for i in line.split()])
	return cnf(*form)


