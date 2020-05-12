from ast import *
from traverse import *



size = Func('size', FuncType([LIST], INT) , ['lst'],
    Match(Var('lst'),
        Int(0),
        ConsCase('_', 'rest', Plus(Int(1), CallFunc('size', [Var('rest')], INT)))
    )
)

# sets in scala need to have type. TODO
content = Func('content', FuncType([LIST], SET) , ['lst'],
    Match(Var('lst'),
        St([]),
        ConsCase('e', 'rest', StPlus(St([Var('e')]), CallFunc('content', [Var('rest')], SET)))
    )
)


split_spec = Choose(ChooseLHS('r', TTuple([LIST, LIST])),
	Eq(content.get_call(['lst']),
		StPlus(content.get_call([TupleAcc(Var('r'), 1)]), content.get_call([TupleAcc(Var('r'), 2)]))))

split0 = Harness('split', [LIST], TTuple([LIST, LIST]), ['lst'], split_spec,
	Match(Var('lst'),
		nil_case = Tuple([Nil(), Nil()]),
		cons_case = ConsCase('h', 't', Match(Var('t'),
			nil_case = Tuple([Nil(), Cons(Var('h'), Nil())]),
			cons_case = ConsCase('h2', 't2',
				LetIn('v', CallFunc('split', [Hole(LIST)], TTuple([LIST, LIST])),
				Tuple([Cons(Var('h1'), TupleAcc(Var('r'), 1)), Cons(Var('h2'), TupleAcc(Var('r'), 1))])
				))
		))
	))

splitf = Func('split', FuncType([LIST], TTuple([LIST, LIST])), ['lst'],
	Match(Var('lst'),
		nil_case = Hole(TTuple([LIST, LIST])),
		cons_case = ConsCase('h', 't', Match(Var('t'),
			nil_case = Tuple([Nil(), Cons(Var('h'), Nil())]),
			cons_case = ConsCase('h2', 't2',
				LetIn('v', CallFunc('split', [Hole(LIST)], TTuple([LIST, LIST])),
				Tuple([Cons(Var('h1'), TupleAcc(Var('r'), 1)), Cons(Var('h2'), TupleAcc(Var('r'), 1))])
				))
		))
	))


# old_choose = Ensuring(Flse(), And(Tru(), Lt(size.get_call(["lst_B"]), size.get_call(["lst_A"]))))
# harness =  Harness("split", [LIST], INT, ["lst_B"], old_choose, Tru())

def test_traverse():
	visitor = Visitor()


	result = split0.accept(visitor)
	environment = {'size': size, 'content': content}
	outer_function = None
	call = visitor.call_leon(splitf, environment, outer_function, split_spec)
    # environment = {"x" : Int(0)}
	# outer_function = None
	# call = visitor.call_leon(node, environment, outer_function, split_spec)
	# print(call)
	# environment = {"x" : Int(0)} # environment works!
    # environment = {}
    # outer_function = None
    # choose = Choose(ChooseLHS("res", INT), Tru()) # want to say res = input * 2
    # call = visitor.call_leon(node, environment, outer_function, choose)
	print(call)



if __name__ == '__main__':
    test_traverse()
