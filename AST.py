
import Types

class AST_node:
	def __init__(self):
		raise Exception('AST node not implemented')

class Int(AST_node):
	def __init__(self, n):
		self.val = n

class Var(AST_node):
	def __init__(self, n):
		self.name = n

class Plus(AST_node):
	def __init__(self, l, r):
		self.l = l
		self.r = r

class Times(AST_node):
	def __init__(self, l, r):
		self.l = l
		self.r = r

class Minus(AST_node):
	def __init__(self, l, r):
		self.l = l
		self.r = r

class Eq(AST_node):
	def __init__(self, l, r):
		self.l = l
		self.r = r

class Leq(AST_node):
	def __init__(self, l, r):
		self.l = l
		self.r = r

class Bool(AST_node):
	def __init__(self, b):
		self.val = b

class And(AST_node):
	def __init__(self, l, r):
		self.l = l
		self.r = r

class Or(AST_node):
	def __init__(self, l, r):
		self.l = l
		self.r = r

class Not(AST_node):
	def __init__(self, l):
		self.l = l

class Nil(AST_node):
	def __init__(self):
		pass

class Cons(AST_node):
	def __init__(self, a, l):
		self.hd = a
		self.tl = l

class Set(AST_node):
	def __init__(self, elts):
		self.elts = elts

class SetPlus(AST_node):
	def __init__(self, l, r):
		self.l = l
		self.r = r

class Match(AST_node):
	def __init__(self, expr, nil_case, x, xs, cons_case):
		self.expr = expr
		self.nil_case = nil_case
		self.varhd = x
		self.vartl = xs
		self.cons_case = cons_case

class Hole(AST_node):
	def __init__(self, type_):
		self.type = type_

class Abs(AST_node):
	def __init__(self, var_types, ret_type, vars_, expr):
		self.vars = vars_
		self.var_types = var_types
		self.ret_type = ret_type
		self.expr = expr

class This(AST_node):
	def __init__(self, type_):
		self.type = type_

class App(AST_node):
	def __init__(self, func, args):
		self.func = func
		self.args = args

class Tuple(AST_node):
	def __init__(self, vals):
		self.vals = vals

class Harness(AST_node):
	def __init__(self, return_type, name, choose_cond, body):
		self.ret_type = return_type
		self.name = name
		self.choose_cond = choose_cond
		self.body = body

TTList = Types.TList()
TTInt = Types.TInt()

size = Abs([TTList], TTInt, ["lst"], Match(Var("lst"), Int(0), '_', 'rest', Plus(Int(1), App(This(Types.TArrow([TTList], TTInt)), [Var('rest')]))))

content = Abs([TTList], Types.TSet(TTInt), ["lst"], Match(Var("lst"), Set([]), 'e', 'rest', SetPlus(Set(['e']), App(This(Types.TArrow([TTList], Types.TSet(TTInt))), [Var('rest')]))))

# split0 = Harness(Tuple([TTList, TTList]), "split",
# 	Abs("r", Tuple([TTList, TTList]),
# 		And()))

