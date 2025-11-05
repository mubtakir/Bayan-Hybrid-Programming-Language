"""
Tests for inheritance, super(), and dunder methods in Bayan Language
اختبارات الوراثة و super والدوال السحرية في لغة بيان
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bayan import HybridLexer, HybridParser, HybridInterpreter

def parse_and_run(code: str):
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    result = interpreter.interpret(ast)
    return interpreter

def test_inheritance_method_resolution():
    code = """
    class A:
    {
        def foo():
        {
            return 1
        }
    }

    class B(A):
    {
    }

    b = B()
    x = b.foo()
    """
    interp = parse_and_run(code)
    assert interp.traditional.global_env['x'] == 1


def test_super_override():
    code = """
    class Base:
    {
        def inc(x):
        {
            return x + 1
        }
    }

    class Child(Base):
    {
        def inc(x):
        {
            return super(inc, x) + 1
        }
    }

    c = Child()
    y = c.inc(5)
    """
    interp = parse_and_run(code)
    assert interp.traditional.global_env['y'] == 7


def test_super_init():
    code = """
    class P:
    {
        def __init__(x):
        {
            self.x = x
        }
    }

    class C(P):
    {
        def __init__(y):
        {
            super(__init__, y)
            self.y = y
        }
    }

    c = C(10)
    x = c.x
    y = c.y
    """
    interp = parse_and_run(code)
    assert interp.traditional.global_env['x'] == 10
    assert interp.traditional.global_env['y'] == 10


def test_dunder_add_and_str_and_eq():
    code = """
    class Box:
    {
        def __init__(v):
        {
            self.v = v
        }
        def __add__(other):
        {
            return self.v + other.v
        }
        def __str__():
        {
            return "Box(" + str(self.v) + ")"
        }
        def __eq__(other):
        {
            return self.v == other.v
        }
    }

    b1 = Box(3)
    b2 = Box(4)
    b3 = Box(3)

    s = str(b1)
    sum12 = b1 + b2
    eq13 = b1 == b3
    eq12 = b1 == b2
    """
    interp = parse_and_run(code)
    g = interp.traditional.global_env
    assert g['s'] == "Box(3)"
    assert g['sum12'] == 7
    assert g['eq13'] is True
    assert g['eq12'] is False

if __name__ == '__main__':
    test_inheritance_method_resolution()
    print("✓ test_inheritance_method_resolution passed")

    test_super_override()
    print("✓ test_super_override passed")

    test_super_init()
    print("✓ test_super_init passed")

    test_dunder_add_and_str_and_eq()
    print("✓ test_dunder_add_and_str_and_eq passed")

    print("\n✅ All inheritance tests passed!")

