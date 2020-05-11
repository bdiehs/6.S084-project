VAR = "VAR"
INTEGER = "INTEGER"
PLUS = "PLUS"
MINUS = "MINUS"
LT = "LT"
LEQ = "LEQ"
EQ = "EQ"
BOOL = "BOOL"
AND = "AND"
NOT = "NOT"
OR = "OR"
FALSE = "FALSE"
TRUE = "TRUE"
LIST = "LIST"
CONS = "CONS"
NIL = "NIL"
MATCH = "MATCH"
FUNC = "FUNCTION"
CALL_FUNC = "CALL FUNCTION"
FUNC_TYPE = "FUNC TYPE"
LET_IN = "LET IN"
APP = "APP"
HOLE = "HOLE"
CHOOSE = "CHOOSE"
SET = "SET"
SET_PLUS = "SET PLUS"
TUPLE = "TUPLE"
TUPLE_ACC = "TUPLE ACC"
HARNESS = "HARNESS"

SCALA_TAB = "  "
EMPTY = "EMPTY"

def list_str(l):
    return ', '.join([str(e) for e in l])

class Type:
    def __init__(self):
        raise Exception('')

# I think when we print these types, we want them like how scala expects them
# so I'm going to change LIST -> List etc
# and change the __str__ to a get_type in case we need that
# also we don't actually need inits if we don't do anything in them

class NonFuncType(Type):
    def is_func_type(self):
        return False

class TList(NonFuncType):
    def __init__(self):
        pass
    def get_type(self):
        return "LIST"
    def __str__(self):
        return "List"

class TSet(NonFuncType):
    def __init__(self, type_):
        pass
    def get_type(self):
        return "SET"
    def __str__(self):
        return "Set"

class TInt(NonFuncType):
    def __init__(self):
        pass
    def get_type(self):
        return "INT"
    def __str__(self):
        return "Int"

class TBool(NonFuncType):
    def __init__(self):
        pass
    def get_type(self):
        return "BOOL"
    def __str__(self):
        return "Boolean"

class TArrow(NonFuncType):
    def __init__(self, t1, t2):
        self.from_ = t1
        self.to_ = t2
    def get_type(self):
        return str(self.from_) + " -> " + str(self.to_)
    def __str__(self):
        return self.get_type() # for now

class TTuple(NonFuncType):
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

class VarNameGen:
    def __init__(self):
        self.num = 0
    def get_name(self):
        self.num += 1
        return "_hole" + str(self.num)

HOLE_NAME_GEN = VarNameGen()


class Empty():
    # the empty node. nodes may become empty after pruning
    def __str__(self):
        return "" # just for debugging
    def get_node_type(self):
        return EMPTY
    def get_type(self):
        return EMPTY # just for debugging
    def is_empty(self):
        return True

class NonEmpty():
    def is_empty(self):
        return False
    def accept(self, visitor):
        return visitor.on(self)

class Var(NonEmpty):
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
    def prune(self, variables):
        return Empty() if self.name not in variables else self
    def get_node_type(self):
        return VAR

class Int(NonEmpty):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)
    def get_type(self, envt):
        return INT
    def prune(self, variables):
        return self
    def get_node_type(self):
        return INTEGER

class ArithmeticOperation(NonEmpty):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def get_left(self):
        return self.left
    def get_right(self):
        return self.right
    def prune(self, variables):
        new_left = self.left.prune(variables)
        new_right = self.right.prune(variables)
        if new_left.is_empty() or new_right.is_empty():
            return Empty()
        return self

class Plus(ArithmeticOperation):
    def __str__(self):
        return "(" + str(self.left) + ")" + " + " + "(" + str(self.right) + ")"
    def get_type(self, envt):
        return INT
    def get_node_type(self):
        return PLUS

class Minus(ArithmeticOperation):
    def __str__(self):
        return "(" + str(self.left) + ")" + " - " + "(" + str(self.right) + ")"
    def get_type(self, envt):
        return INT
    def get_node_type(self):
        return MINUS

class Lt(ArithmeticOperation):
    def __str__(self):
        return "(" + str(self.left) + ")" + " < " + "(" + str(self.right) + ")"
    def get_type(self, envt):
        return BOOL
    def get_node_type(self):
        return LT

class Leq(ArithmeticOperation):
    def __str__(self):
        return "(" + str(self.left) + ")" + " <= " + "(" + str(self.right) + ")"
    def get_type(self, envt):
        return BOOL
    def get_node_type(self):
        return LEQ

class Eq(ArithmeticOperation):
    def __str__(self):
        return "(" + str(self.left) + ")" + " == " + "(" + str(self.right) + ")"
    def get_type(self, envt):
        return BOOL
    def get_node_type(self):
        return EQ

class Bool(NonEmpty):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "true" if self.value else "false"
    def get_type(self, envt):
        return BOOL
    def prune(self, variables):
        return self
    def get_node_type(self):
        return BOOL

class TwoBooleanOperation(NonEmpty):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def get_type(self, envt):
        return BOOL
    def prune(self, variables):
        # remove lowest nodes using variables not in variables
        # if either left or right is empty, truth value becomes the other one
        new_right = self.right.prune(variables)
        new_left = self.left.prune(variables)
        if (not new_right.is_empty()) and (not new_left.is_empty()):
            return self
        if new_right.is_empty() and new_left.is_empty():
            return Empty()
        return new_left if new_right.is_empty() else new_right

class And(TwoBooleanOperation):
    def __str__(self):
        return "(" + str(self.left) + ")" + " && " + "(" + str(self.right) + ")"
    def get_node_type(self):
        return AND

class Or(TwoBooleanOperation):
    def __str__(self):
        return "(" + str(self.left) + ")" + " || " + "(" + str(self.right) + ")"
    def get_node_type(self):
        return OR

class Not(NonEmpty):
    def __init__(self, child):
        self.child = child
    def __str__(self):
        return "!" + "(" + str(self.child) + ")"
    def get_type(self, envt):
        return BOOL
    def get_child(self):
        return self.child
    def prune(self, variables):
        child_pruned = self.child.prune(variables)
        return child_pruned if child_pruned.is_empty() else self
    def get_node_type(self):
        return NOT

class Flse(NonEmpty):
    def __init__(self):
        self.value = False
    def __str__(self):
        return "false"
    def get_type(self, envt):
        return BOOL
    def prune(self, variables):
        return self
    def get_node_type(self):
        return FALSE

class Tru(NonEmpty):
    def __init__(self):
        self.value = True
    def __str__(self):
        return "true"
    def get_type(self, envt):
        return BOOL
    def prune(self, variables):
        return self
    def get_node_type(self):
        return TRUE

# I think we do need a list type. Leon has a list type.
class Lst(NonEmpty):
    def __init__(self, value):
        self.value = value # Cons or Nil
    def __str__(self):
        return str(self.value)
    def get_type(self, envt):
        return LIST
    def get_node_type(self):
        return LIST

class Cons(NonEmpty):
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr
    def get_car(self):
        return self.car
    def get_cdr(self):
        return self.cdr
    def __str__(self):
        return "Cons " + str(self.car) + " " +  str(self.cdr)
    def get_type(self, envt):
        return LIST
    def get_node_type(self):
        return CONS

class Nil(NonEmpty):
    def __init__(self):
        pass
    def __str__(self):
        return "Nil"
    def get_type(self, envt):
        return LIST
    def get_node_type(self):
        return NIL

class ConsCase(Cons):
    def __init__(self, car_name, cdr_name, cons_case):
        self.car_name = car_name
        self.cdr_name = cdr_name
        self.cons_case = cons_case
    def __str__(self):
        return "case Cons(" + self.car_name + ", " + self.cdr_name + ") => \n" + SCALA_TAB*2 + str(self.cons_case)

class Match(NonEmpty):
    # I guess if the only thing we ever want to match on is lists, this is fine
    def __init__(self, match_on, nil_case, cons_case):
        self.match_on = match_on
        self.nil_case = nil_case
        self.cons_case = cons_case # ConsCase instance
    def get_match_on(self):
        return self.match_on
    def get_nil_case(self):
        return self.nil_case
    def get_cons_case(self):
        return self.cons_case
    def __str__(self):
        # replacing tabs with two spaces each
        result = str(self.match_on) + " match {\n" + SCALA_TAB
        result += "case Nil => " + str(self.nil_case) + "\n" + SCALA_TAB
        result += str(self.cons_case)
        result += "\n}"
        return result
    def get_type(self, envt):
        return TArrow(match_on.get_type(), nil_case.get_type())
    def get_node_type(self):
        return MATCH

class Hole(NonEmpty):
    def __init__(self, type_):
        # primitive or FuncType
        self.type = type_
        self.name = HOLE_NAME_GEN.get_name()
    def __str__(self):
        return self.name # TODO figure this out. this is probably just for our debugging
    def get_type(self, envt = None):
        # if not a function, it can just be literally the type
        # if it is a function, I want the types of the args
        #   and the return type
        return self.type
    def get_node_type(self):
        return HOLE

class St(NonEmpty):
    def __init__(self, vals):
        self.vals = vals # Cons or Nil
    def __str__(self):
        return "Set(" + list_str(self.vals) + ")"
    def get_type(self, envt):
        return SET
    def get_node_type(self):
        return SET
    def get_vals(self):
        return self.vals

class StPlus(NonEmpty):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "(" + str(self.left) + ")" + " ++ " + "(" + str(self.right) + ")"
    def get_type(self, envt):
        return SET
    def get_node_type(self):
        return SET_PLUS
    def get_left(self):
        return self.left
    def get_right(self):
        return self.right

class FuncType():
    def __init__(self, var_types, ret_type):
        self.var_types = var_types
        self.ret_type = ret_type

        types_counts = {var_type : 0 for var_type in self.var_types}
        self.fake_var_names = []
        for var_type in self.var_types:
            self.fake_var_names.append(str(var_type) + str(types_counts[var_type]))
            types_counts[var_type] += 1

    def get_function_arguments(self):
        if len(self.var_types) == 0:
            return ""

        arguments = ""
        for i in range(len(self.fake_var_names) -1):
            arguments += str(self.fake_var_names[i]) + " : " + str(self.var_types[i]) + ", "
        arguments += str(self.fake_var_names[-1]) + " : " + str(self.var_types[-1])
        return arguments
    def get_fake_var_names(self):
        return self.fake_var_names
    def get_var_types(self):
        return self.var_types
    def get_ret_type(self):
        return self.ret_type
    def get_node_type(self):
        return FUNC_TYPE
    def is_func_type(self):
        return True


class Func(NonEmpty):
    def __init__(self, name, func_type, vars_, body):
        # I'm changing this to have a func type of var types and ret type
        self.name = name
        self.vars = vars_
        self.func_type = func_type
        self.body = body
    def get_name(self):
        return self.name
    def get_func_type(self):
        return self.func_type
    def get_vars(self):
        return self.vars
    def get_body(self):
        return self.body # rep exposure
    def get_function_arguments(self):
        if len(self.vars) == 0:
            return ""

        arguments = ""
        var_types = self.func_type.get_var_types()
        for i in range(len(self.vars) -1):
            arguments += str(self.vars[i]) + " : " + str(var_types[i]) + ", "
        arguments += str(self.vars[-1]) + " : " + str(var_types[-1])
        return arguments
    def add_tabs_body(self, body):
        body_lines = str(body).split("\n") # BUG use of self.body?
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
        return 'def ' + self.name + " (" + self.get_function_arguments() + ") " + ": " + str(self.func_type.get_ret_type()) + ' = {\n' + self.add_tabs_body(self.body) + "\n}"
    def get_type(self, envt):
        # return TArrow(self.var_types, ret_type)
        return self.func_type
    def get_call(self, variables):
        return CallFunc(self.name, variables, self.func_type.get_ret_type())
    def get_node_type(self):
        return FUNC

class CallFunc(NonEmpty):
    # a call to a function
    # uses specific variable names for the call, not the argument names
    def __init__(self, name, vars_, ret_type):
        self.name = name
        self.vars = vars_
        self.ret_type = ret_type # just for type checking
    def __str__(self):
        return self.name + "(" + list_str(self.vars) + ")"
    def get_vars(self):
        return self.vars
    def get_type(self, envt):
        return TArrow(var_types, ret_type)
    def prune(self, variables):
        # if using variables not in variables, return empty
        for variable in self.vars:
            if variable not in variables:
                return Empty()
        return self
    def get_node_type(self):
        return CALL_FUNC

class App(NonEmpty):
    # I think App and CallFunc are the same thing actually except this one has better types
    # I will resolve that later
    # this one supports currying?
    # I will let this slide for now TODO
    def __init__(self, func, args):
        self.func = func
        self.args = args
    def __str__(self):
        return str(self.func) + "(" + list_str(self.args) + ")"
    def get_type(self, envt):
        return self.func.get_type().to_
    def get_node_type(self):
        return APP

class LetIn(NonEmpty):
    # val assignment followed by body
    def __init__(self, var_name, val, body):
        self.var_name = var_name
        self.val = val
        self.body = body
    def get_var_name(self):
        return self.var_name
    def get_val(self):
        return self.val
    def get_body(self):
        return self.body
    def __str__(self):
        return 'val ' + self.var_name + ' = ' + str(self.val) + '\n' + str(self.body)
    def get_type(self, envt):
        return self.body.get_type(envt)
    def get_node_type(self):
        return LET_IN

class Tuple(NonEmpty):
    def __init__(self, vals):
        self.vals = vals
    def get_vals(self):
        return self.vals
    def __str__(self):
        return list_str(self.vals)
    def get_type(self, envt):
        return TTuple([val.get_type() for val in self.vals])
    def get_node_type(self):
        return TUPLE

class TupleAcc(NonEmpty):
    def __init__(self, tup, idx):
        self.tuple = tup
        self.idx = idx
    def get_tuple(self):
        return self.tuple
    def get_idx(self):
        return self.idx
    def __str__(self):
        return str(self.tuple) + '[' + str(self.idx) + ']'
    def get_type(self, envt):
        return self.tuple.get_type()[self.idx]
    def get_node_type(self):
        return TUPLE_ACC

class ChooseLHS(NonEmpty):
    def __init__(self, var_name, type):
        # must be same as output type
        self.var_name = var_name
        self.type = type
    def __str__(self):
        return "(" + str(self.var_name) + " : " + str(self.type) + ")"

class Choose(NonEmpty):
    def __init__(self, lhs, rhs):
        # LHS must be ChooseLHS
        self.lhs = lhs
        self.rhs = rhs
    def get_lhs(self):
        return self.lhs
    def get_rhs(self):
        return self.rhs
    def set_rhs(self, rhs):
        self.rhs = rhs
    def prune(self):
        # need to update the choose RHS
        # use the variables that all the way to the left, the arguments to the function
        # check if there are variables used in instances of CallFunc in self.rhs
        #   that are not in self.vars
        #   if so, remove the lowest ast node involving those variable(s)
        return self # TODO
        # rhs_pruned = self.rhs.prune(self.vars) # how to get variables out of LHS? would have to implement for everything
        # return Tru() if rhs_pruned.is_empty() else rhs_pruned
        # TODO think about whether or not this should get mutated
    def __str__(self):
        # def split(list : List) : (List,List) = {
        # choose { (res : (List,List)) => splitSpec(list, res) }
        # }
        # OBSERVE THAT CHOOSE GOES ON THE INSIDE
        return "choose {" + str(self.lhs) + " => " + str(self.rhs) + "}"
    def get_type(self):
        return BOOL # I think? should it be its own type?
    def get_node_type(self):
        return CHOOSE

class Harness(Func):
    # for termination measure purposes, I want choose_cond to be very easy to change
    def __init__(self, name, var_types, ret_type, vars_, choose, body):
        self.name = name
        self.vars = vars_
        self.var_types = var_types
        self.ret_type = ret_type
        self.choose = choose # TODO we need to prune variables that are from outer calls
        self.body = body
    def get_name(self):
        return self.name
    def get_var_types(self):
        return self.var_types
    def get_ret_type(self):
        return self.ret_type
    def get_vars(self):
        return self.vars
    def get_choose(self):
        return self.choose
    def get_body(self):
        return self.body
    def get_function_arguments(self):
        if len(self.vars) == 0:
            return ""

        arguments = ""
        var_types = self.var_types
        for i in range(len(self.vars) -1):
            arguments += str(self.vars[i]) + " : " + str(self.var_types[i]) + ", "
        arguments += str(self.vars[-1]) + " : " + str(self.var_types[-1])
        return arguments
    def __str__(self):
        return "def " + self.name + " (" + self.get_function_arguments() + ") " + ": "\
            + str(self.ret_type) + ' = {\n' + self.add_tabs_body(self.body) + "\n} " + str(self.choose)
    def prune(self):
        # need to update the choose RHS
        # use the variables that all the way to the left, the arguments to the function
        # check if there are variables used in instances of CallFunc in self.rhs
        #   that are not in self.vars
        #   if so, remove the lowest ast node involving those variable(s)
        return self # TODO
        # rhs_pruned = self.ensuring.get_rhs().prune(self.vars) # don't prune over just self.vars, also over stuff in scope in LHS
        # if rhs_pruned.is_empty():
        #     self.ensuring.set_rhs(Tru())
        # else:
        #     self.ensuring.set_rhs(rhs_pruned)
    def get_type(self, envt):
        return self.func.get_type().to_
    def get_node_type(self):
        return HARNESS








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
    # split0 = Harness('split', [LIST], TTuple([LIST, LIST]), ['lst'],
    #     Func('_', [TTuple([LIST, LIST])], BOOL, ['r'],
    #         Eq(App(Var('content'), Var('lst')), StPlus(App(Var('content'), TupleAcc(Var('r'), 0)), App('content', [TupleAcc(Var('r'), 1)])))),
    #     Match(Var('lst'),
    #         Tuple([Nil(), Nil()]),
    #         ['h', 't'], Match(Var('t'),
    #             Tuple([Nil(), Cons(Var('h'), Nil())]),
    #             ['h2', 't2'],
    #             LetIn('v', App(Var('split'), [Var('t2')]),
    #                 Tuple([Cons(Var('h1'), TupleAcc(Var('r'), 1)), Cons(Var('h2'), TupleAcc(Var('r'), 2))])
    #             )
    #         )
    #     )
    # )
    # print(split0)
    # old_choose = Ensuring(Flse(), And(Tru(), Lt(size.get_call(["lst_B"]), size.get_call(["lst_A"]))))
    # harness =  Harness("split", [LIST], INT, ["lst_B"], old_choose, Tru())
    # print(harness)
    # harness.prune()
    # print(harness.get_ensuring())


    pass
    # print(Choose(Annotation("r", Lst(Cons(2, Nil()))), Not(Or(Tru(), Flse()))))
    # print(Match(Lst(Nil()), [Case(Cons(PatternValue("h"), Nil()), Flse())]))
