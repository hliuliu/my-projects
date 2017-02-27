

def abserror(tval,appval):
	'''
	Purpose:
		returns the absolute error between the true value tval and the approximate value appval.
		the return value is always a float
	Preconditions:
		tval and appval are of type int,float,or long
	Examples:
		abserror(3.001,3) ==> 0.001
		abserror(1.45,1.5) ==> 0.05
		abserror(10,11) ==> 1.0
		abserror(2,-4.0) ==> 6.0
		abserror(1.2,1.2) ==> 0.0
	'''
	for i in (tval,appval):
		if type(i) not in [int,long,float]:
			raise TypeError
	return float(abs(tval-appval))


def relerror(tval,appval):
	'''
	Purpose:
		returns the relative error between the true value tval and the approximate value appval.
		the return value is always a float
	Preconditions:
		tval and appval are of type int,float,or long
		tval is nonzero
	Examples:
		relerror(3.001,3) ==> 0.000333222259246881
		relerror(1.45,1.5) ==> 0.03448275862068969
		relerror(10,11) ==> 0.1
		relerror(2,-4.0) ==> 3.0
		relerror(1.2,1.2) ==> 0.0
	'''
	for i in (tval,appval):
		if type(i) not in [int,long,float]:
			raise TypeError
	return abserror(tval,appval)/tval

def numsigfigs(tval,appval):
	for i in (tval,appval):
		if type(i) not in [int,long,float]:
			raise TypeError
	r=relerror(tval,appval)
	n,er=1,0.5
	while r<er:
		n+=1
		er/=10.0
		er=round(er,n)
	return n-1

def laginterp(*args):
	from calculus import polynomial
	f=polynomial()
	for k,(x,y) in enumerate(args):
		p=polynomial({0:1})
		q=1
		for i,j in args[:k]+args[k+1:]:
			p*=polynomial({1:1,0:-i})
			q*=(x-i)
		p*=y
		p/=float(q)
		f+=p
	return f

def bisection(f,xl,xr,numit=1):
	for i in (xl,xr):
		if type(i) not in [int,float,long]:
			raise TypeError
	if xl>xr or f(xl)*f(xr)>0:
		raise ValueError('Bad initial guesses!!')
	roots=[]
	from calculus import approx
	for i in range(numit):
		xm=(xl+xr)/2.0
		if approx(xm,round(xm,5)):
			xm=round(xm,5)
		if xm==int(xm):
			xm=int(xm)
		roots.append(xm)
		fl,fr=f(xl),f(xr)
		fm=f(xm)
		if approx(fm,0):
			return roots
		if fl*fm<=0:
			xr=xm
		else:
			xl=xm
	return roots

def fixedpoint(f,x0,numit=1):
	if type(x0) not in [int,long,float]:
		raise TypeError
	apps=[]
	from calculus import approx
	for i in range(numit):
		x1=f(x0)
		apps.append(x1)
		if approx(x0,x1):
			return apps
		x0=x1
	return apps

def horner(pol,x0):
	from calculus import polynomial as poly,unpackcoefs
	if not isinstance(pol,poly) or type(x0) not in [int,float,long]:
		raise TypeError
	if not pol:
		return ([0],[0])
	n=pol.degree()
	pcoefs=unpackcoefs(pol,True)
	b=[pcoefs[-1]]
	for i in range(n):
		b.insert(0,b[0]*x0+pcoefs[n-i-1])
	if not n:
		return (b,[0])
	c=[b[-1]]
	for i in range(n-1):
		c.insert(0,c[0]*x0+b[n-i-1])
	return (b,c)

def hornernewton(pol,x0,maxit=1):
	from calculus import polynomial as poly,unpackcoefs,approx
	if not isinstance(pol,poly) or type(x0) not in [int,float,long]:
		raise TypeError
	app=[x0]
	for i in range(maxit):
		b0,c1=[i[0] for i in horner(pol,x0)]
		if approx(b0,0):
			return app
		x0-=float(b0)/c1
		if approx(x0,round(x0,5)):
			x0=round(x0,5)
		if x0==int(x0):
			x0=int(x0)
		app.append(x0)
	return app


########################################################
if __name__=='__main__':
	pass