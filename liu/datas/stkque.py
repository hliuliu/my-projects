

class _item(object):
	def __init__(self,val,prev=None,nxt=None):
		self.__val=val
		self.__prev=None
		self.__nxt=None
		self.setnext(nxt)
		self.setprev(prev)
	def getval(self):
		return self.__val
	def setval(self,val):
		self.__val=val
	def getprev(self):
		return self.__prev
	def getnext(self):
		return self.__nxt
	def setnext(self,nxt):
		self.__nxt=nxt
		if nxt==None:
			return
		if nxt.__prev!=None:
			nxt.__prev.__nxt=None
		nxt.__prev=self
	def setprev(self,prev):
		self.__prev=prev
		if prev==None:
			return
		if prev.__nxt!=None:
			prev.__nxt.__prev=None
		prev.__nxt=self

class queue(object):
	def __init__(self):
		self.__front=None
		self.__back=None
		self.__size=0
	def isempty(self):
		return self.__size==0
	def enqueue(self,val):
		import copy
		val=copy.deepcopy(val)
		if self.isempty():
			self.__front=_item(val)
			self.__back=self.__front
		else:
			self.__back=_item(val,self.__back)
		self.__size+=1
	def peek(self):
		if self.isempty():
			raise Exception('Queue is Empty')
		import copy
		return copy.deepcopy(self.__front.getval())
	def dequeue(self):
		res=self.peek()
		self.__front=self.__front.getnext()
		if self.__front==None:
			self.__back=None
		else:
			self.__front.setprev(None)
		self.__size-=1
		return res
	def __nonzero__(self):
		return not self.isempty()
	def __iter__(self):
		while self:
			yield self.dequeue()
	def __len__(self):
		return self.__size


class stack(object):
	def __init__(self):
		self.__size=0
		self.__top=None
	def isempty(self):
		return self.__size==0
	def __nonzero__(self):
		return not self.isempty()
	def push(self,val):
		import copy
		val=copy.deepcopy(val)
		self.__top=_item(val,None,self.__top)
		self.__size+=1
	def peek(self):
		if not self:
			raise Exception('Stack is Empty')
		import copy
		return copy.deepcopy(self.__top.getval())
	def pop(self):
		res=self.peek()
		self.__top=self.__top.getnext()
		if self.__top!=None:
			self.__top.setprev(None)
		self.__size-=1
		return res
	def __len__(self):
		return self.__size
	def __iter__(self):
		while self:
			yield self.pop()



################################################
if __name__=='__main__':
	pass
	s=stack()
	s.push(6)
	s.push(1)
	s.push(3)
	for i in [2123,'hello','randstuff',(3,4),['loooool','ok']]:
		s.push(i)
	print len(s)
	for i in s:
		print i
	print len(s)