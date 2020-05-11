from ast import *
from convert_examples import *
from traverse import *

def main(name, var_types, ret_type, vars_, examples, body, return_var_name = "res"):
    input_outputs = InputOutputExamples(examples, return_var_name, ret_type)
    choose = input_outputs.get_choose()
    harness = Harness(name, var_types, ret_type, vars_, choose, body)
    visitor = Visitor()
    print(harness.accept(visitor))

if __name__ == '__main__':
    input_outputs = [{"x" : 1, OUTPUT : 2}, {"x" : 2, OUTPUT : 3}]
    var_types = [INT]
    main("foo", [INT], INT, [Var("x")], input_outputs, body = Empty())
