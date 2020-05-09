import ast

# goal
# have a recursive data type, which is always a list in our case
# the list is used in a function that recursively calls itself
# let A be outer call and B be inner recursive call
# in A, have lst_A, in B, have lst_B
# must check that size(lst_B) < size(lst_A)
# we talked about this this morning...
# options: inside B, we dynamically do some assert that size(lst_B) < size(lst_A) (seems hard and bad)
# better: dynamically asserting stuff isn't really thing because we're just printing printing
# so all asserts happen in the form of chooses
# probably this is in the choose for B (yeah has to be)
# so if B is a recursive call:
    # have a termination measure (like check it)
    # like P && size(lst_B) < size(lst_A) , where P is the old predicate
# we need a way to check if a function is a recursive call
    # should be easy enough
    # if yes, stuff termination measure condition into the choose
# separate things TODO:
    # detect recursive calls. this is done while traversing the AST
    # stuffing termination measure condition into the choose

class TerminationMeasure():
    def __init__(self, termination_measure):
        # termination measure is some function, like size
        # we assume it's a function of one argument
        # we could accumulate a really big choose as we keep recursing
        # need to prune somehow. older variables will be out of scope
        self.termination_measure = termination_measure
    def get_measure(self):
        return self.termination_measure # maybe rep exposure if Func becomes mutable later but copying is hard
    def __str__(self):
        return str(self.termination_measure)
    def add_to_choose(self, old_choose, old_name, new_name):
        # need to modify a choose, instance of Choose
        # add new thing to RHS, because that's how it'll actually be asserted
        # termination_assertion = evaluate self.termination_measure on new_name < self.termination_measure on old_name
        old_termination = self.termination_measure.get_call([old_name])
        new_termination = self.termination_measure.get_call([new_name])
        new_choose = ast.Choose(old_choose.get_lhs(), ast.And(old_choose.get_rhs(), ast.Lt(new_termination, old_termination)))
        # new_choose = ast.Choose(ast.And(old_choose.get_lhs(), ast.Lt(new_termination, old_termination)), old_choose.get_rhs())
        return new_choose

if __name__ == '__main__':
    size = ast.Func('size', [ast.LIST], ast.INT, ['lst'],
        ast.Match(ast.Var('lst'),
            ast.Int(0),
            ['_', 'rest'], ast.Plus(ast.Int(1), ast.App(ast.Var('size'), [ast.Var('rest')]))
        )
    )
    term_measure = TerminationMeasure(size)
    old_choose = ast.Choose(ast.Flse(), ast.Tru())
    new_choose = term_measure.add_to_choose(old_choose, "lst_A", "lst_B")
    print(new_choose)
