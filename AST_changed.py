# INT = "INT"
# # PLUS = "PLUS"
# # MINUS = "MINUS"
# # LEQ = "LEQ"
# # EQ = "EQ"
# PATTERN_VALUE = "PATTERN VALUE"
# BOOL = "BOOL"
# # AND = "AND"
# # NOT = "NOT"
# # OR = "OR"
# # FALSE = "FALSE"
# # TRUE = "TRUE"
# LIST = "LIST"
# # CONS = "CONS"
# # NIL = "NIL"
# # CASE = "CASE"
# # MATCH = "MATCH"
# FUNCTION = "FUNCTION"
# HOLE = "HOLE"
# # IF = "IF"
# # IF_ELSE = "IF ELSE"
# # VAL = "VAL"
# # CHOOSE = "CHOOSE"
# # ANNOTATION = "ANNOTATION"
# SET = "SET"

class Type:
    def __init__(self):
        raise Exception('')

class TList(Type):
    def __init__(self):
        pass
    def __str__(self):
        return "LIST"

class TSet(Type):
    def __init__(self, type_):
        pass
    def __str__(self):
        return "SET"

class TInt(Type):
    def __init__(self):
        pass
    def __str__(self):
        return "INT"

class TBool(Type):
    def __init__(self):
        pass
    def __str__(self):
        return "BOOL"

class TArrow(Type):
    def __init__(self, t1, t2):
        self.from_ = t1
        self.to_ = t2
    def __str__(self):
        return str(self.from_) + " -> " + str(self.to_)

class TTuple(Type):
    def __init__(self, types):
        self.types = types
    def __str__(self):
        return "TUPLE" + types


INT = TInt()
LIST = TList()
BOOL = TBool()
SET = TSet(INT)

class Var():
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def get_type(self, envt):
        return envt[name].get_type()

class Int():
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)
    def get_type(self, envt):
        return INT
    # def evaluate(self):
    #     return self.value

class Plus():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "(" + str(self.left) + ")" + " + " + "(" + str(self.right) + ")"
    def get_type(self, envt):
        return INT

class Minus():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "(" + str(self.left) + ")" + " - " + "(" + str(self.right) + ")"
    def get_type(self, envt):
        return INT

class Leq():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "(" + str(self.left) + ")" + " <= " + "(" + str(self.right) + ")"
    def get_type(self, envt):
        return BOOL

class Eq():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "(" + str(self.left) + ")" + " == " + "(" + str(self.right) + ")"
    def get_type(self, envt):
        return BOOL

# class PatternValue():
#     # I don't think we should have actual variables (this will done via Val)
#     # but we do need a thing for when we do pattern matching
#     def __init__(self, pattern_value):
#         self.pattern_value = pattern_value
#     def __str__(self):
#         return str(self.pattern_value)
#     def get_type(self, envt):
#         return PATTERN_VALUE

class Bool():
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "true" if self.value else "false"
    def get_type(self, envt):
        return BOOL
    # def evaluate(self):
    #     return self.value

class And():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "(" + str(self.left) + ")" + " && " + "(" + str(self.right) + ")"
    def get_type(self, envt):
        return BOOL
    # def evaluate(self, environment):
    #     return self.left.evaluate(environment) and self.right.evaluate(environment)

class Or():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "(" + str(self.left) + ")" + " || " + "(" + str(self.right) + ")"
    def get_type(self, envt):
        return BOOL

class Not():
    def __init__(self, child):
        self.child = child
    def __str__(self):
        return "!" + "(" + str(self.child) + ")"
    def get_type(self, envt):
        return BOOL

class Flse():
    def __init__(self):
        self.value = False
    def __str__(self):
        return "false"
    def get_type(self, envt):
        return BOOL

class Tru():
    def __init__(self):
        self.value = True
    def __str__(self):
        return "true"
    def get_type(self, envt):
        return BOOL

# class Lst():
#     def __init__(self, value):
#         self.value = value # Cons or Nil
#     def __str__(self):
#         return str(self.value)
#     def get_type(self, envt):
#         return LIST

class Cons():
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr
    def __str__(self):
        return "Cons " + str(self.car) + " " +  str(self.cdr)
    def get_type(self, envt):
        return LIST

class Nil():
    def __init__(self):
        pass
    def __str__(self):
        return "Nil"
    def get_type(self, envt):
        return LIST

# class Case():
#     def __init__(self, lhs, rhs):
#         self.lhs = lhs
#         self.rhs = rhs
#     def __str__(self):
#         return "case " + str(self.lhs) + " => " + str(self.rhs)
#     def get_type(self, envt):
#         return CASE

class Match():
    def __init__(self, match_on, nil_case, cons_vars, cons_case):
        self.match_on = match_on
        self.nil_case = nil_case
        self.cons_vars = cons_vars
        self.cons_case = cons_case
    def __str__(self):
        result = str(self.match_on) + " match {\n\t"
        result += "case Nil => " + str(self.nil_case) + "\n\t"
        result += "case Cons(" + self.cons_vars[0] + ", " + self.cons_vars[1] + ") => \n\t\t" + str(self.cons_case)
        result += "\n}"
        return result
    def get_type(self, envt):
        return TArrow(match_on.get_type(), nil_case.get_type())

class Hole():

    def __init__(self, type_):
        self.type = type_
    def __str__(self):
        return " ?? " # TODO figure this out. this is probably just for our debugging
    def get_type(self, envt):
        return self.type

class St():
    def __init__(self, vals):
        self.vals = vals # Cons or Nil
    def __str__(self):
        return str(self.value)
    def get_type(self, envt):
        return SET

class StPlus():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "(" + str(self.left) + ")" + " ++ " + "(" + str(self.right) + ")"
    def get_type(self, envt):
        return SET

class Func():
    def __init__(self, name, var_types, ret_type, vars_, body):
        self.name = name
        self.vars = vars_
        self.var_types = var_types
        self.ret_type = ret_type
        self.body = body
    def __str__(self):
        return 'func' + str(self.vars) + ": " + str(self.var_types) + ' = ' + str(self.body)
    def get_type(self, envt):
        return TArrow(var_types, ret_type)


class App():
    def __init__(self, func, args):
        self.func = func
        self.args = args
    def __str__(self):
        return str(self.func) + "(" + str(self.args) + ")"
    def get_type(self, envt):
        return self.func.get_type().to_

class LetIn():
    def __init__(self, var_name, val, body):
        self.var_name = var_name
        self.val = val
        self.body = body

    def __str__(self):
        return 'val ' self.var_name + ' = ' + str(val) + '\n' + str(body)
    def get_type(self, envt):
        return self.body.get_type(envt)

class Tuple():
    def __init__(self, vals):
        self.vals = vals
    def __str__(self):
        return str(vals)
    def get_type(self, envt):
        return TTuple([val.get_type() for val in self.vals])

class TupleAcc():
    def __init__(self, tup, idx):
        self.tuple = tup
        self.idx = idx
    def __str__(self):
        return str(self.tuple) + '[' + str(self.idx) + ']'
    def get_type(self, envt):
        return self.tuple.get_type()[self.idx]

class Harness():
    def __init__(self, return_type, name, choose_cond, body):
        self.ret_type = return_type
        self.name = name
        self.choose_cond = choose_cond
        self.body = body
    def __str__(self):
        return str(self.func) + "(" + str(self.args) + ")"
    def get_type(self, envt):
        return self.func.get_type().to_


# TODO content and set?

if __name__ == '__main__':
    size = Func('size', [LIST], INT, ['lst'], 
        Match(Var('lst'),
            Int(0),
            ['_', 'rest'], Plus(Int(1), App(Var('size'), [Var('rest')]))
        )
    )
    content = Func('content', [LIST], INT, ['lst'],
        Match(Var('lst'),
            Set([]),
            ['e', 'rest'], StPlus(St(['e']), App(Var('content'), [Var('rest')]))
            )
    )
    # split0 = Func('split', [LIST], Tuple([LIST, LIST]), ['lst'],
    #     Func('_', [Tuple(LIST, LIST)], BOOL, ['r'],
    #         Eq(App(Var('content'), Var('lst')), StPlus(App(Var('content'), TupleAcc(Var('r'), 0)), App(Var('content'), TupleAcc(Var('r'), 1)))))
    #     Match(Var('lst'),
    #         Tuple([Nil(), Nil()]),
    #         ['h', 't'], Match(Var('t'),
    #             Tuple([Nil(), Cons(Var('h'), Nil())])
    #             ['h2', 't2'],
    #         )
    #     )

    # )

    print(size)
    pass
    # print(Choose(Annotation("r", Lst(Cons(2, Nil()))), Not(Or(Tru(), Flse()))))
    # print(Match(Lst(Nil()), [Case(Cons(PatternValue("h"), Nil()), Flse())]))
