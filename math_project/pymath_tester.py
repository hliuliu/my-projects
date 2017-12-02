
import pymath as pm


## Testing creation of integers

# zeroes in diffrent ways

zeroes_strings=[
	'0',
	'00000000',
	' 000 000 00',
	'  \t 0 \n 0 \n\t 0',
	'+0',
	'+ 0000 00',
	'  + \t 0000000',
	'- 00000 00',
	'-0',
	' -  0000 00  '
	]

for z in zeroes_strings:
	assert str(pm.integer(z))=='0'


# nonzero integers

nonzero_strings_pairs =[
	('21','21'), (' 2 1   ','21'), ('+21','21'),
	('+150','150'),('+000000150','150'),('+  00 0150','150'),
	('-32','-32'), ('-00000032','-32'),('-0000000 000 32','-32'),
	('-279','-279'),
	('0'*1000+'12','12'),('5'+'0'*700,'5'+'0'*700)
]

for test,result in nonzero_strings_pairs:
	assert str(pm.integer(test))==result

## testing integers as rings

assert pm.integer('0').lattice()==pm.integers
assert pm.integers.element_type()==pm.integer



## testing the signs of integers

for z in zeroes_strings:
	i=pm.integer(z)
	assert i.is_zero()
	assert not i.is_positive()
	assert not i.is_negative()

positive_strings=[
	'23', '180', '71', '+ 200093','+ 561 ', '1 000 008'
]

negative_strings=[
	'-13','- 104','-56322', '- 1000 00 24','- 781'
]

for p in positive_strings:
	i=pm.integer(p)
	assert not i.is_zero()
	assert i.is_positive()
	assert not i.is_negative()

for n in negative_strings:
	i=pm.integer(n)
	assert not i.is_zero()
	assert not i.is_positive()
	assert i.is_negative()


## testing the '-' (__neg__) operator for integers

int_neg_pairs=[
	('0','0'),
	('12','-12'),
	('-12','12'),
	('5784','-5784'),
	('246','-246'),
	('-410','410'),
	('12'+'89'*500,'-12'+'89'*500)
]

for p,np in int_neg_pairs:
	assert str(-pm.integer(p))==str(pm.integer(np))

## testing the '==' operator for integers

equal_cases=[
	(pm.integer('0'),pm.integer('0')),
	(pm.integer('10'),pm.integer('+10')),
	(pm.integer('25'),pm.integer('  +2 5 ')),
	(pm.integer('-30'),pm.integer('- 30')),
	(pm.integer('-0 54'),-pm.integer('54')),
	(pm.integer('0'),0),
	(pm.integer('+0000'),0),
	(pm.integer('10'),10),
	(pm.integer('25'),25),
	(pm.integer('-30'),-30),
	(pm.integer('-0 54'),-54)
]

for i,j in equal_cases:
	assert i==j and not i!=j


unequal_cases=[
	(pm.integer('0'),pm.integer('-2')),
	(pm.integer('10'),pm.integer('-10')),
	(pm.integer('25'),pm.integer('  +2 ')),
	(pm.integer('-30'),pm.integer('- 29')),
	(pm.integer('-0 54'),pm.integer('78')),
	(pm.integer('0'),15),
	(pm.integer('+0000'),293),
	(pm.integer('10'),11),
	(pm.integer('25'),-25),
	(pm.integer('-30'),30),
	(pm.integer('-0 54'),540)
]

for i,j in unequal_cases:
	assert not i==j and i!=j


## testing inequality operators on integers

gt_cases=[
	(pm.integer('0'),pm.integer('-7')),
	(pm.integer('26'),pm.integer('0')),
	(pm.integer('37'),pm.integer('-12')),
	(pm.integer('14'),pm.integer('-365')),
	(pm.integer('124'),pm.integer('115')),
	(pm.integer('2341'),pm.integer('1674')),
	(pm.integer('1'+'0'*1000),pm.integer('9'*1000))
]

for i,j in gt_cases:
	assert i>j and i>=j
	assert not i<j and not i<=j


lt_cases=[
	(pm.integer('-5'),pm.integer('0')),
	(pm.integer('0'),pm.integer('24')),
	(pm.integer('-10'),pm.integer('8')),
	(pm.integer('-23'),pm.integer('37')),
	(pm.integer('124'),pm.integer('135')),
	(pm.integer('2341'),pm.integer('3234'))
]

for i,j in lt_cases:
	assert not i>j and not i>=j
	assert i<j and i<=j

for i,j in equal_cases:
	assert not i>j and i>=j
	assert not i<j and i<=j


## testing the '+' operator

# adding 2 nonnegative integers

nonneg_add_triples=[
	(pm.integer('0'),pm.integer('0'),pm.integer('0')),
	(pm.integer('0'),pm.integer('15'),pm.integer('15')),
	(pm.integer('28'),pm.integer('0'),pm.integer('28')),
	(pm.integer('3'),pm.integer('2'),pm.integer('5')),
	(pm.integer('12'),pm.integer('6'),pm.integer('18')),
	(pm.integer('3'),pm.integer('7'),pm.integer('10')),
	(pm.integer('231'),pm.integer('568'),pm.integer('799')),
	(pm.integer('407'),pm.integer('685'),pm.integer('1092')),
	(pm.integer('265'),pm.integer('3'),pm.integer('268')),
	(pm.integer('3451'),pm.integer('76'),pm.integer('3527')),
	(pm.integer('9'*1000),pm.integer('1'),pm.integer('1'+'0'*1000))
]

for i,j,k in nonneg_add_triples:
	assert i+j==k


## testing the '-' operator

# subtracting 2 nonnegative integers

nonneg_subtract_triples=[
	(pm.integer('0'),pm.integer('0'),pm.integer('0')),
	(pm.integer('10'),pm.integer('10'),pm.integer('0')),
	(pm.integer('28'),pm.integer('0'),pm.integer('28')),
	(pm.integer('3'),pm.integer('2'),pm.integer('1')),
	(pm.integer('12'),pm.integer('6'),pm.integer('6')),
	(pm.integer('3'),pm.integer('7'),pm.integer('-4')),
	(pm.integer('231'),pm.integer('130'),pm.integer('101')),
	(pm.integer('407'),pm.integer('584'),pm.integer('-177')),
	(pm.integer('265'),pm.integer('3'),pm.integer('262')),
	(pm.integer('3451'),pm.integer('76'),pm.integer('3375')),
	(pm.integer('1'+'0'*1000),pm.integer('1'),pm.integer('9'*1000)),
	(pm.integer('23'),pm.integer('328'),pm.integer('-305'))
]

for i,j,k in nonneg_subtract_triples:
	assert i-j==k



## testing abs function on integers

test_abs_pairs=[
	(pm.integer('0'),pm.integer('0')),
	(pm.integer('12'),pm.integer('12')),
	(pm.integer('34418'),pm.integer('34418')),
	(pm.integer('-2'),pm.integer('2')),
	(pm.integer('-3527'),pm.integer('3527'))
]


for i,j in test_abs_pairs:
	assert abs(i)==j


## testing the boolean values of integers

boolean_value_str_pairs=[
	('0',False), ('1',True), ('5023',True), ('-7634',True), ('-19',True)
]


for i,j in boolean_value_str_pairs:
	if j:
		assert pm.integer(i)
	else:
		assert not pm.integer(i)


## testing the '*' operator

test_mult_triples=[
	(pm.integer('0'),pm.integer('0'),pm.integer('0')),
	(pm.integer('0'),pm.integer('3'),pm.integer('0')),
	(pm.integer('3'),pm.integer('0'),pm.integer('0')),
	(pm.integer('-2'),pm.integer('0'),pm.integer('0')),
	(pm.integer('0'),pm.integer('-2'),pm.integer('0')),
	(pm.integer('1'),pm.integer('1'),pm.integer('1')),
	(pm.integer('1'),pm.integer('28'),pm.integer('28')),
	(pm.integer('32'),pm.integer('1'),pm.integer('32')),
	(pm.integer('45'),pm.integer('-1'),pm.integer('-45')),
	(pm.integer('3'),pm.integer('2'),pm.integer('6')),
	(pm.integer('14'),pm.integer('12'),pm.integer('168')),
	(pm.integer('259'),pm.integer('37'),pm.integer('9583')),
	(pm.integer('37'),pm.integer('259'),pm.integer('9583')),
	(pm.integer('37'),pm.integer('-259'),pm.integer('-9583')),
	(pm.integer('-37'),pm.integer('259'),pm.integer('-9583')),
	(pm.integer('-37'),pm.integer('-259'),pm.integer('9583'))
]



for i,j,k in test_mult_triples:
	assert i*j==k


## testing the '//' operator

test_fdiv_triples=[
	(pm.integer('0'),pm.integer('1'),pm.integer('0')),
	(pm.integer('0'),pm.integer('5'),pm.integer('0')),
	(pm.integer('0'),pm.integer('-1'),pm.integer('0')),
	(pm.integer('0'),pm.integer('-12'),pm.integer('0')),
	(pm.integer('2'),pm.integer('1'),pm.integer('2')),
	(pm.integer('10'),pm.integer('2'),pm.integer('5')),
	(pm.integer('5'),pm.integer('1'),pm.integer('5')),
	(pm.integer('-3'),pm.integer('1'),pm.integer('-3')),
	(pm.integer('18'),pm.integer('1'),pm.integer('18')),
	(pm.integer('2945'),pm.integer('1'),pm.integer('2945')),
	(pm.integer('341'),pm.integer('1'),pm.integer('341')),
	(pm.integer('340'),pm.integer('1'),pm.integer('340')),
	(pm.integer('-341'),pm.integer('1'),pm.integer('-341')),
	(pm.integer('4'),pm.integer('2'),pm.integer('2')),
	(pm.integer('6'),pm.integer('2'),pm.integer('3')),
	(pm.integer('12'),pm.integer('3'),pm.integer('4')),
	(pm.integer('144'),pm.integer('24'),pm.integer('6')),
	(pm.integer('14424'),pm.integer('24'),pm.integer('601')),
	(pm.integer('749'),pm.integer('7'),pm.integer('107')),
	(pm.integer('67'),pm.integer('5'),pm.integer('13')),
	(pm.integer('28'),pm.integer('10'),pm.integer('2')),
	(pm.integer('150'),pm.integer('10'),pm.integer('15')),
	(pm.integer('16000'),pm.integer('200'),pm.integer('80')),
	(pm.integer('17'),pm.integer('2'),pm.integer('8')),
	(pm.integer('-144'),pm.integer('24'),pm.integer('-6')),
	(pm.integer('-1600'),pm.integer('-80'),pm.integer('20')),
	(pm.integer('-15'),pm.integer('4'),pm.integer('-4')),
	(pm.integer('1'+'0'*1000),pm.integer('1'+'0'*800),pm.integer('1'+'0'*200)),
	(pm.integer('87'),pm.integer('29'),pm.integer('3'))
]

for i,j,k in test_fdiv_triples:
	try:
		assert i//j==k
	except AssertionError:
		print i,j,k,i//j



## testing the modulo ('%') operator

test_mod_triples=[
	(pm.integer('0'),pm.integer('1'),pm.integer('0')),
	(pm.integer('0'),pm.integer('2'),pm.integer('0')),
	(pm.integer('0'),pm.integer('45'),pm.integer('0')),
	(pm.integer('0'),pm.integer('-36'),pm.integer('0')),
	(pm.integer('3'),pm.integer('4'),pm.integer('3')),
	(pm.integer('10'),pm.integer('24'),pm.integer('10')),
	(pm.integer('5'),pm.integer('1'),pm.integer('0')),
	(pm.integer('21'),pm.integer('7'),pm.integer('0')),
	(pm.integer('19'),pm.integer('9'),pm.integer('1')),
	(pm.integer('-2'),pm.integer('3'),pm.integer('1')),
	(pm.integer('35'),pm.integer('30'),pm.integer('5')),
	(pm.integer('23'),pm.integer('-35'),pm.integer('-12')),
	(pm.integer('2'),pm.integer('-34'),pm.integer('-32'))
]


for i,j,k in test_mod_triples:
	try:
		assert i%j==k
	except AssertionError:
		print i,j,k, i%j



## testing the ** operator (a**b) where a,b are integers and b>=0 

test_power_triples=[
	(pm.integer('0'),pm.integer('0'),pm.integer('1')),
	(pm.integer('0'),pm.integer('1'),pm.integer('0')),
	(pm.integer('0'),pm.integer('2'),pm.integer('0')),
	(pm.integer('0'),pm.integer('10'),pm.integer('0')),
	(pm.integer('1'),pm.integer('0'),pm.integer('1')),
	(pm.integer('1'),pm.integer('1'),pm.integer('1')),
	(pm.integer('1'),pm.integer('25'),pm.integer('1')),
	(pm.integer('2'),pm.integer('0'),pm.integer('1')),
	(pm.integer('2'),pm.integer('1'),pm.integer('2')),
	(pm.integer('2'),pm.integer('4'),pm.integer('16')),
	(pm.integer('2'),pm.integer('10'),pm.integer('1024')),
	(pm.integer('7'),pm.integer('3'),pm.integer('343')),
	(pm.integer('-7'),pm.integer('3'),pm.integer('-343')),
	(pm.integer('-2'),pm.integer('10'),pm.integer('1024')),
]


for i,j,k in test_power_triples:
	assert i**j==k



####### integer_tools ##############

itools=pm.integer_tools

## testing iter_digits


def eqiter(it1,it2):
	for i,j in zip(it1,it2):
		if not i==j:
			return False
	for i in it1:
		return False
	for i in it2:
		return False
	return True

'''
def xrange(n):
	i=0
	while i<n:
		yield i
		i+=1
assert eqiter(iter([0,1,2]),iter(xrange(3)))
'''


test_iter_digits_pairs=[
	(pm.integer('0'),iter([0])),
	(pm.integer('136'),iter([1,3,6])),
	(pm.integer('8548890'),iter([8,5,4,8,8,9,0])),
	(pm.integer('-32'),iter([-1,3,2])),
	(pm.integer('-92345'),iter([-1,9,2,3,4,5])),
]


for i,j in test_iter_digits_pairs:
	assert eqiter(itools.iter_digits(i),j)


## testing digits

test_digits_pairs=[
	(pm.integer('0'),[0]),
	(pm.integer('136'),[1,3,6]),
	(pm.integer('8548890'),[8,5,4,8,8,9,0]),
	(pm.integer('-32'),[-1,3,2]),
	(pm.integer('-92345'),[-1,9,2,3,4,5]),
]


for i,j in test_digits_pairs:
	try:
		assert itools.digits(i)==j
	except AssertionError:
		print i,j


## testing num_digits and sum_digits

test_num_digits_pairs=[
	(pm.integer('0'),pm.integer('1')),
	(pm.integer('125'),pm.integer('3')),
	(pm.integer('-93'),pm.integer('2')),
]

for i,j in test_num_digits_pairs:
	assert itools.num_digits(i)==j

test_sum_digits_pairs=[
	(pm.integer('0'),pm.integer('0')),
	(pm.integer('125'),pm.integer('8')),
	(pm.integer('876001'),pm.integer('22')),
	(pm.integer('-23'),pm.integer('5')),
	(pm.integer('-9421'),pm.integer('16')),
]

for i,j in test_sum_digits_pairs:
	assert itools.sum_digits(i)==j


## testing integer_xrange and integer_range

test_integer_x_range_pairs=[
	((pm.integer('5'),), range(5)),
	((pm.integer('16'),), range(16)),
	((pm.integer('1000'),), range(1000)),
	((pm.integer('-20'),),[]),
	((pm.integer('0'),), []),
	((pm.integer('1'),pm.integer('6')), range(1,6)),
	((pm.integer('-5'),pm.integer('40')), range(-5,40)),
	((pm.integer('2'),pm.integer('7'),pm.integer('2')), [2,4,6])
]


for i,j in test_integer_x_range_pairs:
	assert eqiter(itools.integer_xrange(*i),iter(j))
	assert itools.integer_range(*i)==j



## Testing creation of rationals

rational_string_pairs=[
	(pm.rational(0),'0'),
	(pm.rational(2),'2'),
	(pm.rational(15),'15'),
	(pm.rational(-24),'-24'),
	(pm.rational(1,2),'1/2'),
	(pm.rational(1,5),'1/5'),
	(pm.rational(1,8),'1/8'),
	(pm.rational(2,3),'2/3'),
	(pm.rational(-9,10),'-9/10'),
	(pm.rational(2,4),'1/2'),
	(pm.rational(12,11),'12/11'),
	(pm.rational(6,-9),'-2/3'),
	(pm.rational(-12,-10),'6/5'),
	(pm.rational('3/7'),'3/7'),
	(pm.rational('5'),'5'),
	(pm.rational(' 1 0 ',' 4 '),'5/2'),
	(pm.rational('1/3','4'),'1/12'),
	(pm.rational('12','2/3'),'18'),
	(pm.rational('2/7','5/ 11'),'22/35'),
]


for i,j in rational_string_pairs:
	assert str(i)==j



## Testing casting rationals to integers

rat_to_int_pairs= [
	(pm.rational(0),pm.integer(0)),
	(pm.rational(1),pm.integer(1)),
	(pm.rational(26),pm.integer(26)),
	(pm.rational(-1),pm.integer(-1)),
	(pm.rational(-8),pm.integer(-8)),
	(pm.rational(1,2),pm.integer(0)),
	(pm.rational(3,4),pm.integer(0)),
	(pm.rational(2,7),pm.integer(0)),
	(pm.rational(10,3),pm.integer(3)),
	(pm.rational(-3,4),pm.integer(0)),
	(pm.rational(-11,3),pm.integer(-3)),
	(pm.rational(16,3),pm.integer(5)),
	(pm.rational(-16,3),pm.integer(-5)),
]


for i,j in rat_to_int_pairs:
	assert pm.integer(i)==j


## Testing numerator denominator pair for rationals

test_num_dem_triple=[
	(pm.rational(0),pm.integer(0),pm.integer(1)),
	(pm.rational(7),pm.integer(7),pm.integer(1)),
	(pm.rational(-2),pm.integer(-2),pm.integer(1)),
	(pm.rational(1,2),pm.integer(1),pm.integer(2)),
	(pm.rational(1,7),pm.integer(1),pm.integer(7)),
	(pm.rational(8,14),pm.integer(4),pm.integer(7)),
	(pm.rational(8,-14),pm.integer(-4),pm.integer(7)),
]

for i,j,k in test_num_dem_triple:
	assert i.num_dem_pair()==(j,k)


## testing floor and ceiling for rationals

test_floor_ceil_triple=[
	(pm.rational(0),pm.integer(0),pm.integer(0)),
	(pm.rational(3),pm.integer(3),pm.integer(3)),
	(pm.rational(-4),pm.integer(-4),pm.integer(-4)),
	(pm.rational(1,2),pm.integer(0),pm.integer(1)),
	(pm.rational(-1,2),pm.integer(-1),pm.integer(0)),
	(pm.rational(6,5),pm.integer(1),pm.integer(2)),
	(pm.rational(6,-5),pm.integer(-2),pm.integer(-1)),
]

for i,j,k in test_floor_ceil_triple:
	assert i.floor()==j
	assert i.ceiling()==k


## testing the mixed_number_decomp method for rationals

test_mixed_number_decomp_triple=[
	(pm.rational(0),pm.integer(0),pm.rational(0)),
	(pm.rational(3,5),pm.integer(0),pm.rational(3,5)),
	(pm.rational(17,8),pm.integer(2),pm.rational(1,8)),
	(pm.rational(-3,5),pm.integer(0),pm.rational(-3,5)),
	(pm.rational(-17,8),pm.integer(-2),pm.rational(-1,8)),
]

for i,j,k in test_mixed_number_decomp_triple:
	assert i.mixed_number_decomp()==(j,k)




####### number_theory ###########
ntheory= pm.number_theory

isprime= ntheory.isprime


# testing isprime

test_is_prime_pairs=[
	(pm.integer('0'),False),
	(pm.integer(1),False),
	(pm.integer(2),True),
	(pm.integer(5),True),
	(pm.integer(14),False),
	(pm.integer(10000),False),
	(pm.integer(37),True),
]

for i,j in test_is_prime_pairs:
	assert isprime(i)==j


# testing factorization

test_factorization_pairs=[
	(pm.integer(2),[(2,1)]),
	(pm.integer(4),[(2,2)]),
	(pm.integer(9),[(3,2)]),
	(pm.integer(21),[(3,1),(7,1)]),
	(pm.integer(48),[(2,4),(3,1)]),
	(pm.integer(72),[(2,3),(3,2)]),
	(pm.integer(125),[(5,3)]),
]


for i,j in test_factorization_pairs:
	assert ntheory.factorization(i)==j


# testing divisors

test_divisors_pairs=[
	(pm.integer(0),[0]),
	(pm.integer(1),[1]),
	(pm.integer(2),[1,2]),
	(pm.integer(3),[1,3]),
	(pm.integer(4),[1,2,4]),
	(pm.integer(6),[1,2,3,6]),
	(pm.integer(9),[1,3,9]),
	(pm.integer(12),[1,2,3,4,6,12]),
	(pm.integer(35),[1,5,7,35]),
]

for i,j in test_divisors_pairs:
	assert ntheory.divisors(i)==j


# testing isprime_power

test_isprime_power_true=[
	pm.integer(2), pm.integer(3), pm.integer(4),
	pm.integer(5), pm.integer(8), pm.integer(9),
	pm.integer(13), pm.integer(25), pm.integer(27),
	pm.integer(31), pm.integer(32), pm.integer(37),
	pm.integer(47), pm.integer(64), pm.integer(81),
	pm.integer(49), pm.integer(243), pm.integer(343),
	pm.integer(1),
]

for i in test_isprime_power_true:
	assert ntheory.isprime_power(i)


test_isprime_power_false=[
	pm.integer(-7), pm.integer(0), pm.integer(6),
	pm.integer(10), pm.integer(12), pm.integer(14),
	pm.integer(20), pm.integer(21), pm.integer(28),
	pm.integer(33), pm.integer(35), pm.integer(42),
]


for i in test_isprime_power_false:
	assert not ntheory.isprime_power(i)

# testing gcd for integers

test_gcd_int=[
	(pm.integer(2),pm.integer(2),pm.integer(2)),
	(pm.integer(3),pm.integer(4),pm.integer(1)),
	(pm.integer(18),pm.integer(15),pm.integer(3)),
]

for i,j,k in test_gcd_int:
	assert (ntheory.gcd(i,j)==k)


