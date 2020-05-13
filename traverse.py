from ast import *
import subprocess
ARITHMETIC_OPERATIONS = {PLUS, MINUS, LT, LEQ, EQ}
ARITHMETIC_OPERATIONS_SYMBOLS = {PLUS : '+', MINUS : '-', LT : '<', LEQ : '<=', EQ : '='}
TWO_BOOLEAN_OPERATIONS = {AND, OR}
BOOLEAN_OPERATIONS_SYMBOLS = {AND : "&&", OR : "||"}
SPACE = " "

LEON_IMPORTS = "import leon.annotation._\nimport leon.lang._\nimport leon.lang.synthesis._\n\n"
DECLARE_OBJECT = "object Complete {\n"
DECLARE_LISTS = "sealed abstract class List\ncase class Cons(head: BigInt, tail: List) extends List\ncase object Nil extends List\n"
CLOSE_OBJECT = "\n}"

SIZE_CONS_CASE = ConsCase("_", "rest", Plus(Int(1), App(Var('size'), [Var('rest')])))
SIZE = Func('size', FuncType([LIST], INT), ['lst'],
    Match(Var('lst'),
        Int(0),
        SIZE_CONS_CASE)
)

class Visitor():
    # TODO might need to change strs of types
    def __init__(self, environment, outer_function):
        self.environment = environment
        self.outer_function = outer_function
    def add_tabs_body(self, body):
        body_lines = str(body).split("\n")
        if len(body_lines) == 0:
            return ""
        tabbed_body = ""
        for line in body_lines[:-1]:
            tabbed_body += SCALA_TAB + line + "\n"
        tabbed_body += SCALA_TAB + body_lines[-1]
        return tabbed_body

    def _get_environment_lines(self, environment):
        envt_lines = ""
        for name, value in environment.items():
            # we don't want the val thing if it's a function
            if value.get_node_type() != FUNC:
                envt_lines += 'val ' + name + ' = ' + str(value) + '\n'
            else:
                envt_lines += str(value) + '\n'
        return envt_lines

    def get_func_str(self, node, environment, outer_function, choose, variable_name = None):
        # returns function signature
        if node.get_node_type() == HOLE:
            hole_type = node.get_type()
            if not hole_type.is_func_type():
                print("HOLE, NON FUNC")
                # hole, not functional
                # str(node) for a type seems buggy
                return "def " + hole_name + "() : " + str(node) + " = {\n"
            print("HOLE, FUNC")
            return "def " + hole_name + "(" + hole_type.get_function_arguments() + ") : " + str(hole_type.get_ret_type()) + " = {\n"
        if node.get_node_type() != FUNC:
            print("NON HOLE, NON FUNC")
            # non hole, non functional
            return "def hole(" + variable_name + " : " + str(node.get_type())  + ")" + " : " + str(node.get_type(environment)) + " = {\n"
        # non hole, functional
        print("NON HOLE, FUNC")
        return "def hole(" + hole_type.get_function_arguments() + ") : " + str(node.get_func_type().get_ret_type()) + "= {\n"

    def get_choose_func_non_hole(self, node, outer_function, choose):
        if outer_function == None or outer_function.get_name() != node.get_name():
            return str(choose.prune())
        else:
            new_choose = node.get_choose().prune()
            # termination measure is if any of the args is a list, it needs to be smaller
            # need to change names
            current_vars = node.get_vars()
            current_var_types = node.get_func_type().get_var_types()
            outer_vars = outer_function.get_vars()
            outer_var_types = outer_function.get_func_type().get_var_types()

            new_choose = choose
            for i in range(len(current_var_types)):
                if current_var_types[i] == LIST:
                    renamed_current_var = current_vars[i] + "'" # make it prime
                    measure = Lt(SIZE(renamed_current_var), SIZE(outer_vars[i]))
                    termination_measure = TerminationMeasure(SIZE)
                    new_choose = termination_measure.add_to_choose(new_choose, outer_vars[i], renamed_current_var)
            return new_choose

    # TODO how to use other variables in the RHS of the choose?
    def get_leon_call(self, node, environment, outer_function, choose, variable_name):
        # TODO, execute bash script and read in from file
        # this might've been a bad idea to send the node, here, now need to type check again? would change that
        # need the signature (type of hole)
        # need to do termination stuff
        # need to apply the choose
        # need to use the environment. need to build up lines of vals for that DONE
        leon_call = ""
        envt_lines = self._get_environment_lines(environment)
        leon_call += envt_lines # hopefully it's right for those to be outside the function?
        func_str = self.get_func_str(node, environment, outer_function, choose, variable_name) # includes the "{" for now
        leon_call += func_str
        # now just need to do choose. no body!

        if node.get_type() == HOLE or node.get_node_type() != FUNC:
            choose_str = str(choose.prune())
        else:
            # complicated choose
            choose_str = get_choose_func_non_hole(self, node, outer_function, choose)
        leon_call += SCALA_TAB + choose_str
        leon_call += "\n}\n"
        return leon_call

    def harness_call_leon(self, input_program):
        # this is not SFB or RFC
        leon_call = input_program
        print("(harness) Going to call Leon with\n", leon_call)
        leon_call = self.add_tabs_body(leon_call)
        leon_call = LEON_IMPORTS + DECLARE_OBJECT + DECLARE_LISTS + leon_call + CLOSE_OBJECT

        f = open("input_program.txt", "w")
        f.write(leon_call)
        f.close()

        subprocess.run("./run.sh")

        result_file = open("output_program.scala", "r")
        result_program = result_file.read()
        result_file.close()

    def call_leon(self, node, environment, outer_function, choose, variable_name = None):
        print("Leon call on node: ", node)
        leon_call = self.get_leon_call(node, environment, outer_function, choose, variable_name)
        print("(nonharness) Going to call Leon with \n", leon_call)
        leon_call = self.add_tabs_body(leon_call)
        leon_call = LEON_IMPORTS + DECLARE_OBJECT + DECLARE_LISTS + leon_call + CLOSE_OBJECT
        # TODO actually run the script
        # have program string from leon_call
        # write that to a file
        # run the bash script which writes a program to file, read in from that file
        # need to write to file that bash script reads in from.
        f = open("input_program.txt", "w")
        f.write(leon_call)
        f.close()

        subprocess.run("./run.sh")

        result_file = open("output_program.scala", "r")
        result_program = result_file.read()
        result_file.close()
        quit()
        # at the highest level (harness), we probably want to write our string to a file too
        return result_program # for now
    def on(self, node, can_call_leon = True, environment = {}, outer_function = None, choose = None):
        print("on envt", environment)
        if node.get_node_type() == EMPTY:
            return str(node)
        if node.get_node_type() == VAR:
            return str(node)
        if node.get_node_type() == INT:
            return str(node)
        if node.get_node_type() in ARITHMETIC_OPERATIONS:
            left = self.on(node.get_left(), can_call_leon = False, environment = environment, outer_function = outer_function, choose = choose)
            right = self.on(node.get_right(), can_call_leon = False, environment = environment, outer_function = outer_function, choose = choose)

            if (left == None or right == None) and (not can_call_leon):
                return None
            if left != None and right != None:
                return "(" + left + SPACE + ARITHMETIC_OPERATIONS_SYMBOLS[node.get_type()] + SPACE + right + ")"
            # at least one is None
            if not can_call_leon:
                return None
            # at least one is None and can call leon: do it
            return self.call_leon(node, environment, outer_function, choose)
        if node.get_node_type() in TWO_BOOLEAN_OPERATIONS:
            left = self.on(node.get_left(), can_call_leon = False, environment = environment, outer_function = outer_function, choose = choose)
            right = self.on(node.get_right(), can_call_leon = False, environment = environment, outer_function = outer_function, choose = choose)

            if (left == None or right == None) and (not can_call_leon):
                return None
            if left != None and right != None:
                return "(" + left + SPACE + BOOLEAN_OPERATIONS_SYMBOLS[node.get_type()] + SPACE + right + ")"
            if not can_call_leon:
                return None
            return self.call_leon(node, environment, outer_function, choose)
        if node.get_node_type() == NOT:
            child = self.on(node.get_child(), can_call_leon = can_call_leon, environment = environment, outer_function = outer_function, choose = choose)
            if child != None:
                return child
            if child == None and (not can_call_leon):
                return None
            return self.call_leon(node, environment, outer_function, choose)
        if node.get_node_type() == FALSE or node.get_node_type == TRUE:
            return str(node)
        if node.get_node_type() == CONS:
            car = self.on(node.get_car(), can_call_leon = can_call_leon, environment = environment, outer_function = outer_function, choose = choose)
            cdr = self.on(node.get_cdr(), can_call_leon = can_call_leon, environment = environment, outer_function = outer_function, choose = choose)
            if car != None and cdr != None:
                return "Cons " + car + SPACE + cdr
            if not can_call_leon:
                return None
            return self.call_leon(node, environment, outer_function, choose)
        if node.get_node_type() == NIL:
            return str(node)
        if node.get_node_type() == MATCH:
            match_on = self.on(node.get_match_on(), can_call_leon = False, environment = environment, outer_function = outer_function, choose = choose)
            nil_case = self.on(node.get_nil_case(), can_call_leon = False, environment = environment, outer_function = outer_function, choose = choose)
            cons_case = self.on(node.get_cons_case().cons_case, can_call_leon = False, environment = environment, outer_function = outer_function, choose = choose)

            if match_on == None or (nil_case == None and cons_case == None):
                # if the thing we're matching on is a hole, have to call leon
                # if both the cases are holes, have to be solved together, have to call leon
                if not can_call_leon:
                    return None
                return self.call_leon(node, environment, outer_function, choose, str(node.get_match_on()))
            if nil_case == None:
                nil_case = self.call_leon(node.get_nil_case(), environment, outer_function, choose, str(node.get_match_on()))
            if cons_case == None:
                cons_case = self.call_leon(node.get_cons_case(), environment, outer_function, choose, str(node.get_match_on()))

            result = match_on + " match {\n" + SCALA_TAB
            result += "case Nil => " + nil_case + "\n" + SCALA_TAB
            result += cons_case
            result += "\n}"
            return result

        if node.get_node_type() == SET:
            new_vals = [self.on(val, can_call_leon, environment, outer_function) for val in node.get_vals()]
            if None not in new_vals:
                return "Set(" + list_str(new_vals) + ")"
            if not can_call_leon:
                return None
            return self.call_leon(node, can_call_leon, environment, outer_function, choose)
        if node.get_node_type() == SET_PLUS:
            left = self.on(node.get_left(), can_call_leon = False, environment = environment, outer_function = outer_function, choose = choose)
            right = self.on(node.get_right(), can_call_leon = False, environment = environment, outer_function = outer_function, choose = choose)

            if (left == None or right == None) and (not can_call_leon):
                return None
            if left != None and right != None:
                return "(" + left + SPACE + "++" + SPACE + right + ")"
            if not can_call_leon:
                return None
            return self.call_leon(node, environment, outer_function, choose)
        if node.get_node_type() == FUNC:
            # TODO only most recent function call matters, right?
            # TODO need to handle recursive stuff
            if outer_function != None and node.get_name() == outer_function.get_name():
                # recursive call, must handle measure stuff
                pass # TODO fix termination which is currently broken
            body = self.on(node.get_body(), can_call_leon = can_call_leon, environment = environment, outer_function = node, choose = choose)
            if body != None:
                return body
            if not can_call_leon:
                return None
            return self.call_leon(node, environment, outer_function, choose)
        if node.get_node_type() == CALL_FUNC:
            return str(node)
        # TODO app
        if node.get_node_type() == LET_IN:
            val = self.on(node.get_val(), can_call_leon = can_call_leon, environment = environment, outer_function = outer_function, choose = choose)
            environment[node.get_var_name()] = val
            body = self.on(node.get_body(), can_call_leon = can_call_leon, environment = environment, outer_function = outer_function, choose = choose)
            if val != None and body != None:
                return 'val ' + node.get_var_name() + ' = ' + val + '\n' + body
        if node.get_node_type() == TUPLE:
            new_vals = [self.on(val, can_call_leon, environment, outer_function) for val in node.get_vals()]
            if None not in new_vals:
                return list_str(new_vals)
            if not can_call_leon:
                return None
            return self.call_leon(node, can_call_leon, environment, outer_function, choose)
        if node.get_node_type() == TUPLE_ACC:
            # do we need everything in the tuple to be resolvable? probably.
            new_val = self.on(node.tuple, can_call_leon, environment, outer_function)
            if new_val != None:
                return "(" + str(new_val) + ")" + '._' + str(node.get_idx())
            if not can_call_leon:
                return None
            return self.call_leon(node, environment, outer_function, choose)
        if node.get_node_type() == HARNESS:
            new_body = self.on(node.get_body(), can_call_leon = True, environment = self.environment, outer_function = self.outer_function, choose = node.get_choose())
            input_program = "def " + node.get_name() + " (" + node.get_function_arguments() + ") " + ": "\
                + str(node.ret_type) + ' = {\n' + node.add_tabs_body(new_body) + str(node.get_choose()) + "\n} "
            # TODO for harness, need to actually call leon!
            return self.harness_call_leon(input_program)
        if node.get_node_type() == HOLE:
            # are we inside a recursive call? need to do measure stuff and pruning
            if not can_call_leon:
                return None
            return self.call_leon(node, environment, outer_function, choose)

if __name__ == '__main__':
    visitor = Visitor()
    # node = Hole(FuncType([INT], INT))
    # TODO how to represent empty body?
    # node = Func("foo", FuncType([INT], INT), ["x"], Int(0))
    # # node = Hole(INT)
    # # node = Hole(INT)
    # # environment = {"x" : Int(0)} # environment works!
    # environment = {}
    # outer_function = None
    # choose = Choose(ChooseLHS("res", INT), Tru()) # want to say res = input * 2
    # call = visitor.call_leon(node, environment, outer_function, choose)
    # print(call)

    # traversing tree w/ harness
    choose = Choose(ChooseLHS("res", INT), Eq("res", Plus(Int(1), "x")))
    # need empty body
    harness = Harness("foo", [INT], INT, ["x"], choose, Empty())
    result = harness.accept(visitor)
    print(result)
