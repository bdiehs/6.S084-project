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



class Int():
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)
    def get_type(self):
        return INT
    # def evaluate(self):
    #     return self.value

class Plus():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "(" + str(self.left) + ")" + " + " + "(" + str(self.right) + ")"
    def get_type(self):
        return INT

class Minus():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "(" + str(self.left) + ")" + " - " + "(" + str(self.right) + ")"
    def get_type(self):
        return INT

class Leq():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "(" + str(self.left) + ")" + " <= " + "(" + str(self.right) + ")"
    def get_type(self):
        return BOOL

class Eq():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "(" + str(self.left) + ")" + " == " + "(" + str(self.right) + ")"
    def get_type(self):
        return BOOL

# class PatternValue():
#     # I don't think we should have actual variables (this will done via Val)
#     # but we do need a thing for when we do pattern matching
#     def __init__(self, pattern_value):
#         self.pattern_value = pattern_value
#     def __str__(self):
#         return str(self.pattern_value)
#     def get_type(self):
#         return PATTERN_VALUE

class Bool():
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "true" if self.value else "false"
    def get_type(self):
        return BOOL
    # def evaluate(self):
    #     return self.value

class And():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "(" + str(self.left) + ")" + " && " + "(" + str(self.right) + ")"
    def get_type(self):
        return BOOL
    # def evaluate(self, environment):
    #     return self.left.evaluate(environment) and self.right.evaluate(environment)

class Or():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "(" + str(self.left) + ")" + " || " + "(" + str(self.right) + ")"
    def get_type(self):
        return BOOL

class Not():
    def __init__(self, child):
        self.child = child
    def __str__(self):
        return "!" + "(" + str(self.child) + ")"
    def get_type(self):
        return BOOL

class Flse():
    def __init__(self):
        self.value = False
    def __str__(self):
        return "false"
    def get_type(self):
        return BOOL

class Tru():
    def __init__(self):
        self.value = True
    def __str__(self):
        return "true"
    def get_type(self):
        return BOOL

# class Lst():
#     def __init__(self, value):
#         self.value = value # Cons or Nil
#     def __str__(self):
#         return str(self.value)
#     def get_type(self):
#         return LIST

class Cons():
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr
    def __str__(self):
        return "Cons " + str(self.car) + " " +  str(self.cdr)
    def get_type(self):
        return LIST

class Nil():
    def __str__(self):
        return "Nil"
    def get_type(self):
        return LIST

# class Case():
#     def __init__(self, lhs, rhs):
#         self.lhs = lhs
#         self.rhs = rhs
#     def __str__(self):
#         return "case " + str(self.lhs) + " => " + str(self.rhs)
#     def get_type(self):
#         return CASE

class Match():
    def __init__(self, match_on, cases):
        self.match_on = match_on
        self.cases = cases
    def __str__(self):
        result = str(self.match_on) + " match {\n\t"
        for case in self.cases[:-1]:
            result += str(case) + "\n\t"
        result += str(self.cases[-1]) + "\n" # don't want to tab the end curly bracket
        result += "}"
        return result
    def get_type(self):
        return MATCH

class Hole():

    def __init__(self, type_):
        self.type = type_
    def __str__(self):
        return " ?? " # TODO figure this out. this is probably just for our debugging
    def get_type(self):
        return self.type


class St():
    def __init__(self, vals):
        self.vals = vals # Cons or Nil
    def __str__(self):
        return str(self.value)
    def get_type(self):
        return SET

class StPlus():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "(" + str(self.left) + ")" + " ++ " + "(" + str(self.right) + ")"
    def get_type(self):
        return SET

class Abs():
    def __init__(self, var_types, ret_type, vars_, body):
        self.vars = vars_
        self.var_types = var_types
        self.ret_type = ret_type
        self.body = body
    def __str__(self):
        return 'func' + self.vars + ": " + str(var_types) + ' = ' + str(body)
    def get_type(self):
        return TArrow(var_types, ret_type)

class This():
    def __init__(self, type_):
        self.type = type_
    def __str__(self):
        return 'this'
    def get_type(self):
        return self.type

class App():
    def __init__(self, func, args):
        self.func = func
        self.args = args
    def __str__(self):
        return str(self.func) + "(" + str(self.args) + ")"
    def get_type(self):
        return get_type(self.func).to_

class Tuple():
    def __init__(self, vals):
        self.vals = vals
    def __str__(self):
        return str(vals)
    def get_type(self):
        return TTuple([get_type(val) for val in self.vals])

class Harness():
    def __init__(self, return_type, name, choose_cond, body):
        self.ret_type = return_type
        self.name = name
        self.choose_cond = choose_cond
        self.body = body
    def __str__(self):
        return str(self.func) + "(" + str(self.args) + ")"
    def get_type(self):
        return get_type(self.func).to_


# TODO content and set?

if __name__ == '__main__':
    pass
    # print(Choose(Annotation("r", Lst(Cons(2, Nil()))), Not(Or(Tru(), Flse()))))
    # print(Match(Lst(Nil()), [Case(Cons(PatternValue("h"), Nil()), Flse())]))
