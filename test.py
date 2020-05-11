from ast import *
from traverse import *



size = Func('size', FuncType([LIST], INT) , ['lst'],
    Match(Var('lst'),
        Int(0),
        ConsCase('_', 'rest', Plus(Int(1), CallFunc('size', [Var('rest')], INT)))
    )
)

content = Func('content', FuncType([LIST], SET) , ['lst'],
    Match(Var('lst'),
        St([]),
        ConsCase('e', 'rest', StPlus(St(['e']), CallFunc('content', [Var('rest')], SET)))
    )
)


split_spec = Choose(ChooseLHS('r', TTuple([LIST, LIST])),
	Eq(content.get_call(['lst']),
		StPlus(content.get_call(TupleAcc(Var('r'), 0)), content.get_call(TupleAcc(Var('r'), 0)))))

split0 = Harness('split', [LIST], TTuple([LIST, LIST]), ['lst'], split_spec,
	Match(Var('lst'),
		nil_case = Tuple([Nil(), Nil()]),
		cons_case = ConsCase('h', 't', Match(Var('t'),
			nil_case = Tuple([Nil(), Cons(Var('h'), Nil())]),
			cons_case = ConsCase('h2', 't2',
				LetIn('v', CallFunc('split', [Var('t2')], TTuple([LIST, LIST])),
				Tuple([Cons(Var('h1'), TupleAcc(Var('r'), 1)), Cons(Var('h2'), TupleAcc(Var('r'), 1))])
				))
		))
	))



# old_choose = Ensuring(Flse(), And(Tru(), Lt(size.get_call(["lst_B"]), size.get_call(["lst_A"]))))
# harness =  Harness("split", [LIST], INT, ["lst_B"], old_choose, Tru())

def test_traverse():
	visitor = Visitor()


	node = split0
	# environment = {'size': size, 'content': content}
    # environment = {"x" : Int(0)}
	# outer_function = None
	# call = visitor.call_leon(node, environment, outer_function, split_spec)
	# print(call)



if __name__ == '__main__':
    test_traverse()