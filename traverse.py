from ast import *
ARITHMETIC_OPERATIONS = {PLUS, MINUS, LT, LEQ, EQ}
ARITHMETIC_OPERATIONS_SYMBOLS = {PLUS : '+', MINUS : '-', LT : '<', LEQ : '<=', EQ : '='}
TWO_BOOLEAN_OPERATIONS = {AND, OR}
BOOLEAN_OPERATIONS_SYMBOLS = {AND : "&&", OR : "||"}
SPACE = " "

class Visitor():
    # needs on for each type of node
    def call_leon(self, node, environment, outer_function):
        # TODO, execute bash script and read in from file
        return ""
    def on(self, node, can_call_leon = True, environment = Set(), outer_function = None):
        # if there was a hole in a subtree and the node couldn't get a program for itself,
        # need to pass that info up to parent
        # return (string for program, boolean) ?
        # return string or None ?
        if node.get_node_type() == VAR:
            return str(node)
        if node.get_node_type() == INT:
            return str(node)
        if node.get_node_type() in ARITHMETIC_OPERATIONS:
            left = on(node.get_left(), can_call_leon = False, environment = environment, outer_function = outer_function)
            right = on(node.get_right(), can_call_leon = False, environment = environment, outer_function = outer_function)

            if (left == None or right == None) and (not can_call_leon):
                return None
            if left != None and right != None:
                return "(" + left + SPACE + ARITHMETIC_OPERATIONS_SYMBOLS[node.get_type()] + SPACE + right + ")"
            # at least one is None
            if not can_call_leon:
                return None
            # at least one is None and can call leon: do it
            return self.call_leon(node, environment, outer_function)
        if node.get_node_type() in TWO_BOOLEAN_OPERATIONS:
            left = on(node.get_left(), can_call_leon = False, environment = environment, outer_function = outer_function)
            right = on(node.get_right(), can_call_leon = False, environment = environment, outer_function = outer_function)

            if (left == None or right == None) and (not can_call_leon):
                return None
            if left != None and right != None:
                return "(" + left + SPACE + BOOLEAN_OPERATIONS_SYMBOLS[node.get_type()] + SPACE + right + ")"
            if not can_call_leon:
                return None
            return self.call_leon(node, environment, outer_function)
        if node.get_node_type() == NOT:
            child = on(node.get_child(), can_call_leon = can_call_leon, environment = environment, outer_function = outer_function)
            if child != None:
                return child
            if child == None and (not can_call_leon):
                return None
            return self.call_leon(node, environment, outer_function)
        if node.get_node_type() == FALSE or node.get_node_type == TRUE:
            return str(node)
        



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
