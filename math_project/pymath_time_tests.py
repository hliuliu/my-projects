
from time import time
from pymath.number_theory import isprime,factorization
from pymath import integer



def time_test_1():
	print '%s()'%time_test_1.__name__
	n=289
	print 'calling isprime(%d):'%n,
	start=time()
	print isprime(n)
	end=time()
	print 'time taken:',end-start
	n=465
	print 'calling isprime(%d):'%n,
	start=time()
	print isprime(n)
	end=time()
	print 'time taken:',end-start
	n=571
	print 'calling isprime(%d):'%n,
	start=time()
	print isprime(n)
	end=time()
	print 'time taken:',end-start
	n=1579
	print 'calling isprime(%d):'%n,
	start=time()
	print isprime(n)
	end=time()
	print 'time taken:',end-start
	n=15203
	print 'calling isprime(%d):'%n,
	start=time()
	print isprime(n)
	end=time()
	print 'time taken:',end-start
	n=2**17-1
	print 'calling isprime(%d):'%n,
	start=time()
	print isprime(n)
	end=time()
	print 'time taken:',end-start
	n=2**20-7
	print 'calling isprime(%d):'%n,
	start=time()
	print isprime(n)
	end=time()
	print 'time taken:',end-start



def time_test_2():
	print '%s()'%time_test_2.__name__
	n=3
	print 'calling factorization(%d):'%n,
	start=time()
	print factorization(n)
	end=time()
	print 'time taken:',end-start
	n=12
	print 'calling factorization(%d):'%n,
	start=time()
	print factorization(n)
	end=time()
	print 'time taken:',end-start
	n=121*40
	print 'calling factorization(%d):'%n,
	start=time()
	print factorization(n)
	end=time()
	print 'time taken:',end-start


def time_test_3():
	print '%s()'%time_test_3.__name__
	a=integer('1274487746697236426')
	b=integer('5878799963469')
	print 'computing %s*%s:'%(a,b),
	start=time()
	print a*b
	end=time()
	print 'time taken:',end-start
	a=integer('1274487746697236481')
	b=integer('58787999634696454')
	print 'computing %s*%s:'%(a,b),
	start=time()
	print a*b
	end=time()
	print 'time taken:',end-start
	a=integer('1274487746697236481')
	b=integer('58787999634696454555')
	print 'computing %s*%s:'%(a,b),
	start=time()
	print a*b
	end=time()
	print 'time taken:',end-start
	a=integer('1274487746697236481'*2)
	b=integer('58787999634696454')
	print 'computing %s*%s:'%(a,b),
	start=time()
	print a*b
	end=time()
	print 'time taken:',end-start
	a=integer('1274487746697236481'*3)
	b=integer('58787999634696454')
	print 'computing %s*%s:'%(a,b),
	start=time()
	print a*b
	end=time()
	print 'time taken:',end-start
	a=integer('1274487746697236481'*3)
	b=integer('58787999634696454118'*2)
	print 'computing %s*%s:'%(a,b),
	start=time()
	print a*b
	end=time()
	print 'time taken:',end-start
	a=integer('1274487746697236481'*3)
	b=integer('58787999634696454118'*5)
	print 'computing %s*%s:'%(a,b),
	start=time()
	print a*b
	end=time()
	print 'time taken:',end-start
	a=integer('1274487746697236481'*10)
	b=integer('58787999634696454118'*4)
	print 'computing %s*%s:'%(a,b),
	start=time()
	print a*b
	end=time()
	print 'time taken:',end-start
	a=integer('1274487746697236489'*50)
	b=integer('587879996346964541187714100'*20)
	print 'computing %s*%s:'%(a,b),
	start=time()
	print a*b
	end=time()
	print 'time taken:',end-start


def time_test_4():
	print '%s()'%time_test_4.__name__
	a=integer('1276426')
	b=integer('2')
	print 'computing %s//%s:'%(a,b),
	start=time()
	print a//b
	end=time()
	print 'time taken:',end-start
	a=integer('12764267844691111')
	b=integer('2')
	print 'computing %s//%s:'%(a,b),
	start=time()
	print a//b
	end=time()
	print 'time taken:',end-start
	a=integer('127647999474699134799255698')
	b=integer('2')
	print 'computing %s//%s:'%(a,b),
	start=time()
	print a//b
	end=time()
	print 'time taken:',end-start
	a=integer('127647999474699134799255698'*3)
	b=integer('2')
	print 'computing %s//%s:'%(a,b),
	start=time()
	print a//b
	end=time()
	print 'time taken:',end-start
	a=integer('127647999474699134799255698'*10)
	b=integer('2')
	print 'computing %s//%s:'%(a,b),
	start=time()
	print a//b
	end=time()
	print 'time taken:',end-start
	a=integer('127647999474699134799255698'*50)
	b=integer('2')
	print 'computing %s//%s:'%(a,b),
	start=time()
	print a//b
	end=time()
	print 'time taken:',end-start
	a=integer('127647999474699134799255698')
	b=integer('21245641')
	print 'computing %s//%s:'%(a,b),
	start=time()
	print a//b
	end=time()
	print 'time taken:',end-start
	a=integer('127647999474699134799255698'*20)
	b=integer('21245641598763')
	print 'computing %s//%s:'%(a,b),
	start=time()
	print a//b
	end=time()
	print 'time taken:',end-start
	a=integer('127647999474699134799255698'*20)
	b=integer('21245641598763'*10)
	print 'computing %s//%s:'%(a,b),
	start=time()
	print a//b
	end=time()
	print 'time taken:',end-start


def time_test_5():
	print '%s()'%time_test_5.__name__
	a=integer(13)
	b=2
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=3
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=5
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=8
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=10
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=14
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=17
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=20
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=25
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=30
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=40
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=50
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=60
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=75
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=100
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=200
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=300
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=500
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	b=700
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	a*=a
	b=350
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start
	a=integer(13)
	print 'computing %s**%s:'%(a,b),
	start=time()
	a=a**b
	print a
	end=time()
	print 'time taken:',end-start
	b=2
	print 'computing %s**%s:'%(a,b),
	start=time()
	print a**b
	end=time()
	print 'time taken:',end-start







# time_test_1()
# print
# time_test_2()
# print
# time_test_3()

time_test_4()
print

#time_test_5()



