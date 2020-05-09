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

SCALA_TAB = "  "

def list_str(l):
    return ', '.join([str(e) for e in l])

class Type:
    def __init__(self):
        raise Exception('')

# I think when we print these types, we want them like how scala expects them
# so I'm going to change LIST -> List etc
# and change the __str__ to a get_type in case we need that
# also we don't actually need inits if we don't do anything in them
class TList(Type):
    def __init__(self):
        pass
    def get_type(self):
        return "LIST"
    def __str__(self):
        return "List"

class TSet(Type):
    def __init__(self, type_):
        pass
    def get_type(self):
        return "SET"
    def __str__(self):
        return "Set"

class TInt(Type):
    def __init__(self):
        pass
    def get_type(self):
        return "INT"
    def __str__(self):
        return "Int"

class TBool(Type):
    def __init__(self):
        pass
    def get_type(self):
        return "BOOL"
    def __str__(self):
        return "Boolean"

class TArrow(Type):
    def __init__(self, t1, t2):
        self.from_ = t1
        self.to_ = t2
    def get_type(self):
        return str(self.from_) + " -> " + str(self.to_)
    def __str__(self):
        return self.get_type() # for now

class TTuple(Type):
    # what is this for?
    def __init__(self, types):
        self.types = types
    def get_type(self):
        return "TUPLE(" + list_str(self.types) + ')'
    def __str__(self):
        return "(" + list_str(self.types) + ")"


INT = TInt()
LIST = TList()
BOOL = TBool()
SET = TSet(INT)

class Var():
    # I know we have the problem of variables that are inputs in functions,
    # but I think there's cases where it makes more sense for a Var to have a name and a value
    # and then the value is its own node and has a type
    # not the environment way
    # like what we talked about this morning?
    def __init__(self, name):
        self.name = name
        # self.value = value
    def __str__(self):
        return self.name #+ " = " + str(self.value)
    def get_type(self, envt):
        return envt[name].get_type()
    # def get_type(self):
    #     return self.value.get_type()

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

class Lt():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "(" + str(self.left) + ")" + " < " + "(" + str(self.right) + ")"
    def get_type(self, envt):
        return BOOL

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

# I think we do need a list type. Leon has a list type.
class Lst():
    def __init__(self, value):
        self.value = value # Cons or Nil
    def __str__(self):
        return str(self.value)
    def get_type(self, envt):
        return LIST

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
    # I guess if the only thing we ever want to match on is lists, this is fine
    def __init__(self, match_on, nil_case, cons_vars, cons_case):
        self.match_on = match_on
        self.nil_case = nil_case
        self.cons_vars = cons_vars
        self.cons_case = cons_case
    def __str__(self):
        # replacing tabs with two spaces each
        result = str(self.match_on) + " match {\n" + SCALA_TAB
        result += "case Nil => " + str(self.nil_case) + "\n" + SCALA_TAB
        result += "case Cons(" + self.cons_vars[0] + ", " + self.cons_vars[1] + ") => \n" + SCALA_TAB*2 + str(self.cons_case)
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
        return str(self.vals)
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
    def get_name(self):
        return self.name
    def get_var_types(self):
        return self.var_types
    def get_ret_type(self):
        return self.ret_type
    def get_vars(self):
        return self.vars
    def get_body(self):
        return self.body # rep exposure
    def _get_function_arguments(self):
        if len(self.vars) == 0:
            return ""

        arguments = ""
        for i in range(len(self.vars) -1):
            arguments += str(self.vars[i]) + " : " + str(self.var_types[i]) + ", "
        arguments += str(self.vars[-1]) + " : " + str(self.var_types[-1])
        return arguments
    def _add_tabs_body(self):
        body_lines = str(self.body).split("\n")
        if len(body_lines) == 0:
            return ""
        tabbed_body = ""
        for line in body_lines[:-1]:
            tabbed_body += SCALA_TAB + line + "\n"
        tabbed_body += SCALA_TAB + body_lines[-1]
        return tabbed_body

    def __str__(self):
        # this has a bug, multiple parameters won't be next to their type
        # also, shouldn't this get pretty printed the way scala expects it, like with scala types like List instead of LIST etc?
        # also self.body doesn't look right...
        return 'def ' + self.name + " (" + self._get_function_arguments() + ") " + ": " + str(self.ret_type) + ' = {\n' + self._add_tabs_body() + "\n}"
    def get_type(self, envt):
        return TArrow(var_types, ret_type)
    def get_call(self, variables):
        # precondition: variables must be passed in in the same order as originally
        # returns string representing calling the function
        # for example size(lst_A)
        return self.name + "(" + list_str(variables) + ")"


class App():
    def __init__(self, func, args):
        self.func = func
        self.args = args
    def __str__(self):
        return str(self.func) + "(" + list_str(self.args) + ")"
    def get_type(self, envt):
        return self.func.get_type().to_

class LetIn():
    # val assignment followed by body
    def __init__(self, var_name, val, body):
        self.var_name = var_name
        self.val = val
        self.body = body

    def __str__(self):
        return 'val ' + self.var_name + ' = ' + str(self.val) + '\n' + str(self.body)
    def get_type(self, envt):
        return self.body.get_type(envt)

class Tuple():
    def __init__(self, vals):
        self.vals = vals
    def __str__(self):
        return list_str(self.vals)
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

class Choose():
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    def get_lhs(self):
        return self.lhs
    def get_rhs(self):
        return self.rhs
    def __str__(self):
        return str(self.lhs) + " => " + str(self.rhs)
    def get_type(self):
        return BOOL # I think? should it be its own type?

class Harness(Func):
    # for termination measure purposes, I want choose_cond to be very easy to change
    def __init__(self, name, var_types, ret_type, vars_, choose_cond, body):
        self.name = name
        self.vars = vars_
        self.var_types = var_types
        self.ret_type = ret_type
        self.choose_cond = choose_cond
        self.body = body
    def __str__(self):
        # isn't harness not a thing in Leon? why do we have a harness?
        # is this for our own use (like functions that aren't Harnesses, we won't search for holes and will just pretty print)?
        # anyway I'm changing this to like function
        # I don't think we want the keyword harness in the string
        # TODO figure out: are there two sets of curly brackets, one for choose, one for body? or one whole thing?
        # would it be one big choose with the body in it, and holes in teh body => the post condition? my best guess
        # I think we should discuss this so I'm going to leave it for now

        return 'harness ' + list_str(self.vars) + ": " + list_str(self.var_types) + ' = ' + str(self.body)
        # return "def " + self.name + " (" + self._get_function_arguments() + ") " + ": " + str(self.ret_type) + ' = ' + str(self.choose_cond) + self._add_tabs_body() + "\n}"
    def get_type(self, envt):
        return self.func.get_type().to_








if __name__ == '__main__':
    # size = Func('size', [LIST, INT], INT, ['lst', Int(0)],
    #     Match(Var('lst'),
    #         Int(0),
    #         ['_', 'rest'], Plus(Int(1), App(Var('size'), [Var('rest')]))
    #     )
    # )
    # content = Func('content', [LIST], INT, ['lst'],
    #     Match(Var('lst'),
    #         St([]),
    #         ['e', 'rest'], StPlus(St(['e']), App(Var('content'), [Var('rest')]))
    #         )
    # )
    split0 = Harness('split', [LIST], TTuple([LIST, LIST]), ['lst'],
        Func('_', [TTuple([LIST, LIST])], BOOL, ['r'],
            Eq(App(Var('content'), Var('lst')), StPlus(App(Var('content'), TupleAcc(Var('r'), 0)), App(Var('content'), TupleAcc(Var('r'), 1))))),
        Match(Var('lst'),
            Tuple([Nil(), Nil()]),
            ['h', 't'], Match(Var('t'),
                Tuple([Nil(), Cons(Var('h'), Nil())]),
                ['h2', 't2'],
                LetIn('v', App(Var('split'), [Var('t2')]),
                    Tuple([Cons(Var('h1'), TupleAcc(Var('r'), 1)), Cons(Var('h2'), TupleAcc(Var('r'), 2))])
                )
            )
        )
    )

    print(split0)
    pass
    # print(Choose(Annotation("r", Lst(Cons(2, Nil()))), Not(Or(Tru(), Flse()))))
    # print(Match(Lst(Nil()), [Case(Cons(PatternValue("h"), Nil()), Flse())]))
