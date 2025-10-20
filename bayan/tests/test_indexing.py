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


def test_python_list_index_get():
    code = """
    lst = [1, 2, 3]
    a = lst[1]
    """
    intr = run(code)
    assert intr.traditional.global_env['a'] == 2


def test_bayan_object_get_set_item():
    code = """
    class Bag:
    {
        def __init__(): { self.d = {} }
        def __getitem__(k): { return self.d[k] }
        def __setitem__(k, v): { self.d[k] = v }
    }
    b = Bag()
    b["x"] = 7
    y = b["x"]
    """
    intr = run(code)
    assert intr.traditional.global_env['y'] == 7

