class Type:

	def __init__(self):
		raise Exception('')

class TList(Type):

	def __init__(self):
		pass

class TSet(Type):

	def __init__(self, type_):
		self.type = type_

class TInt(Type):

	def __init__(self):
		pass

class TBool(Type):

	def __init__(self):
		pass

class TArrow(Type):

	def __init__(self, t1, t2):
		self.from_ = t1
		self.to_ = t2

class TTuple(Type):

	def __init__(self, types):
		self.types = types


