

class graph(object):
	'''
	A class to instantiate an undirected graph
	'''
	def __init__(self,nodes=[],edges=[]):
		self.__nodes=[]
		self.__adjmat=[]
		for u in nodes:
			self.insertnode(u)
		for u,v in edges:
			self.insertedge(u,v)
	def insertnode(self,x):
		from copy import deepcopy
		if x not in self.__nodes:
			self.__nodes.append(deepcopy(x))
			for i in self.__adjmat:
				i.append(False)
			self.__adjmat.append([False]*len(self.__nodes))
	def __contains__(self,x):
		return x in self.__nodes
	def hasedge(self,u,v):
		for w in [u,v]:
			if w not in self:
				return False
		i=self.__nodes.index(u)
		j=self.__nodes.index(v)
		return self.__adjmat[i][j]
	def insertedge(self,u,v):
		for i in [u,v]:
			if i not in self:
				raise ValueError
		if u==v:
			return
		u=self.__nodes.index(u)
		v=self.__nodes.index(v)
		self.__adjmat[u][v]=True
		self.__adjmat[v][u]=True
	def nodelist(self):
		from copy import deepcopy
		return deepcopy(self.__nodes)
	def __orientedge(self,e):
		u,v=e
		if v<u:
			u,v=v,u
		return (u,v)
	def edgelist(self):
		from copy import deepcopy
		res=[]
		for i in range(len(self.__nodes)):
			for j in range(i):
				if self.__adjmat[i][j]:
					res.append(self.__orientedge((deepcopy(self.__nodes[i]),deepcopy(self.__nodes[j]))))
		return res
	def adjmatrix(self):
		return [[j for j in i] for i in self.__adjmat]
	def deletenode(self,x):
		if x not in self:
			return
		pos=self.__nodes.index(x)
		self.__adjmat.pop(pos)
		for i in self.__adjmat:
			i.pop(pos)
		self.__nodes.pop(pos)
	def deleteedge(self,u,v):
		for w in [u,v]:
			if w not in self:
				raise ValueError
		i=self.__nodes.index(u)
		j=self.__nodes.index(v)
		self.__adjmat[i][j]=False
		self.__adjmat[j][i]=False
	def numnodes(self):
		return len(self.nodelist())
	def numedges(self):
		return len(self.edgelist())
	def incidentedges(self,x):
		if x not in self:
			raise ValueError
		i=self.__nodes.index(x)
		res=[]
		from copy import deepcopy
		for j,k in zip(self.__nodes,self.__adjmat[i]):
			if k:
				res.append(self.__orientedge((deepcopy(x),deepcopy(j))))
		return res
	def degree(self,x):
		return len(self.incidentedges(x))
	def degreeseq(self):
		ds=[]
		for s in self.__nodes:
			ds.append(self.degree(s))
		ds.sort(reverse=True)
		return ds
	def iscomplete(self):
		n=self.numnodes()
		return self.degreeseq()==[n-1]*n
	def incidentnodes(self,x):
		res=[]
		for i,j in self.incidentedges(x):
			if i==x:
				res.append(j)
			else:
				res.append(i)
		return res
	def componentof(self,x):
		if x not in self:
			raise ValueError
		g=graph([x])
		from stkque import queue
		q=queue()
		q.enqueue(x)
		while q:
			x=q.dequeue()
			for y in self.incidentnodes(x):
				if y not in g:
					q.enqueue(y)
					g.insertnode(y)
				g.insertedge(x,y)
		return g
	def components(self):
		nodes=list(self.__nodes)
		res=[]
		while nodes:
			res.append(self.componentof(nodes[0]))
			for i in res[-1].nodelist():
				nodes.remove(i)
		if not res:
			res=[graph()]
		return res
	def __repr__(self):
		return 'graph(%s,%s)'%(self.__nodes,self.edgelist())
	def __eq__(self,other):
		return issubgraph(self,other) and issubgraph(other,self)
	def __iter__(self):
		from copy import deepcopy
		for i in self.__nodes:
			yield deepcopy(i)
	def connected(self):
		return len(self.components())==1
	def acyclic(self):
		if self==graph():
			return True
		comps=self.components()
		if len(comps)==1:
			return self.numedges()+1==self.numnodes()
		for c in comps:
			if not c.acyclic():
				return False
		return True
	def relabel(self,x,y):
		if x not in self:
			raise ValueError
		i=self.__nodes.index(x)
		self.__nodes[i]=y
	def bfs(self,start):
		if start not in self:
			raise ValueError
		from stkque import queue
		q=queue()
		visited=[start]
		trav=[start]
		q.enqueue(start)
		while q:
			trav.append([])
			start=q.dequeue()
			for i in self.incidentnodes(start):
				if i not in visited:
					q.enqueue(i)
					visited.append(i)
					trav[-1].append(i)
		return trav
	def bft(self,start):
		trav=self.bfs(start)
		from stkque import queue
		q=queue()
		q.enqueue(start)
		trav.pop(0)
		g=graph([start])
		for i in trav:
			el=q.dequeue()
			for j in i:
				q.enqueue(j)
				g.insertnode(j)
				g.insertedge(el,j)
		return g
	def dfs(self,start):
		if start not in self:
			raise ValueError
		def recdfs(this,start,visited):
			visited.append(start)
			for i in this.incidentnodes(start):
				if i not in visited:
					recdfs(this,i,visited)
			return visited
		return recdfs(self,start,[])
	def dft(self,start):
		if start not in self:
			raise ValueError
		g=graph()
		def dftrec(this,g,start):
			g.insertnode(start)
			for i in g.incidentnodes():
				if i not in g:
					dftrec(this,g,i)
					g.insertedge(start,i)
			
		dftrec(self,g,start)
		return g
	def isbipartite(self):
		if self.numnodes()==0:
			return True
		red,blue=[],[]
		nodelist=list(self.__nodes)
		node=nodelist[0]
		from stkque import queue
		q=queue()
		red.append(node)
		while nodelist:
			q.enqueue(nodelist.pop(0))
			while q:
				node=q.dequeue()
				inred= node in red
				for i in self.incidentnodes(node):
					if i not in red+blue:
						q.enqueue(i)
						if inred:
							blue.append(i)
						else:
							red.append(i)
						nodelist.remove(i)
						continue
					if inred and (i in red):
						return False
					if not inred and (i in blue):
						return False
		return True
	def traversable(self):
		if not self.connected():
			return False
		odd=[i for i in self.degreeseq() if i%2]
		return len(odd) in [0,2]
	def eulerian(self):
		if not self.traversable():
			return False
		for i in self.degreeseq():
			if i%2:
				return False
		return True
	def haspath(self,x,y):
		if x not in self or y not in self:
			raise ValueError
		from stkque import queue
		q=queue()
		q.enqueue(x)
		visited=[x]
		while q:
			x=q.dequeue()
			if x==y:
				return True
			for i in x.incidentnodes():
				if i not in visited:
					q.enqueue(i)
					visited.append(i)
		return False
	def isregular(self):
		'''
		Purpose:
			returns whether of not the instance, self, is a regular graph.
			a graph is regular if the degree of every node is the same.
		Preconditions:
			none
		Examples:
			graph().isregular() -> True
			graph([1,2,3]).isregular() -> True
			graph([1,2,3,4],[(1,2),(3,4)]).isregular() -> True
			graph([1,2,3,4,5],[(1,2),(1,3),(2,4),(3,5)]).isregular() -> False
		'''
		from algs import identical
		return identical(self.degreeseq())
	def union(self,other):
		'''
		Purpose:
			returns the union of self and other.
			the union of two graphs, G and H, is U,
			where U is the graph with node list G.nodelist()+H.nodelist(),
			and edge list G.edgelist()+H.edgelist(), but not necessarily in that order.
			to avoid node name collision, every node v in G is replaced with (v,1)
			and v in H with (v,2).
		Preconditions:
			other is an instance of graph. i.e. isinstance(other,graph) returns True
		Examples:
			graph().union(graph()) -> graph()
			graph([1,2]).union(graph()) -> graph([(1,1),(2,1)])
			graph().union(graph([1,2])) -> graph([(1,2),(2,2)])
			graph([1,2],[(1,2)]).union(graph([1,3,4],[(1,3),(3,4)])) 
				-> graph([(1,1),(2,1),(1,2),(3,2),(3,2)],
					[((1,1),(2,1)),((1,2),(3,2)),((3,2),(4,2))]
					)
		'''
		if not isinstance(other,graph):
			raise TypeError
		u=graph()
		for i in self:
			u.insertnode((i,1))
		for i in other:
			u.insertnode((i,2))
		for x,y in self.edgelist():
			u.insertedge((x,1),(y,1))
		for x,y in other.edgelist():
			u.insertedge((x,2),(y,2))
		return u
	def join(self,other):
		'''
		Purpose:
			returns the join of self and other.
			the join of two graphs, G and H, is J,
			where J is the union of G and H with additional edges, every (u,v) which satisfy 
			u in G and v in H.
		Preconditions:
			other is an instance of graph. i.e. isinstance(other,graph) returns True
		Examples:
			graph().join(graph()) -> graph()
			graph([1,2]).join(graph()) -> graph([(1,1),(2,1)])
			graph().join(graph([1,2])) -> graph([(1,2),(2,2)])
			graph([1,2]).join(graph([3,4],[(3,4)])) 
				-> graph([(1,1),(2,1),(3,2),(4,2)],
					[((3,2),(4,2)),((1,1),(3,2)),((1,1),(4,2)),((2,1),(3,2)),((2,1),(4,2))]
					)
		'''
		ans=self.union(other)
		for i in self:
			for j in other:
				ans.insertedge((i,1),(j,2))
		return ans



class hashgraph(graph):
	def __init__(self,nodes=set(),edges=set()):
		self.__adjmat={}
		for i in nodes:
			self.insertnode(i)
		for u,v in edges:
			self.insertedge(u,v)
	def insertnode(self,x):
		if x not in self:
			self.__adjmat[x]=set()
	def __contains__(self,x):
		return x in self.__adjmat
	def __orientedge(self,e):
		u,v=e
		if v<u:
			u,v=v,u
		return (u,v)
	def insertedge(self,x,y):
		for i in [x,y]:
			if i not in self:
				raise ValueError
		if x!=y:
			self.__adjmat[x].add(y)
			self.__adjmat[y].add(x)
	def hasedge(self,x,y):
		for i in [x,y]:
			if i not in self:
				return False
		return y in self.__adjmat[x]
	def nodeset(self):
		return set(self.__adjmat)
	def nodelist(self):
		return list(self.nodeset())
	def edgeset(self):
		edges=set()
		for i in self.__adjmat:
			for j in self.__adjmat[i]:
				edges.add(self.__orientedge(i,j))
		return edges
	def edgelist(self):
		return list(self.edgeset())
	def adjmatrix(self):
		return {i:{k:k in j for k in self.__adjmat} for i,j in self.__adjmat.items()}
	def deletenode(self,x):
		if x in self:
			for i in self.__adjmat[x]:
				self.__adjmat[i].discard(x)
			del self.__adjmat[x]
	def deleteedge(self,x,y):
		for i in [x,y]:
			if i not in self:
				raise ValueError
		self.__adjmat[x].discard(y)
		self.__adjmat[y].discard(x)
	def numnodes(self):
		return len(self.__adjmat)
	def numedges(self):
		m=0
		for i,j in self.__adjmat.items():
			m+=len(j)
		return m/2
	def incidentedges(self,x):
		if x not in self:
			raise ValueError
		edges=set()
		for i in self.__adjmat[x]:
			edges.add(self.__orientedge(x,i))
		return edges
	def incidentnodes(self,x):
		if x not in self:
			raise ValueError
		return set(self.__adjmat[x])
	def degreeseq(self):
		self.__nodes=self.__adjmat
		ds=super(hashgraph,self).degreeseq()
		del self.__nodes
		return ds



def samplenode(g):
	if not isinstance(g,graph):
		raise TypeError
	nl=g.nodelist()
	import random
	index=random.randrange(len(nl))
	return nl[index]



def complete(*nodes):
	c=graph(nodes)
	nl=c.nodelist()
	for i in nl:
		for j in nl:
			if i!=j:
				c.insertedge(i,j)
	return c

def complement(g):
	if not isinstance(g,graph):
		raise TypeError
	c=complete(*(g.nodelist()))
	for i,j in g.edgelist():
		c.deleteedge(i,j)
	return c

def cycle(*nodes):
	if not nodes:
		return graph()
	g=graph(nodes)
	for i,j in zip(nodes,nodes[1:]+(nodes[0],)):
		g.insertedge(i,j)
	return g

def issubgraph(g,h):
	for i in [g,h]:
		if not isinstance(i,graph):
			raise TypeError
	for i in g.nodelist():
		if i not in h:
			return False
	el=h.edgelist()
	for i in g.edgelist():
		if i not in el:
			return False
	return True

def path(*nodes):
	if not nodes:
		return graph()
	c=cycle(*nodes)
	c.deleteedge(nodes[0],nodes[-1])
	return c


def istree(g):
	if not isinstance(g,graph):
		raise TypeError
	return g.connected() and g.acyclic()


def graphical(seq):
	'''
	Purpose:
		returns whether or not the sequence, seq, is graphical.
		a sequence is graphical is it is the degree sequence of some graph.
	Preconditions:
		seq is a collection containing only nonnegative ints.
	Examples:
		graphical([1,1]) -> True
		graphical([2,3,1,2]) -> True
		graphical([5,4,1,6]) -> False
		graphical([2,2,3,2,1,1,4,0]) -> False
	'''
	for i in seq:
		if type(i)!=int:
			raise TypeError
	seq=sorted(seq,reverse=True)
	while seq:
		parity=0
		for i in seq:
			parity^=(i & 1)
		if parity:
			return False
		maxdeg=seq.pop(0)
		if not maxdeg:
			return True
		while seq and not seq[-1]:
			seq.pop()
		if maxdeg>len(seq):
			return False
		for i in xrange(maxdeg):
			seq[i]-=1
		posl=maxdeg-1
		if maxdeg<len(seq) and seq[posl]<seq[maxdeg]:
			while posl>0 and seq[posl]==seq[posl-1]:
				posl-=1
			posr=maxdeg
			while posr<len(seq)-1 and seq[posr]==seq[posr+1]:
				posr+=1
			temp=seq[maxdeg]
			seq[maxdeg:posr+1]=[seq[posl]]*(maxdeg-posl)
			seq[posl:maxdeg]=[temp]*(posr-maxdeg+1)
	return True




class disjointset(object):
	class __node:
		def __init__(self,value,parent,rank):
			self.value=value
			self.parent=parent
			self.rank=rank
	def __init__(self):
		self.__nodes={}
	def makeset(self,x):
		if x in self.__nodes:
			return
		self.__nodes[x]=(self.__node(x,x,0))
	def findset(self,x):
		if x!=self.__nodes[x].parent:
			self.__nodes[x].parent=self.findset(self.__nodes[x].parent)
		return self.__nodes[x].parent
	def __link(self,x,y):
		if self.__nodes[x].rank>self.__nodes[y].rank:
			self.__nodes[y].parent=x
		else:
			self.__nodes[x].parent=y
		if self.__nodes[x].rank==self.__nodes[y].rank:
			self.__nodes[y].rank+=1
	def union(self,x,y):
		f=self.findset
		x,y=f(x),f(y)
		if x!=y:
			self.__link(x,y)

##########################################################
if __name__=='__main__':
	pass