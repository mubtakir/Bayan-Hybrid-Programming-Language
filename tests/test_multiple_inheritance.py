import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bayan import HybridLexer, HybridParser, HybridInterpreter

def run(code):
    lx = HybridLexer(code)
    toks = lx.tokenize()
    ps = HybridParser(toks)
    ast = ps.parse()
    intr = HybridInterpreter()
    intr.interpret(ast)
    return intr

def test_mi_linearization_left_to_right():
    code = """
    class A:
    {
        def who(): { return "A" }
    }
    class B:
    {
        def who(): { return "B" }
    }
    class C(A, B):
    {
    }
    c = C()
    w = c.who()
    """
    intr = run(code)
    g = intr.traditional.global_env
    assert g['w'] == "A"


def test_mi_super_moves_along_mro():
    code = """
    class A:
    {
        def f(): { return "A" }
    }
    class B(A):
    {
        def f(): { return super(f) + "B" }
    }
    class C(B):
    {
        def f(): { return super(f) + "C" }
    }
    # Linear chain sanity (not MI yet)
    c = C()
    s = c.f()
    """
    intr = run(code)
    assert intr.traditional.global_env['s'] == "ABC"


def test_mi_diamond_c3():
    code = """
    class A:
    {
        def f(): { return "A" }
    }
    class B(A):
    {
        def f(): { return super(f) + "B" }
    }
    class C(A):
    {
        def f(): { return super(f) + "C" }
    }
    class D(B, C):
    {
        def f(): { return super(f) + "D" }
    }

    d = D()
    out = d.f()
    """
    intr = run(code)
    # C3 MRO for D(B, C) over A is D, B, C, A
    # With each method doing super(f) + "Letter", the order is A then C then B then D
    assert intr.traditional.global_env['out'] == "ACBD"

if __name__ == '__main__':
    test_mi_linearization_left_to_right()
    print('\u2713 test_mi_linearization_left_to_right passed')
    test_mi_super_moves_along_mro()
    print('\u2713 test_mi_super_moves_along_mro passed')
    test_mi_diamond_c3()
    print('\u2713 test_mi_diamond_c3 passed')

