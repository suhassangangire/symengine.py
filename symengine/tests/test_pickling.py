from symengine import symbols, sin, sinh, have_numpy, have_llvm, cos, Symbol
import pickle
import unittest


def test_basic():
    x, y, z = symbols('x y z')
    expr = sin(cos(x + y)/z)**2
    s = pickle.dumps(expr)
    expr2 = pickle.loads(s)
    assert expr == expr2


class MySymbol(Symbol):
    def __init__(self, name, attr):
        super().__init__(name=name)
        self.attr = attr

    def __reduce__(self):
        return (self.__class__, (self.name, self.attr))


def test_pysymbol():
    a = MySymbol("hello", attr=1)
    b = pickle.loads(pickle.dumps(a))
    assert b.attr == 1
    a._unsafe_reset()
    b._unsafe_reset()


@unittest.skipUnless(have_llvm, "No LLVM support")
@unittest.skipUnless(have_numpy, "Numpy not installed")
def test_llvm_double():
    import numpy as np
    from symengine import Lambdify
    args = x, y, z = symbols('x y z')
    expr = sin(sinh(x+y) + z)
    l = Lambdify(args, expr, cse=True, backend='llvm')
    ss = pickle.dumps(l)
    ll = pickle.loads(ss)
    inp = [1, 2, 3]
    assert np.allclose(l(inp), ll(inp))
