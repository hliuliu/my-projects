



class bst(object):
	def __init__(self):
		self.__parent=None
		self.__root=None
		self.__left,self.__right=None,None
	def __len__(self):
		if self.__root==None:
			return 0
		return len(self.__left)+len(self.__right)
	def insert(self,x):
		if x==None or self.__root==x:
			return
		if self.__root==None:
			self.__root=x
			self.__left,self.__right=bst(),bst()
			self.__left.__parent=self
			self.__right.__parent=self
		elif x>self.__root:
			self.__right.insert(x)
		else:
			self.__left.insert(x)
	def isempty(self):
		return self.__root==None
	def __find(self,x):
		if self.isempty() or x==None:
			return None
		if self.__root==x:
			return self
		if self.__root<x:
			return self.__right.__find(x)
		return self.__left.__find(x)
	def __contains__(self,x):
		return self.__find(x)!=None
	def preorder(self):
		if self.isempty():
			return []
		return [self.__root]+self.__left.preorder()+self.__right.preorder()
	def postorder(self):
		if self.isempty():
			return []
		return self.__left.postorder()+self.__right.postorder()+[self.__root]
	def inorder(self):
		if self.isempty():
			return []
		return self.__left.inorder()+[self.__root]+self.__right.inorder()
	def levelorder(self):
		from stkque import queue
		q=queue()
		res=[]
		q.enqueue(self)
		for i in q:
			if not i.isempty():
				res.append(i.__root)
				q.enqueue(i.__left)
				q.enqueue(i.__right)
		return res
	def __repr__(self):
		def replist(this):
			if this.isempty():
				return []
			ans=[None,this.__root,None]
			ans[0]=replist(this.__left)
			ans[2]=replist(this.__right)
			return ans
		return str(replist(self))
	def __str__(self):
		def treestr(this,indent):
			if this.isempty():
				return ''
			res=treestr(this.__right,indent+3)
			res+=' '*indent+str(this.__root)+'\n'
			res+=treestr(this.__left,indent+3)
			return res
		return treestr(self,0)
	def getmin(self):
		if self.isempty():
			return None
		if self.__left.isempty():
			return self.__root
		return self.__left.getmin()
	def getmax(self):
		if self.isempty():
			return None
		if self.__right.isempty():
			return self.__root
		return self.__right.getmax()
	def height(self):
		if self.isempty():
			return 0
		l=self.__left.height()
		r=self.__right.height()
		return 1+(r if r>l else l)
	def __iter__(self):
		return iter(self.inorder())
	def remove(self,x):
		subt=self.__find(x)
		if subt==None:
			raise ValueError('%s is not in the tree'%repr(s))
		if len(subt)==1:
			subt.__root=None
			subt.__left=None
			subt.__right=None
		elif subt.__left.__root==None:
			p=subt.__parent
			if p==None:
				self.__root=self.__right.__root
				self.__left=self.__right.__left
				self.__right=self.__right.__right
				return
			if x<p.__root:
				p.__left=subt.__right
			else:
				p.__right=subt.__right
			subt.__right.__parent=p
		else:
			p=subt.__parent
			r=subt.__right
			if p==None:
				p=self.__left
				p.__parent=None
				while p.__root!=None:
					p=p.__right
				p.__parent.__right=r
				r.__parent=p.__parent
				self.__root=self.__left.__root
				self.__right=self.__left.__right
				self.__left=self.__left.__left
			else:
				if x<p.__root:
					p.__left=subt.__left
				else:
					p.__right=subt.__left
				subt.__left.__parent=p
				p=p.__left
				while p.__root!=None:
					p=p.__right
				p.__root=r.__root
				p.__left=r.__left
				p.__right=r.__right
				if p.__root!=None:
					p.__left.__parent=p
					p.__right.__parent=p


class heap(object):
	def __init__(self,minheap=True):
		self.__elements=[]
		self.__ismin=bool(minheap)
	def __len__(self):
		return len(self.__elements)
	def __nonzero__(self):
		return bool(self.__elements)
	def insert(self,item):
		from copy import deepcopy
		item=deepcopy(item)
		self.__elements.append(item)
		pos=len(self)-1
		while pos:
			if self.__ismin:
				if self.__elements[pos]<self.__elements[(pos-1)/2]:
					self.__elements[pos],self.__elements[(pos-1)/2]=self.__elements[(pos-1)/2],self.__elements[pos]
					pos-=1
					pos/=2
				else:
					return
			else:
				if self.__elements[pos]>self.__elements[(pos-1)/2]:
					self.__elements[pos],self.__elements[(pos-1)/2]=self.__elements[(pos-1)/2],self.__elements[pos]
					pos-=1
					pos/=2
				else:
					return
	def levelorder(self):
		from copy import deepcopy
		return deepcopy(self.__elements)
	def preorder(self):
		from copy import deepcopy
		def _preo(pos):
			if pos>=len(self):
				return []
			return [deepcopy(self.__elements[pos])]+_preo(2*pos+1)+_preo(2*pos+2)
		return _preo(0)
	def postorder(self):
		from copy import deepcopy
		def _posto(pos):
			if pos>=len(self):
				return []
			return _posto(2*pos+1)+_posto(2*pos+2)+[deepcopy(self.__elements[pos])]
		return _posto(0)
	def inorder(self):
		from copy import deepcopy
		def _ino(pos):
			if pos>=len(self):
				return []
			return _ino(2*pos+1)+[deepcopy(self.__elements[pos])]+_ino(2*pos+2)
		return _ino(0)
	def get(self):
		if not self:
			raise ValueError
		from copy import deepcopy
		item=deepcopy(self.__elements[0])
		self.__elements[0]=self.__elements[-1]
		del self.__elements[-1]
		pos=0
		while 2*pos<len(self)-1:
			left=2*pos+1
			right=left+1
			if right>=len(self):
				if self.__ismin:
					if self.__elements[pos]>self.__elements[left]:
						self.__elements[pos],self.__elements[left]=self.__elements[left],self.__elements[pos]
				else:
					if self.__elements[pos]<self.__elements[left]:
						self.__elements[pos],self.__elements[left]=self.__elements[left],self.__elements[pos]
				return item
			if self.__ismin:
				if self.__elements[left]<=self.__elements[right]:
					if self.__elements[pos]>self.__elements[left]:
						self.__elements[pos],self.__elements[left]=self.__elements[left],self.__elements[pos]
						pos=left
					else:
						return item
				else:
					if self.__elements[pos]>self.__elements[right]:
						self.__elements[pos],self.__elements[right]=self.__elements[right],self.__elements[pos]
						pos=right
					else:
						return item
			else:
				if self.__elements[left]>=self.__elements[right]:
					if self.__elements[pos]<self.__elements[left]:
						self.__elements[pos],self.__elements[left]=self.__elements[left],self.__elements[pos]
						pos=left
					else:
						return item
				else:
					if self.__elements[pos]<self.__elements[right]:
						self.__elements[pos],self.__elements[right]=self.__elements[right],self.__elements[pos]
						pos=right
					else:
						return item
		return item
	def __iter__(self):
		while self:
			yield self.get()





##########################################################
if __name__=='__main__':
	pass
	