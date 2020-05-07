INT = "INT"
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
