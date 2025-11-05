#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for generator functionality (yield) in Bayan language
اختبارات لوظائف المولدات (yield) في لغة البيان
"""

import sys
sys.path.insert(0, 'bayan')

from bayan.lexer import HybridLexer, TokenType
from bayan.parser import HybridParser
from bayan.ast_nodes import YieldExpr, FunctionDef

def test_lexer_yield_keyword():
    """Test that lexer recognizes 'yield' keyword"""
    code = "yield 42"
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    
    # Find YIELD token
    yield_tokens = [t for t in tokens if t.type == TokenType.YIELD]
    assert len(yield_tokens) == 1, "Should have one YIELD token"
    print("✅ Lexer recognizes 'yield' keyword")

def test_parse_yield_simple():
    """Test parsing simple yield statement"""
    code = """
def generator(): {
    yield 42
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    assert len(ast.statements) == 1, "Should have one statement"
    func = ast.statements[0]
    assert isinstance(func, FunctionDef), f"Should be FunctionDef, got {type(func)}"
    
    # Check that body contains yield
    yield_stmt = func.body.statements[0]
    assert isinstance(yield_stmt, YieldExpr), f"Should be YieldExpr, got {type(yield_stmt)}"
    print("✅ Parser handles 'yield 42'")

def test_parse_yield_with_value():
    """Test parsing yield with expression"""
    code = """
def count(n): {
    i = 0
    while i < n: {
        yield i
        i = i + 1
    }
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    func = ast.statements[0]
    assert isinstance(func, FunctionDef), "Should be FunctionDef"
    print("✅ Parser handles 'yield i' in loop")

def test_parse_yield_none():
    """Test parsing yield without value"""
    code = """
def generator(): {
    yield
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    func = ast.statements[0]
    yield_stmt = func.body.statements[0]
    assert isinstance(yield_stmt, YieldExpr), "Should be YieldExpr"
    assert yield_stmt.value is None, "Yield value should be None"
    print("✅ Parser handles 'yield' without value")

def test_parse_multiple_yields():
    """Test parsing multiple yield statements"""
    code = """
def generator(): {
    yield 1
    yield 2
    yield 3
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    func = ast.statements[0]
    assert len(func.body.statements) == 3, "Should have 3 yield statements"
    
    for stmt in func.body.statements:
        assert isinstance(stmt, YieldExpr), "All statements should be YieldExpr"
    
    print("✅ Parser handles multiple yield statements")

def test_parse_yield_in_for_loop():
    """Test parsing yield inside for loop"""
    code = """
def iterate(items): {
    for item in items: {
        yield item
    }
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    func = ast.statements[0]
    assert isinstance(func, FunctionDef), "Should be FunctionDef"
    print("✅ Parser handles yield in for loop")

def test_parse_yield_with_expression():
    """Test parsing yield with complex expression"""
    code = """
def squares(n): {
    i = 0
    while i < n: {
        yield i * i
        i = i + 1
    }
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    func = ast.statements[0]
    assert isinstance(func, FunctionDef), "Should be FunctionDef"
    print("✅ Parser handles 'yield i * i'")

def test_parse_yield_with_function_call():
    """Test parsing yield with function call"""
    code = """
def process(items): {
    for item in items: {
        yield transform(item)
    }
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    func = ast.statements[0]
    assert isinstance(func, FunctionDef), "Should be FunctionDef"
    print("✅ Parser handles 'yield transform(item)'")

def test_parse_fibonacci_generator():
    """Test parsing fibonacci generator"""
    code = """
def fibonacci(n): {
    a = 0
    b = 1
    i = 0
    while i < n: {
        yield a
        temp = a
        a = b
        b = temp + b
        i = i + 1
    }
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    func = ast.statements[0]
    assert isinstance(func, FunctionDef), "Should be FunctionDef"
    assert func.name == "fibonacci", "Function name should be 'fibonacci'"
    print("✅ Parser handles fibonacci generator")

def test_parse_yield_with_conditional():
    """Test parsing yield with conditional"""
    code = """
def filter_even(items): {
    for item in items: {
        if item % 2 == 0: {
            yield item
        }
    }
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    func = ast.statements[0]
    assert isinstance(func, FunctionDef), "Should be FunctionDef"
    print("✅ Parser handles yield with conditional")

if __name__ == "__main__":
    print("Testing Generator Functionality (yield)")
    print("=" * 50)
    
    test_lexer_yield_keyword()
    test_parse_yield_simple()
    test_parse_yield_with_value()
    test_parse_yield_none()
    test_parse_multiple_yields()
    test_parse_yield_in_for_loop()
    test_parse_yield_with_expression()
    test_parse_yield_with_function_call()
    test_parse_fibonacci_generator()
    test_parse_yield_with_conditional()
    
    print("=" * 50)
    print("✅ All generator tests passed!")

