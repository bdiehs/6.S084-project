from ast import *
ARITHMETIC_OPERATIONS = {PLUS, MINUS, LT, LEQ, EQ}
ARITHMETIC_OPERATIONS_SYMBOLS = {PLUS : '+', MINUS : '-', LT : '<', LEQ : '<=', EQ : '='}
TWO_BOOLEAN_OPERATIONS = {AND, OR}
BOOLEAN_OPERATIONS_SYMBOLS = {AND : "&&", OR : "||"}
SPACE = " "

SIZE_CONS_CASE = ConsCase("_", "rest", Plus(Int(1), App(Var('size'), [Var('rest')])))
SIZE = Func('size', FuncType([LIST], INT), ['lst'],
    Match(Var('lst'),
        Int(0),
        SIZE_CONS_CASE)
)

class Visitor():
    # needs on for each type of node
    def get_leon_call_non_func(self, node, environment, ensuring):
        # not a hole. could be from inside a hole. not a function.
        # get everything for leon call after the environment?
        leon_call = ""
        envt_lines = ""
        for name, value in environment.items():
            envt_lines += 'val ' + name + ' = ' + str(value) + '\n'
        leon_call += envt_lines # hopefully it's right for those to be outside the function?
        function_str = "def hole() : " + str(node.get_type()) + " = {\n}"
        leon_call += function_str
        leon_call += SPACE + str(ensuring) # node.get_ensuring().prune() ?? shouldn't be needed here
        return leon_call

    def get_leon_call_func_non_hole(self, node, environment, outer_function, ensuring):
        # TODO separate thing for a hole func. need to come up with variable names
        leon_call = ""

        envt_lines = ""
        for name, value in environment.items():
            envt_lines += 'val ' + name + ' = ' + str(value) + '\n'
        leon_call += envt_lines # hopefully it's right for those to be outside the function?

        function_str = "def hole(" + node.get_function_arguments() + ") : " + str(node.get_func_type().get_ret_type()) + "{\n}"
        if outer_function == None or outer_function.get_name() != node.get_name():
            function_str += str(ensuring.prune())
        else:
            new_ensuring = node.get_ensuring().prune()
            # termination measure is if any of the args is a list, it needs to be smaller
            # need to change names
            current_vars = node.get_vars()
            current_var_types = node.get_func_type().get_var_types()
            outer_vars = outer_function.get_vars()
            outer_var_types = outer_function.get_func_type().get_var_types()

            new_ensuring = ensuring
            for i in range(len(current_var_types)):
                if current_var_types[i] == LIST:
                    renamed_current_var = current_vars[i] + "'" # make it prime
                    measure = Lt(SIZE(renamed_current_var), SIZE(outer_vars[i]))
                    termination_measure = TerminationMeasure(SIZE)
                    new_ensuring = termination_measure.add_to_choose(new_ensuring, outer_vars[i], renamed_current_var)
            function_str += SPACE + new_ensuring
        leon_call += function_str
        return leon_call

    def get_leon_call_hole_func(self, hole_type, environment, outer_function, ensuring):
        # TODO separate thing for a hole func. need to come up with variable names
        # hole_type is a FuncType
        leon_call = ""
        envt_lines = ""
        for name, value in environment.items():
            envt_lines += 'val ' + name + ' = ' + str(value) + '\n'
        leon_call += envt_lines # hopefully it's right for those to be outside the function?

        function_str = "def hole(" + hole_type.get_function_arguments() + ") : " + str(hole_type.get_ret_type()) + "{\n}"

        # now here is a problem: we don't know if the hole is recursive or not
        # we assume it's not
        # I guess should always prune just in case
        pruned_ensuring = ensuring.prune()
        function_str += str(pruned_ensuring)
        leon_call += function_str
        return leon_call

    def get_leon_call(self, node, environment, outer_function, ensuring):
        # TODO, execute bash script and read in from file
        # this might've been a bad idea to send the node, here, now need to type check again? would change that
        # need the signature (type of hole)
        # need to do termination stuff
        # need to apply the ensuring
        # need to use the environment. need to build up lines of vals for that DONE
        leon_call = ""
        envt_lines = ""
        for name, value in environment.items():
            envt_lines += 'val ' + name + ' = ' + str(value) + '\n'
        leon_call += envt_lines # hopefully it's right for those to be outside the function?

        # ensuring stuff and termination stuff
        print("node type " + node.get_node_type())
        if node.get_node_type() == HOLE:
            hole_type = node.get_type()
            if not hole_type.is_func_type():
            # if hole_type.get_node_type() != FUNC_TYPE:
                return self.get_leon_call_non_func(hole_type, environment, ensuring)
            else:
                # function inside hole. last case to figure out!
                return self.get_leon_call_hole_func(hole_type, environment, outer_function, ensuring)
        else:
            # non hole.
            if node.get_node_type() != FUNC:
                # TODO figure out environment stuff??/
                function_str = "def hole() : " + str(node.get_type(environment)) + " = {\n}"
                leon_call += function_str
                leon_call += SPACE + str(ensuring)
                return leon_call
            else:
                return self.get_leon_call_func_non_hole(node, environment, outer_function, ensuring)

    def call_leon(self, node, environment, outer_function, ensuring):
        leon_call = self.get_leon_call(node, environment, outer_function, ensuring)
        # TODO actually run the script
        return leon_call # for now
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

if __name__ == '__main__':
    visitor = Visitor()
    # node = Hole(FuncType([INT], INT))
    # TODO how to represent empty body?
    # node = Func("foo", FuncType([], INT), [], Int(0))
    # node = Hole(INT)
    node = Plus(Hole(INT), Int(5))
    environment = {"x" : Int(0)}
    outer_function = None
    ensuring = Ensuring(Flse(), Tru())
    call = visitor.get_leon_call(node, environment, outer_function, ensuring)
    print(call)
