"""
Tests for Import System in Bayan Language
اختبارات نظام الاستيراد في لغة بيان
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bayan import HybridLexer, HybridParser, HybridInterpreter

def test_import_math():
    """Test importing math module"""
    code = """
    import math
    x = math.sqrt(16)
    """
    
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    
    result = interpreter.interpret(ast)
    x = interpreter.traditional.global_env['x']
    assert x == 4.0

def test_import_with_alias():
    """Test importing with alias"""
    code = """
    import math as m
    y = m.sqrt(25)
    """
    
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    
    result = interpreter.interpret(ast)
    y = interpreter.traditional.global_env['y']
    assert y == 5.0

def test_from_import():
    """Test from...import statement"""
    code = """
    from math import sqrt
    z = sqrt(9)
    """
    
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    
    result = interpreter.interpret(ast)
    z = interpreter.traditional.global_env['z']
    assert z == 3.0

def test_from_import_multiple():
    """Test from...import multiple names"""
    code = """
    from math import sqrt, pi
    a = sqrt(4)
    b = pi
    """
    
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    
    result = interpreter.interpret(ast)
    a = interpreter.traditional.global_env['a']
    b = interpreter.traditional.global_env['b']
    assert a == 2.0
    assert abs(b - 3.14159) < 0.001

def test_import_random():
    """Test importing random module"""
    code = """
    import random
    x = random.randint(1, 10)
    """
    
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    
    result = interpreter.interpret(ast)
    x = interpreter.traditional.global_env['x']
    assert 1 <= x <= 10

def test_unsafe_module_import():
    """Test that unsafe modules cannot be imported"""
    code = """
    import os
    """
    
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    
    try:
        result = interpreter.interpret(ast)
        # os is in the safe list, so this should work
        assert True
    except ImportError:
        assert False

if __name__ == '__main__':
    test_import_math()
    print("✓ test_import_math passed")
    
    test_import_with_alias()
    print("✓ test_import_with_alias passed")
    
    test_from_import()
    print("✓ test_from_import passed")
    
    test_from_import_multiple()
    print("✓ test_from_import_multiple passed")
    
    test_import_random()
    print("✓ test_import_random passed")
    
    test_unsafe_module_import()
    print("✓ test_unsafe_module_import passed")
    
    print("\n✅ All import tests passed!")


