
from algebra import matrix as _matrix, det as _det
from vector import vector as _vect, projonto as _ponto
from calculus import approx as _approx, inf as _inf, sin as _sin, cos as _cos
from math import sqrt as _sqrt




class shape(object):
	def __new__(cls):
		obj=super(shape,cls).__new__(cls)
		return obj
	def area(self):
		return 0
	def perimeter(self):
		return 0
	def __contains__(self,sh):
		if not isinstance(sh,shape):
			return False
		return sh==self
	def rotate(self,rad,about=None):
		if about==None:
			about=self.center()
		if not isinstance(about,point):
			raise TypeError
		return about
	def intersect(self,other):
		return None
	def reflectx(self):
		return self
	def reflecty(self):
		return self
	def center(self):
		return self
	def spin(self,rad,num,about=None):
		if about==None:
			about=self.center()
		if not isinstance(about,point):
			raise TypeError
		res=[self]
		rad=float(rad)/num
		for i in xrange(num):
			self=self.rotate(rad,about)
			res.append(self)
		return res
	def translate(self,dx,dy):
		return self+point(dx,dy)

class point(shape):
	def __new__(cls,x=0,y=0):
		ptcoords=[]
		for i in (x,y):
			if type(i) not in [int,float,long]:
				raise TypeError
			if type(i)==float:
				if _approx(i,round(i,10)):
					i=round(i,10)
				if i==int(i):
					i=int(i)
			ptcoords.append(i)
		obj=super(point,cls).__new__(cls)
		x,y=ptcoords
		obj.__xy=_vect(x,y)
		return obj
	def tovector(self):
		return self.__xy.subvector()
	def xcoord(self):
		return self.__xy.get(0)
	def ycoord(self):
		return self.__xy.get(1)
	def __repr__(self):
		return 'point'+str(self)
	def __str__(self):
		return str(self.__xy)
	def __eq__(self,other):
		if not isinstance(other,point):
			return False
		return self.__xy==other.__xy
	def __ne__(self,other):
		return not (self==other)
	def __nonzero__(self):
		return self!=point()
	def __add__(self,other):
		if not isinstance(other,point):
			raise TypeError
		return point(*((self.__xy+other.__xy).tolist()))
	def __neg__(self):
		return point(*((-self.__xy).tolist()))
	def __sub__(self,other):
		return self+(-other)
	def __mul__(self,other):
		if type(other) not in [int,long,float]:
			raise TypeError
		return point(*((self.__xy*other).tolist()))
	def __div__(self,other):
		return self*(1.0/other)
	def transpose(self):
		return point(self.ycoord(),self.xcoord())
	def reflectx(self):
		return point(-self.xcoord(),self.ycoord())
	def reflecty(self):
		return point(self.xcoord(),-self.ycoord())
	def __rotate_about_orig(self,rad):
		rotmat=_matrix([[_cos(rad),-_sin(rad)],[_sin(rad),_cos(rad)]])
		p=_matrix([self.__xy.tolist()]).transpose()
		p=rotmat*p
		return point(p.get(0,0),p.get(1,0))
	def rotate(self,rad,about=None):
		about=super(point,self).rotate(rad,about)
		return (self-about).__rotate_about_orig(rad)+about
	def __lt__(self,other):
		if not isinstance(other,point):
			return NotImplemented
		if self.xcoord()==other.xcoord():
			return self.ycoord()<other.ycoord()
		return self.xcoord()<other.xcoord()
	def __le__(self,other):
		return self<other or self==other
	def __gt__(self,other):
		if not isinstance(other,point):
			return NotImplemented
		return other<self
	def __ge__(self,other):
		return self>other or self==other
	def __intersectpoint(self,other):
		if self==other:
			return self
		return None
	def intersect(self,other):
		if other==None:
			return None
		if not isinstance(other,shape):
			raise TypeError
		if isinstance(other,point):
			return self.__intersectpoint(other)
		return other.intersect(self)
	


def pointdirection(p0,p1,p2):
	'''
	Purpose:
		To rotate from line passing through points p0,p2 to line passing through points p0,p1 with an angle<180 degrees
		about (centered at) the point p0, determing which direction is this rotation.
		returns 'clockwise','counterclockwise',or 'straight', depending on the result.
	Preconditions:
		p0,p1,p2 are instances of point
	Examples:
		pointdirection((0,0),(1,2),(2,7)) ==> 'clockwise'
		pointdirection((1,0),(1,2),(4,7)) ==> 'counterclockwise'
		pointdirection((4,5),(6,8),(0,-1)) ==> 'straight'
	'''
	for i in (p0,p1,p2):
		if not isinstance(i,point):
			raise TypeError
	crs=_matrix([(p1-p0).tovector().tolist(),(p2-p0).tovector().tolist()])
	d=_det(crs)
	if d>0:
		return 'clockwise'
	if d<0:
		return 'counterclockwise'
	return 'straight'


def randlatpt(a,b):
	'''
	Purpose:
		returns a random lattice point (x,y), where x,y in [a,b].
	Preconditions:
		a and b are of type int
	'''
	import random
	return point(random.randint(a,b),random.randint(a,b))

def distptfromorig(pt):
	'''
	Purpose:
		returns the Euclidean distance of point pt from the origin.
	Preconditions:
		pt is an instance of point
	Examples:
		distptfromorig((3,4)) ==> 5
		distptfromorig((-7,24)) ==> 25
		distptfromorig((0,138)) ==> 138
	'''
	if not isinstance(pt,point):
		raise TypeError
	return pt.tovector().length()

def distpts(pt1,pt2):
	for i in (pt1,pt2):
		if not isinstance(i,point):
			raise TypeError
	return distptfromorig(pt1-pt2)

def closestptpair(*args):
	for i in args:
		if not isinstance(i,point):
			raise TypeError
	if len(args)<2:
		return
	pxs=sorted(args)
	pys=[j.transpose() for j in sorted([i.transpose() for i in args])]
	def clpair(pxs,pys):
		if len(pxs)==2:
			return tuple(pxs)
		if len(pxs)==3:
			p1,p2,p3=pxs
			d12=distpts(p1,p2)
			d13=distpts(p1,p3)
			d23=distpts(p2,p3)
			if d12<=d13:
				if d12<=d23:
					return (p1,p2)
				return (p2,p3)
			if d13<=d23:
				return (p1,p3)
			return (p2,p3)
		pxl=pxs[:len(pxs)/2]
		pxr=pxs[len(pxs)/2:]
		pyl,pyr=[],[]
		xm=pxl[-1].xcoord()
		for y in pys:
			if y<=pxl[-1]:
				pyl.append(y)
			else:
				pyr.append(y)
		cpl=clpair(pxl,pyl)
		cpr=clpair(pxr,pyr)
		cp=cpl
		if distpts(*cpr)<distpts(*cp):
			cp=cpr
		d=distpts(*cp)
		yd=[i for i in pys if abs(i.xcoord()-xm)<=d]
		for i in range(len(yd)-1):
			for j in range(i+1,min(i+8,len(yd))):
				if distpts(yd[i],yd[j])<d:
					d=distpts(yd[i],yd[j])
					cp=(yd[i],yd[j])
		return cp
	return clpair(pxs,pys)



####################################### beginning of line class ########################################################################

class line(shape):
	def __new__(cls,p0,p1):
		for i in (p0,p1):
			if not isinstance(i,point):
				raise TypeError
		if p0==p1:
			return p0
		if p0>p1:
			p0,p1=p1,p0
		obj=super(line,cls).__new__(cls)
		obj.__p0,obj.__p1=p0,p1
		dif=p1-p0
		p0x,p0y=p0.tovector().tolist()
		p1x,p1y=p1.tovector().tolist()
		if _approx(p0x,p1x):
			p0=point(p0x,0)
			p1=point(p0x,1)
			slope=_inf
		else:
			slope=dif.ycoord()/float(dif.xcoord())
			if _approx(slope,round(slope,10)):
				slope=round(slope,10)
			ny=slope*p0x
			p0=point(0,p0y-ny)
			p1=point(1,p0.ycoord()+slope)
		obj.__p0norm,obj.__p1norm=p0,p1
		obj.__slope=slope
		obj.__strval='(x,y) = %s + t*%s '%(p0,p1-p0)
		return obj
	def slope(self):
		return self.__slope
	def vertical(self):
		return self.slope()==_inf
	def endpoints(self):
		return (self.__p0,self.__p1)
	def horrizontal(self):
		return self.slope()==0
	def __str__(self):
		return self.__strval
	def __repr__(self):
		return 'line(point%s,point%s)'%self.endpoints()
	def length(self):
		return _inf
	def perimeter(self):
		return self.length()
	def __contains__(self,other):
		if isinstance(other,point):
			p0,p1,p2=sorted(self.endpoints()+(other,))
			return pointdirection(p0,p1,p2)=='straight'
		if isinstance(other,line):
			p0,p1=other.endpoints()
			return p0 in self and p1 in self
		return False
	def __intersectpoint(self,pt):
		if pt in self:
			return pt
		return None
	def __intersectline(self,other):
		if self.slope()==other.slope():
			if self in other:
				return self
			if other in self:
				return other
			if (self.__p0 not in other) and (self.__p1 not in other):
				return None
			p0,p1,p2,p3=sorted(self.endpoints()+other.endpoints())
			return line(p1,p2)
		def solveline(l):
			if l.vertical():
				return (1,0,l.endpoints()[0].xcoord())
			b=-1
			p0,p1=l.endpoints()
			x0,y0=p0.tovector().tolist()
			x1,y1=p1.tovector().tolist()
			mat=_matrix([[x0,-1],[x1,-1]])
			mat1=_matrix([[y0,-1],[y1,-1]])
			mat2=_matrix([[x0,y0],[x1,y1]])
			d=_det(mat)
			a=float(_det(mat1))/d
			c=float(_det(mat2))/d
			return (a,b,c)
		a1,b1,c1=solveline(self)
		a2,b2,c2=solveline(other)
		mat=_matrix([[a1,b1],[a2,b2]])
		mat1=_matrix([[c1,b1],[c2,b2]])
		mat2=_matrix([[a1,c1],[a2,c2]])
		d=_det(mat)
		x=float(_det(mat1))/d
		y=float(_det(mat2))/d
		p=point(x,y)
		return p
	def intersect(self,other):
		if other==None:
			return None
		if not isinstance(other,shape):
			raise TypeError
		if isinstance(other,point):
			return self.__intersectpoint(other)
		if isinstance(other,line):
			return self.__intersectline(other)
		return other.intersect(self)
	def rotate(self,rad,about=None):
		p0,p1=self.endpoints()
		about=super(point,self.center()).rotate(rad,about)
		return line(p0.rotate(rad,about),p1.rotate(rad,about))
	def reflectx(self):
		p0,p1=self.endpoints()
		return line(p0.reflectx(),p1.reflectx())
	def reflecty(self):
		p0,p1=self.endpoints()
		return line(p0.reflectx(),p1.reflecty())
	def midpoint(self):
		p0,p1=self.endpoints()
		return (p0+p1)/2
	def __eq__(self,other):
		if type(other)!=line:
			return False
		for p in self.endpoints():
			if p not in other:
				return False
		return True
	def __neg__(self):
		p0,p1=self.endpoints()
		return line(-p0,-p1)
	def __ne__(self,other):
		return not (self==other)
	def __lt__(self,other):
		if type(other)!=line:
			return NotImplemented
		if self.slope()!=other.slope():
			return self.slope()<other.slope()
		return self.__p0norm<other.__p0norm
	def __le__(self,other):
		return (self<other) or (self==other)
	def __gt__(self,other):
		if not type(other)!=line:
			return NotImplemented
		return other<self
	def __ge__(self,other):
		return (self>other) or (self==other)
	def transpose(self):
		p0,p1=self.endpoints()
		return line(p0.transpose(),p1.transpose())
	def ycoord(self,x,ext=True):
		if type(x) not in [int,float,long]:
			raise TypeError
		if self.vertical():
			if x==self.__p0.xcoord():
				if ext:
					return (-_inf,_inf)
				return (self.__p0.ycoord(),self.__p1.ycoord())
			return None
		if ext:
			p0,p1=self.endpoints()
			m=self.slope()
			b=p0.ycoord()-m*p0.xcoord()
			ans=m*x+b
			if type(ans) in [int,long]:
				return ans
			if _approx(ans,round(ans,10)):
				ans=round(ans,10)
			if ans==int(ans):
				ans=int(ans)
			return ans
		res=self.ycoord(x,True)
		p0,p1=self.endpoints()
		x0,x1=map(lambda p: p.xcoord(), [p0,p1])
		if x0<=x<=x1:
			return res
		return None
	def xcoord(self,y,ext=True):
		return self.transpose().ycoord(y,ext)
	def center(self):
		return self.midpoint()
	def translate(self,dx,dy):
		dp=point(dx,dy)
		p0,p1=self.endpoints()
		return line(p0+dp,p1+dp)
	def as_segment(self):
		return line_segment(*(self.endpoints()))
	def asline(self):
		return self

####################################### end of line class ########################################################################



class line_segment(line):
	def __new__(cls,p0,p1):
		obj=super(line_segment,cls).__new__(cls,p0,p1)
		return obj
	def asline(self):
		return line(*(self.endpoints()))
	def __contains__(self,other):
		if other not in self.asline():
			return False
		if isinstance(other,point):
			p0,p1=self.endpoints()
			return p0<=other<=p1
		if isinstance(other,line_segment):
			p0,p1=self.endpoints()
			p2,p3=other.endpoints()
			return p2 in self and p3 in self
		return False
	def __str__(self):
		return repr(self)
	def __repr__(self):
		return 'line_segment(point%s,point%s)'%self.endpoints()
	def length(self):
		return distpts(*(self.endpoints()))
	def intersect(self,other):
		other=self.asline().intersect(other)
		if other==None or isinstance(other,point):
			return other
		if type(other)==line:
			return self
		if isinstance(other,line_segment):
			p0,p1=self.endpoints()
			p2,p3=other.endpoints()
			if p1<p2 or p3<p0:
				return None
			p0,p1,p2,p3=sorted([p0,p1,p2,p3])
			return line_segment(p1,p2)
		return other.intersect(self)
	def rotate(self,rad,about=None):
		return super(line_segment,self).rotate(rad,about).as_segment()
	def reflectx(self):
		return super(line_segment,self).reflectx().as_segment()
	def reflecty(self):
		return super(line_segment,self).reflecty().as_segment()
	def split(self,n=2):
		p0,p1=self.endpoints()
		dp=p1-p0
		dp/=n
		cur=p0
		res=[]
		for i in xrange(n):
			res.append(line_segment(cur,cur+dp))
			cur+=dp
		return res
	def __eq__(self,other):
		if not isinstance(other,line_segment):
			return False
		return self.endpoints()==other.endpoints()
	def __ne__(self,other):
		return not self==other
	def __lt__(self,other):
		if not isinstance(other,line_segment):
			return NotImplemented
		return self.endpoints()<other.endpoints()
	def __gt__(self,other):
		if not isinstance(other,line_segment):
			return NotImplemented
		return other<self
	def __le__(self,other):
		return self<other or self==other
	def __ge__(self,other):
		return self>other or self==other
	def __neg__(self,other):
		p0,p1=self.endpoints()
		return line_segment(-p0,-p1)
	def transpose(self):
		return super(line_segment,self).transpose().as_segment()
	def xcoord(self,x,ext=False):
		return super(line_segment,self).xcoord(x,ext)
	def ycoord(self,y,ext=False):
		return super(line_segment,self).ycoord(y,ext)
	def translate(self,dx,dy):
		return super(line_segment,self).translate(dx,dy).as_segment()



def closestptonline(pt,l):
	if not isinstance(pt,point) or not isinstance(l,line):
		raise TypeError
	p0,p1=l.endpoints()
	u=(p1-p0).tovector()
	v=(pt-p0).tovector()
	pvu=point(*(_ponto(v,u).tolist()))+p0
	if pvu in l:
		return pvu
	if pvu>p1:
		return p1
	return p0

def closestptslines(l1,l2):
	if not isinstance(l1,line) or not isinstance(l2,line):
		raise TypeError
	res=l1.intersect(l2)
	rev=False
	if isinstance(res,point):
		return (res,res)
	if isinstance(res,line):
		return (res.endpoints()[0],)*2
	if type(l1)==type(l2)==line:
		p0,p1=l1.endpoints()
		return (p0,closestptonline(p0,l2))
	if type(l1)==line:
		l1,l2=l2,l1
		rev=True
	p0,p1,p2,p3=l1.endpoints()+l2.endpoints()
	curp=(p0,closestptonline(p0,l2))
	minp=curp
	curp=(p1,closestptonline(p1,l2))
	if distpts(*minp)>distpts(*curp):
		minp=curp
	if isinstance(l2,line_segment):
		curp=(closestptonline(p2,l1),p2)
		if distpts(*minp)>distpts(*curp):
			minp=curp
		curp=(closestptonline(p3,l1),p3)
		if distpts(*minp)>distpts(*curp):
			minp=curp
	return (lambda x: (x[1],x[0]) if rev else x) (minp)


def shortestdistlines(l1,l2):
	return distpts(*closetptslines(l1,l2))

def paralines(l1,l2):
	if not isinstance(l1,line) or not isinstance(l2,line):
		raise TypeError
	return l1.slope()==l2.slope()

def perplines(l1,l2):
	if not isinstance(l1,line) or not isinstance(l2,line):
		raise TypeError
	l1,l2=sorted([l1,l2],key=lambda(l):l.slope())
	if l1.horrizontal() and l2.vertical():
		return True
	if l1.horrizontal():
		return False
	return _approx(l2.slope(),-1.0/l1.slope())

class triangle(shape):
 	def __new__(cls,p0,p1,p2):
 		for i in (p0,p1,p2):
 			if not isinstance(i,point):
 				raise TypeError
 		p0,p1,p2=sorted((p0,p1,p2))
 		if p1 in [p0,p2]:
 			return line_segment(p0,p2)
 		obj=super(triangle,cls).__new__(cls)
 		obj.__p0=p0
 		obj.__p1=p1
 		obj.__p2=p2
 		obj.__p01,obj.__p02,obj.__p12=(line_segment(p0,p1),line_segment(p0,p2),line_segment(p1,p2))
 		return obj
 	def vertices(self):
 		return self.__p0,self.__p1,self.__p2
 	def __str__(self):
 		return str(tuple([str(i) for i in self.vertices()]))
 	def __repr__(self):
 		return 'triangle'+str(self)
 	def edges(self):
 		return self.__p01,self.__p02,self.__p12
 	def perimeter(self):
 		e0,e1,e2=self.edges()
 		return e0.length()+e1.length()+e2.length()
 	def area(self):
 		e0,e1,e2=self.edges()
 		s=self.perimeter()/2.0
 		if _approx(s,round(s,10)):
 			s=round(s,10)
 		if s==int(s):
 			s=int(s)
 		ans=_sqrt(s*(s-e0.length())*(s-e1.length())*(s-e2.length()))
 		if _approx(ans,round(ans,10)):
 			ans=round(ans,10)
 		if ans==int(ans):
 			ans=int(ans)
 		return ans
 	def isisoceles(self):
 		e=self.edges()
 		l0,l1,l2=sorted([i.length() for i in e])
 		return l1 in [l0,l2]
 	def isequilateral(self):
 		e=self.edges()
 		l0,l1,l2=sorted([i.length() for i in e])
 		return l0==l2
 	def rotate(self,rad,about=None):
 		about=super(point,self.center()).rotate(rad,about)
 		p0,p1,p2=self.vertices()
 		p0=p0.rotate(rad,about)
 		p1=p1.rotate(rad,about)
 		p2=p2.rotate(rad,about)
 		return triangle(p0,p1,p2)
 	def center(self):
 		p0,p1,p2=self.vertices()
 		return (p0+p1+p2)/3
 	centroid=center
 	def orthocenter(self):
 		p0,p1,p2=self.vertices()
 		p01,p02,p12=self.edges()
 		l1=line(p0,closestptonline(p0,p12))
 		l2=line(p1,closestptonline(p1,p02))
 		return l1.intersect(l2)
 	def circumradius(self):
 		e0,e1,e2=self.edges()
 		k=self.area()
 		ans=e0.length()*e1.length()*e2.length()
 		ans=float(ans)
 		ans/=4
 		if _approx(ans,round(ans,10)):
 			ans=round(ans,10)
 		ans/=k
 		if _approx(ans,round(ans,10)):
 			ans=round(ans,10)
 		if ans==int(ans):
 			ans=int(ans)
 		return ans
 	def __contains__(self,other):
 		if isinstance(other,point):
 			p0,p1,p2=self.vertices()
 			p01,p02,p12=self.edges()
 			if p0.xcoord()>other.xcoord():
 				return False
 			if p2.xcoord()<other.xcoord():
 				return False
 			for i in [p01,p12,p02]:
 				if other in i:
 					return True
 			if p01.vertical():
 				y0=p02.ycoord(other.xcoord())
 				y1=p12.ycoord(other.xcoord())
 				return y0<=other.ycoord()<=y1
 			if p12.vertical():
 				y1=p01.ycoord(other.xcoord())
 				y2=p02.ycoord(other.xcoord())
 				return y1<=other.ycoord()<=y2
 			y01,y02,y12=map(lambda l: l.asline().ycoord(other.xcoord()), [p01,p02,p12])
 			c01,c02,c12=map(lambda y: point(other.xcoord(),y), [y01,y02,y12])
 			bounds=[(c,y,p) for c,y,p in zip([c01,c02,c12],[y01,y02,y12],[p01,p02,p12]) if c in p]
 			if len(bounds)<2:
 				return False
 			bounds.sort(key=lambda k: k[1])
 			[_,ymin,_],[_,ymax,_]=bounds[0],bounds[-1]
 			return ymin<=other.ycoord()<=ymax
 		if isinstance(other,line_segment):
 			return [i in self for i in other.endpoints()]==[True]*2
 		if isinstance(other,triangle):
 			return [i in self for i in other.vertices()]==[True]*3
 		return False
 	def __eq__(self,other):
 		if not isinstance(other,triangle):
 			return False
 		return self.vertices()==other.vertices()
 	def __ne__(self,other):
		return not (self==other)
	def __lt__(self,other):
		if not isinstance(other,triangle):
			return NotImplemented
		return self.vertices()<other.vertices()
	def __gt__(self,other):
		if not isinstance(other,triangle):
			return NotImplemented
		return other<self
	def __le__(self,other):
		return self<other or self==other
	def __ge__(self,other):
		return self>other or self==other
	def __intersectpoint(self,pt):
		if pt in self:
			return pt
		return None
	def __intersectline(self,l):
		endpts=[]
		for i in self.edges():
			endpts.append(i.intersect(l))
		while None in endpts:
			endpts.remove(None)
		if not endpts:
			return None
		if len(endpts)==1:
			return endpts[0]
		if line_segment in map(type, endpts):
			return endpts[map(type,endpts).index(line_segment)]
		endpts.sort()
		return line_segment(endpts[0],endpts[-1])
	def __intersectlineseg(self,ls):
		lsnew=self.__intersectline(ls.asline())
		if lsnew==None:
			return None
		return ls.intersect(lsnew)
	def __intersecttriangle(self,tr):
		raise NotImplementedError
	def intersect(self,other):
		if other==None:
			return None
		if not isinstance(other,shape):
			raise TypeError
		if isinstance(other,point):
			return self.__intersectpoint(other)
		if isinstance(other,line_segment):
			return self.__intersectlineseg(other)
		if isinstance(other,line):
			return self.__intersectline(other)
		if isinstance(other,triangle):
			return self.__intersecttriangle(other)
		return other.intersect(self)





