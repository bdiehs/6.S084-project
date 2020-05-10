from ast import *
ARITHMETIC_OPERATIONS = {PLUS, MINUS, LT, LEQ, EQ}
ARITHMETIC_OPERATIONS_SYMBOLS = {PLUS : '+', MINUS : '-', LT : '<', LEQ : '<=', EQ : '='}
TWO_BOOLEAN_OPERATIONS = {AND, OR}
SPACE = " "

class Visitor():
    # needs on for each type of node
    def call_leon(self):
        # TODO, execute bash script and read in from file
        return ""
    def on(self, node, can_call_leon = True, environment = Set(), outer_function = None):
        if node.get_node_type() == VAR:
            return str(node)
        if node.get_node_type() == INT:
            return str(node)
        if node.get_node_type() in ARITHMETIC_OPERATIONS:
            left = on(node.get_left(), can_call_leon = False, environment = environment, outer_function = outer_function)
            right = on(node.get_right(), can_call_leon = False, environment = environment, outer_function = outer_function)
            return "(" + left + SPACE + ARITHMETIC_OPERATIONS_SYMBOLS[node.get_type()] + SPACE + right + ")"
        if node.get_node_type() in TWO_BOOLEAN_OPERATIONS:
            left = on(node.get_left, can_call_leon = False, environment = environment, outer_function = outer_function)
            right = on(node.get_right, can_call_leon = False, environment = environment, outer_function = outer_function)
            pass

        # TODO other boolean stuff
        # lists, match
        # hard thing: hole
        if node.get_node_type() == HOLE:
            # are we inside a recursive call? need to do measure stuff and pruning
            # in the easiest case, this is just a hole like ??? or an ensuring
            # we are going to make a call to Leon to fill this hole right now
            # what if holes are not independent, like holes w/i holes?
            # well the first one we hit is an outer hole anyway
            # need to give leon the environment
            pass
