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

def test_super_legacy_and_pythonic_equivalence():
    code = """
    class Base:
    {
        def f(x): { return x + 1 }
    }
    class Child(Base):
    {
        def f(x): { return super(f, x) + 1 }
        def g(x): { return super().f(x) + 1 }
    }
    c = Child()
    a = c.f(10)
    b = c.g(10)
    """
    intr = run(code)
    g = intr.traditional.global_env
    assert g['a'] == 12
    assert g['b'] == 12

if __name__ == '__main__':
    test_super_legacy_and_pythonic_equivalence()
    print('✓ test_super_legacy_and_pythonic_equivalence passed')

