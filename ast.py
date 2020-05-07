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
    def __type__(self):
        return INT
    def get_value(self):
        return self.value
