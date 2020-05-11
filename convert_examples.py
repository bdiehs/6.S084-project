from ast import *
OUTPUT = "OUTPUT"

class InputOutputExamples():
    def __init__(self, inputs_outputs, return_var_name, return_type):
        # input outputs is a list of dictionaries
        # each dictoinary maps variable names to values
        self.inputs_outputs = inputs_outputs
        self.return_var_name = return_var_name
        self.return_type = return_type
    def _make_big_and(self, assignments):
        if len(assignments) == 0:
            return Tru()
        if len(assignments) == 1:
            key = list(assignments.keys())[0]

            return Eq(key, assignments[key]) if key != OUTPUT else Tru()
        first_name = list(assignments.keys())[0]
        if first_name != OUTPUT:
            print("use first name " + first_name)
            first_assertion = Eq(first_name, assignments[first_name])
        del assignments[first_name]
        return And(first_assertion, self._make_big_and(assignments))
    def get_choose(self):
        # need to make rhs, bunch of if elses
        first_assignments = self.inputs_outputs[0]
        first_big_and = self._make_big_and(first_assignments.copy())
        outer_if = If(first_big_and, Eq(self.return_var_name, first_assignments[OUTPUT]))

        for assignments in self.inputs_outputs[1:]:
            big_and = self._make_big_and(assignments.copy())
            new_if = If(big_and, Eq(self.return_var_name, assignments[OUTPUT]))
            outer_if.set_false_case(new_if)

        chooseLHS = ChooseLHS(self.return_var_name, self.return_type)
        choose = Choose(chooseLHS, outer_if)
        return choose

if __name__ == '__main__':
    input_outputs = [{"x" : 1, OUTPUT : 2}, {"x" : 2, OUTPUT : 3}]
    input_output_examples = InputOutputExamples(input_outputs, "res", INT)
    print(input_output_examples.get_choose())
