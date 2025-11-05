#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for decorators (@) in Bayan language
اختبارات للمزخرفات (@) في لغة البيان
"""

import sys
sys.path.insert(0, 'bayan')

from bayan.lexer import HybridLexer, TokenType
from bayan.parser import HybridParser
from bayan.ast_nodes import FunctionDef, ClassDef, Decorator

def test_lexer_at_symbol():
    """Test that lexer recognizes '@' as AT token"""
    code = "@decorator"
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    
    # Find AT token
    at_tokens = [t for t in tokens if t.type == TokenType.AT]
    assert len(at_tokens) == 1, "Should have one AT token"
    print("✅ Lexer recognizes '@' as AT")

def test_parse_simple_decorator():
    """Test parsing simple decorator on function"""
    code = """
@decorator
def my_function(): {
    return 42
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    assert len(ast.statements) == 1, "Should have one statement"
    func = ast.statements[0]
    assert isinstance(func, FunctionDef), "Should be FunctionDef"
    assert len(func.decorators) == 1, "Should have one decorator"
    assert isinstance(func.decorators[0], Decorator), "Should be Decorator instance"
    assert func.decorators[0].name == "decorator", "Decorator name should be 'decorator'"
    assert len(func.decorators[0].args) == 0, "Decorator should have no args"
    print("✅ Parser handles simple decorator on function")

def test_parse_decorator_with_args():
    """Test parsing decorator with arguments"""
    code = """
@decorator(arg1, arg2)
def my_function(): {
    return 42
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    func = ast.statements[0]
    assert len(func.decorators) == 1, "Should have one decorator"
    assert len(func.decorators[0].args) == 2, "Decorator should have 2 args"
    print("✅ Parser handles decorator with arguments")

def test_parse_multiple_decorators():
    """Test parsing multiple decorators on function"""
    code = """
@decorator1
@decorator2
@decorator3
def my_function(): {
    return 42
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    func = ast.statements[0]
    assert len(func.decorators) == 3, "Should have three decorators"
    assert func.decorators[0].name == "decorator1", "First decorator should be 'decorator1'"
    assert func.decorators[1].name == "decorator2", "Second decorator should be 'decorator2'"
    assert func.decorators[2].name == "decorator3", "Third decorator should be 'decorator3'"
    print("✅ Parser handles multiple decorators")

def test_parse_decorator_on_class():
    """Test parsing decorator on class"""
    code = """
@dataclass
class MyClass: {
    x = 10
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    cls = ast.statements[0]
    assert isinstance(cls, ClassDef), "Should be ClassDef"
    assert len(cls.decorators) == 1, "Should have one decorator"
    assert cls.decorators[0].name == "dataclass", "Decorator name should be 'dataclass'"
    print("✅ Parser handles decorator on class")

def test_parse_decorator_with_string_arg():
    """Test parsing decorator with string argument"""
    code = """
@route("/api/users")
def get_users(): {
    return []
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    func = ast.statements[0]
    assert len(func.decorators) == 1, "Should have one decorator"
    assert func.decorators[0].name == "route", "Decorator name should be 'route'"
    assert len(func.decorators[0].args) == 1, "Decorator should have 1 arg"
    print("✅ Parser handles decorator with string argument")

def test_parse_decorator_with_number_arg():
    """Test parsing decorator with number argument"""
    code = """
@cache(300)
def expensive_function(): {
    return 42
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    func = ast.statements[0]
    assert len(func.decorators) == 1, "Should have one decorator"
    assert func.decorators[0].name == "cache", "Decorator name should be 'cache'"
    print("✅ Parser handles decorator with number argument")

def test_parse_decorator_ast_structure():
    """Test that Decorator AST node is created correctly"""
    code = """
@my_decorator
def test(): {
    return 0
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    func = ast.statements[0]
    decorator = func.decorators[0]
    
    assert isinstance(decorator, Decorator), "Should be Decorator instance"
    assert decorator.name == "my_decorator", "Decorator name should be 'my_decorator'"
    assert decorator.args == [], "Decorator should have no args"
    print("✅ Decorator AST node structure is correct")

def test_parse_decorator_on_async_function():
    """Test parsing decorator on async function"""
    code = """
@async_decorator
async def fetch_data(): {
    return 42
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    func = ast.statements[0]
    assert len(func.decorators) == 1, "Should have one decorator"
    assert func.decorators[0].name == "async_decorator", "Decorator name should be 'async_decorator'"
    print("✅ Parser handles decorator on async function")

def test_parse_mixed_decorators():
    """Test parsing decorators with and without arguments"""
    code = """
@decorator1
@decorator2(arg1)
@decorator3(arg1, arg2)
def my_function(): {
    return 42
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    func = ast.statements[0]
    assert len(func.decorators) == 3, "Should have three decorators"
    assert len(func.decorators[0].args) == 0, "First decorator should have no args"
    assert len(func.decorators[1].args) == 1, "Second decorator should have 1 arg"
    assert len(func.decorators[2].args) == 2, "Third decorator should have 2 args"
    print("✅ Parser handles mixed decorators")

def test_parse_decorator_repr():
    """Test Decorator __repr__ method"""
    code = """
@my_decorator(arg1, arg2)
def test(): {
    return 0
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    func = ast.statements[0]
    decorator = func.decorators[0]
    
    repr_str = repr(decorator)
    assert "my_decorator" in repr_str, "Repr should contain decorator name"
    print("✅ Decorator __repr__ works correctly")

if __name__ == "__main__":
    print("Testing Decorators (@)")
    print("=" * 50)
    
    test_lexer_at_symbol()
    test_parse_simple_decorator()
    test_parse_decorator_with_args()
    test_parse_multiple_decorators()
    test_parse_decorator_on_class()
    test_parse_decorator_with_string_arg()
    test_parse_decorator_with_number_arg()
    test_parse_decorator_ast_structure()
    test_parse_decorator_on_async_function()
    test_parse_mixed_decorators()
    test_parse_decorator_repr()
    
    print("=" * 50)
    print("✅ All decorator tests return 0ed!")

