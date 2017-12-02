'''
Basics Package:

contains the basics numerical datatype as specified in the rings module

Also contains some basic tools for those datatypes



'''




def is_math_type(x):
	'''
		returns whether or not x is of math_type
		that is, if type(x) is one of [integer,rational]
	'''
	return type(x) in _math_types


def py_to_math(x):
	'''
		Converts a object x, of python datatype 
			into a pymath datatype, if possible.
			otherwise, x is unconverted
		returns the converted value
	'''
	if type(x) in _py_to_math_dict:
		return _py_to_math_dict[type(x)](x)
	return x

def math_to_py(x):
	'''
		Converts a object x, of pymath datatype 
			into a python datatype, if possible.
			otherwise, x is unconverted
		returns the converted value
	'''
	if type(x) in _math_to_py_dict:
		return _math_to_py_dict[type(x)](x)
	return x






import rings
from rings import *





_math_types=[integer,rational]
_py_to_math_dict= {int:integer,long:integer}
_math_to_py_dict= {integer:int,rational:float}







import integer_tools
















