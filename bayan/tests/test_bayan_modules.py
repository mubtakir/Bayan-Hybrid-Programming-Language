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


def test_import_bayan_module_var_and_func():
    code = """
    import tests.bayan_modules.m1 as m1
    a = m1.x
    b = m1.inc(3)
    """
    intr = run(code)
    assert intr.traditional.global_env['a'] == 7
    assert intr.traditional.global_env['b'] == 4


def test_from_import_bayan_module_function():
    code = """
    from tests.bayan_modules.m2 import add
    c = add(2, 3)
    """
    intr = run(code)
    assert intr.traditional.global_env['c'] == 5


def test_from_import_bayan_module_class():
    code = """
    from tests.bayan_modules.mc import C
    obj = C(9)
    d = obj.get()
    """
    intr = run(code)
    assert intr.traditional.global_env['d'] == 9

