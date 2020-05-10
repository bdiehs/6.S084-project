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
    def on(self, node, can_call_leon = True, environment = {}, outer_function = None, ensuring = None):
        # if there was a hole in a subtree and the node couldn't get a program for itself,
        # need to pass that info up to parent
        # return (string for program, boolean) ?
        # return string or None ?
        if node.get_node_type() == VAR:
            return str(node)
        if node.get_node_type() == INT:
            return str(node)
        if node.get_node_type() in ARITHMETIC_OPERATIONS:
            left = on(node.get_left(), can_call_leon = False, environment = environment, outer_function = outer_function, ensuring = ensuring)
            right = on(node.get_right(), can_call_leon = False, environment = environment, outer_function = outer_function, ensuring = ensuring)

            if (left == None or right == None) and (not can_call_leon):
                return None
            if left != None and right != None:
                return "(" + left + SPACE + ARITHMETIC_OPERATIONS_SYMBOLS[node.get_type()] + SPACE + right + ")"
            # at least one is None
            if not can_call_leon:
                return None
            # at least one is None and can call leon: do it
            return self.call_leon(node, environment, outer_function, ensuring)
        if node.get_node_type() in TWO_BOOLEAN_OPERATIONS:
            left = on(node.get_left(), can_call_leon = False, environment = environment, outer_function = outer_function, ensuring = ensuring)
            right = on(node.get_right(), can_call_leon = False, environment = environment, outer_function = outer_function, ensuring = ensuring)

            if (left == None or right == None) and (not can_call_leon):
                return None
            if left != None and right != None:
                return "(" + left + SPACE + BOOLEAN_OPERATIONS_SYMBOLS[node.get_type()] + SPACE + right + ")"
            if not can_call_leon:
                return None
            return self.call_leon(node, environment, outer_function, ensuring)
        if node.get_node_type() == NOT:
            child = on(node.get_child(), can_call_leon = can_call_leon, environment = environment, outer_function = outer_function, ensuring = ensuring)
            if child != None:
                return child
            if child == None and (not can_call_leon):
                return None
            return self.call_leon(node, environment, outer_function, ensuring)
        if node.get_node_type() == FALSE or node.get_node_type == TRUE:
            return str(node)
        if node.get_node_type() == CONS:
            car = on(node.get_car(), can_call_leon = can_call_leon, environment = environment, outer_function = outer_function, ensuring = ensuring)
            cdr = on(node.get_cdr(), can_call_leon = can_call_leon, environment = environment, outer_function = outer_function, ensuring = ensuring)
            if car != None and cdr != None:
                return "Cons " + car + SPACE + cdr
            if not can_call_leon:
                return None
            return self.call_leon(node, environment, outer_function, ensuring)
        if node.get_node_type() == NIL:
            return str(node)
        if node.get_node_type() == MATCH:
            # TODO add cons case to other stuff? or nah... should never exist in the wild
            match_on = on(node.get_match_on(), can_call_leon = False, environment = environment, outer_function = outer_function, ensuring = ensuring)
            nil_case = on(node.get_nil_case(), can_call_leon = False, environment = environment, outer_function = outer_function, ensuring = ensuring)
            cons_case = on(node.get_cons_case(), can_call_leon = False, environment = environment, outer_function = outer_function, ensuring = ensuring)
            if match_on != None and nil_case != None and cons_case != None:
                result = match_on + " match {\n" + SCALA_TAB
                result += "case Nil => " + nil_case + "\n" + SCALA_TAB
                result += cons_case
                result += "\n}"
                return result
            if not can_call_leon:
                return None
            return self.call_leon(node, environment, outer_function, ensuring)
        # TODO set and set plus
        if node.get_node_type() == FUNC:
            # TODO only most recent function call matters, right?
            # TODO need to handle recursive stuff
            if outer_function != None and node.get_name() == outer_function.get_name():
                # recursive call, must handle measure stuff
                pass # TODO fix termination which is currently broken
            body = on(node.get_body(), can_call_leon = can_call_leon, environment = environment, outer_function = node, ensuring = ensuring)
            if body != None:
                return body
            if not can_call_leon:
                return None
            return self.call_leon(node, environment, outer_function, ensuring)
        if node.get_node_type() == CALL_FUNC:
            return str(node)
        # TODO app
        if node.get_node_type() == LET_IN:
            val = on(node.get_val(), can_call_leon = can_call_leon, environment = environment, outer_function = outer_function, ensuring = ensuring)
            environment[node.get_var_name()] = val
            body = on(node.get_body(), can_call_leon = can_call_leon, environment = environment, outer_function = outer_function, ensuring = ensuring)
            if val != None and body != None:
                return 'val ' + node.get_var_name() + ' = ' + val + '\n' + self.body
        if node.get_node_type() == TUPLE:
            new_vals = [on(val, can_call_leon, environment, outer_function) for val in node.get_vals()]
            if None not in new_vals:
                return list_str(new_vals)
            if not can_call_leon:
                return None
            return self.call_leon(node, can_call_leon, environment, outer_function, ensuring)
        if node.get_node_type() == TUPLE_ACC:
            # do we need everything in the tuple to be resolvable? probably.
            new_vals = [on(val, can_call_leon, environment, outer_function) for val in node.get_vals()]
            if None not in new_vals:
                return "(" + list_str(new_vals) + ")" + '[' + str(node.get_idx()) + ']'
            if not can_call_leon:
                return None
            return self.call_leon(node, environment, outer_function, ensuring)
        if node.get_node_type() == ENSURING:
            # do I have to prune stuff here?
            return str(node) # there's never any holes in an ensuring, right?
        if node.get_node_type() == HARNESS:
            new_body = on(node.get_body(), can_call_leon = True, environment = {}, outer_function = None, ensuring = node.get_ensuring())
            ensuring = on(node.get_ensuring(), can_call_leon = True, environment = {}, outer_function = None, ensuring = node.get_ensuring())
            return "def " + node.get_name() + " (" + node.get_function_arguments() + ") " + ": "\
                + str(self.ret_type) + ' = {\n' + node.add_tabs_body(new_body) + "\n} " + ensuring
        if node.get_node_type() == HOLE:
            # are we inside a recursive call? need to do measure stuff and pruning
            if not can_call_leon:
                return None
            return self.call_leon(node, environment, outer_function, ensuring)
