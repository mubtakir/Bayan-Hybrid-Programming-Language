import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from bayan import HybridLexer, HybridParser, HybridInterpreter


def run(code: str):
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    intr = HybridInterpreter()
    return intr.interpret(ast)


def test_undefined_variable_stack_trace():
    code = """
    a = b + 1
    """
    with pytest.raises(Exception) as ei:
        run(code)
    msg = str(ei.value)
    assert "NameError" in msg
    assert "Undefined variable: b" in msg
    assert "Bayan stack:" in msg
    # Should include node types in stack
    assert "BinaryOp" in msg or "+" in msg
    assert "Assignment" in msg


def test_missing_attribute_stack_trace():
    code = """
    class A:
    {
        def __init__(): { }
    }
    a = A()
    x = a.missing()
    """
    with pytest.raises(Exception) as ei:
        run(code)
    msg = str(ei.value)
    assert "AttributeError" in msg
    assert "Bayan stack:" in msg
    assert "MethodCall" in msg or ".missing" in msg


def test_indexing_error_stack_trace():
    code = """
    x = 5
    y = x[0]
    """
    with pytest.raises(Exception) as ei:
        run(code)
    msg = str(ei.value)
    assert "TypeError" in msg
    assert "Bayan stack:" in msg
    assert "SubscriptAccess" in msg or "Indexing" in msg




def test_error_message_includes_code_frame():
    code = """
    a = b + 1
    """
    # Strip leading newline to control line numbers
    code = code.lstrip("\n")
    lexer = HybridLexer(code)
    toks = lexer.tokenize()
    # Provide a filename to parser; and tell interpreter the source for code-frames
    parser = HybridParser(toks, filename="mem.by")
    ast = parser.parse()
    intr = HybridInterpreter()
    intr.traditional.set_source(code, filename="mem.by")
    with pytest.raises(Exception) as ei:
        intr.interpret(ast)
    msg = str(ei.value)
    assert "Bayan stack:" in msg
    assert "File mem.by:1:" in msg
    assert ">1 |" in msg  # numbered current line prefix
    assert "a = b + 1" in msg
    assert "^" in msg  # caret under the column



def test_undefined_name_suggestions():
    code = """
    x = 10
    y = x1 + 1
    """
    with pytest.raises(Exception) as ei:
        run(code)
    msg = str(ei.value)
    assert "Undefined variable: x1" in msg
    assert "Did you mean:" in msg
    assert "x" in msg


def test_colored_code_frame_optional():
    code = """
    a = b + 1
    """.lstrip("\n")
    lexer = HybridLexer(code)
    toks = lexer.tokenize()
    parser = HybridParser(toks, filename="mem.by")
    ast = parser.parse()
    intr = HybridInterpreter()
    intr.traditional.set_source(code, filename="mem.by")
    intr.traditional.set_error_formatting(colors=True)
    with pytest.raises(Exception) as ei:
        intr.interpret(ast)
    msg = str(ei.value)
    assert "\x1b[" in msg  # ANSI escape present when colors enabled
    assert "File mem.by:1:" in msg
    assert ">1 |" in msg
    assert "^" in msg

