import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from bayan import HybridLexer, HybridParser, HybridInterpreter


def run(code: str) -> HybridInterpreter:
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    intr = HybridInterpreter()
    intr.interpret(ast)
    return intr


def test_contains_operator():
    code = """
    class Bag:
    {
        def __init__(): { self.lst = [1, 2, 3] }
        def __contains__(x): { return x in self.lst }
    }
    b = Bag()
    a = 2 in b
    c = 5 in b
    """
    intr = run(code)
    assert intr.traditional.global_env['a'] is True
    assert intr.traditional.global_env['c'] is False


def test_iter_for_loop():
    code = """
    class Seq:
    {
        def __iter__(): { return [1, 2, 3] }
    }
    s = 0
    for x in Seq():
    {
        s = s + x
    }
    """
    intr = run(code)
    assert intr.traditional.global_env['s'] == 6


def test_callable_dunder():
    code = """
    class Adder:
    {
        def __call__(x, y): { return x + y }
    }
    f = Adder()
    z = f(2, 3)
    """
    intr = run(code)
    assert intr.traditional.global_env['z'] == 5


def test_repr_dunder():
    code = """
    class P:
    {
        def __repr__(): { return "P()" }
    }
    r = repr(P())
    """
    intr = run(code)
    assert intr.traditional.global_env['r'] == "P()"


def test_bool_dunder_in_condition_and_not():
    code = """
    class Z:
    {
        def __bool__(): { return False }
    }
    if Z():
    {
        a = 1
    }
    else:
    {
        a = 2
    }
    d = not Z()
    """
    intr = run(code)
    assert intr.traditional.global_env['a'] == 2
    assert intr.traditional.global_env['d'] is True

