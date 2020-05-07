INT = "INT"
PATTERN_VALUE = "PATTERN VALUE"
BOOL = "BOOL"
AND = "AND"
NOT = "NOT"
OR = "OR"
FALSE = "FALSE"
TRUE = "TRUE"
LIST = "LIST"
CONS = "CONS"
NIL = "NIL"
CASE = "CASE"
MATCH = "MATCH"
FUNCTION = "FUNCTION"
HOLE = "HOLE"
IF = "IF"
IF_ELSE = "IF ELSE"
VAL = "VAL"
CHOOSE = "CHOOSE"
ANNOTATION = "ANNOTATION"

class Int():
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)
    def get_type(self):
        return INT
    # def evaluate(self):
    #     return self.value

class PatternValue():
    # I don't think we should have actual variables (this will done via Val)
    # but we do need a thing for when we do pattern matching
    def __init__(self, pattern_value):
        self.pattern_value = pattern_value
    def __str__(self):
        return str(self.pattern_value)
    def get_type(self):
        return PATTERN_VALUE

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
        return AND
    # def evaluate(self, environment):
    #     return self.left.evaluate(environment) and self.right.evaluate(environment)

class Or():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "(" + str(self.left) + ")" + " || " + "(" + str(self.right) + ")"
    def get_type(self):
        return OR

class Not():
    def __init__(self, child):
        self.child = child
    def __str__(self):
        return "!" + "(" + str(self.child) + ")"
    def get_type(self):
        return NOT

class Flse():
    def __init__(self):
        self.value = False
    def __str__(self):
        return "false"
    def get_type(self):
        return FALSE

class Tru():
    def __init__(self):
        self.value = True
    def __str__(self):
        return "true"
    def get_type(self):
        return TRUE

class Lst():
    def __init__(self, value):
        self.value = value # Cons or Nil
    def __str__(self):
        return str(self.value)
    def get_type(self):
        return LIST

class Cons():
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr
    def __str__(self):
        return "Cons " + str(self.car) + " " +  str(self.cdr)
    def get_type(self):
        return CONS

class Nil():
    def __str__(self):
        return "Nil"
    def get_type(self):
        return NIL

class Case():
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    def __str__(self):
        return "case " + str(self.lhs) + " => " + str(self.rhs)
    def get_type(self):
        return CASE

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
    def __str__(self):
        return " ?? " # TODO figure this out. this is probably just for our debugging
    def get_type(self):
        return HOLE

class If():
    def __init__(self, condition, tcase):
        self.condition = condition
        self.tcase = tcase
    def __str__(self):
        return "if (" + str(self.condition) + ") {\n\t" + str(self.tcase) + "\n}"
    def get_type(self):
        return IF

class IfElse():
    def __init__(self, condition, tcase, fcase):
        self.condition = condition
        self.tcase = tcase
        self.fcase = fcase
    def __str__(self):
        return "if (" + str(self.condition) + ") {\n\t" + str(self.tcase) + "\n}" + " else {\n\t" + str(self.fcase) + "\n}"
    def get_type(self):
        return IF_ELSE

class Val():
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __str__(self):
        return "val " + str(self.name) + " = " + str(self.value)
    def get_type(self):
        return VAL

class Choose():
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    def __str__(self):
        return "choose {" + "(" + str(self.lhs) + ")" + " => " + str(self.rhs) + "}"
    def get_type(self):
        return CHOOSE

class Annotation():
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __str__(self):
        return str(self.name) + " : " + str(self.value)
    def get_type(self):
        return ANNOTATION

# TODO content and set?

if __name__ == '__main__':
    # print(Choose(Annotation("r", Lst(Cons(2, Nil()))), Not(Or(Tru(), Flse()))))
    print(Match(Lst(Nil()), [Case(Cons(PatternValue("h"), Nil()), Flse())]))
