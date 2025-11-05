#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for async/await functionality in Bayan language
اختبارات لوظائف async/await في لغة البيان
"""

import sys
sys.path.insert(0, 'bayan')

from bayan.lexer import HybridLexer, TokenType
from bayan.parser import HybridParser
from bayan.ast_nodes import AsyncFunctionDef, AwaitExpr

def test_lexer_async_keyword():
    """Test that lexer recognizes 'async' keyword"""
    code = "async def fetch():"
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    
    # Find ASYNC token
    async_tokens = [t for t in tokens if t.type == TokenType.ASYNC]
    assert len(async_tokens) == 1, "Should have one ASYNC token"
    print("✅ Lexer recognizes 'async' keyword")

def test_lexer_await_keyword():
    """Test that lexer recognizes 'await' keyword"""
    code = "await fetch()"
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    
    # Find AWAIT token
    await_tokens = [t for t in tokens if t.type == TokenType.AWAIT]
    assert len(await_tokens) == 1, "Should have one AWAIT token"
    print("✅ Lexer recognizes 'await' keyword")

def test_parse_async_function_simple():
    """Test parsing simple async function"""
    code = """
async def fetch(): {
    return 42
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    assert len(ast.statements) == 1, "Should have one statement"
    func = ast.statements[0]
    assert isinstance(func, AsyncFunctionDef), f"Should be AsyncFunctionDef, got {type(func)}"
    assert func.name == "fetch", f"Function name should be 'fetch', got {func.name}"
    assert len(func.params) == 0, "Should have no parameters"
    print("✅ Parser handles 'async def fetch(): { return 42 }'")

def test_parse_async_function_with_params():
    """Test parsing async function with parameters"""
    code = """
async def fetch(url, timeout): {
    return url
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    func = ast.statements[0]
    assert isinstance(func, AsyncFunctionDef), "Should be AsyncFunctionDef"
    assert func.name == "fetch", "Function name should be 'fetch'"
    assert len(func.params) == 2, "Should have 2 parameters"
    print("✅ Parser handles 'async def fetch(url, timeout): { ... }'")

def test_parse_await_expression():
    """Test parsing await expression"""
    code = """
async def main(): {
    result = await fetch()
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    func = ast.statements[0]
    assert isinstance(func, AsyncFunctionDef), "Should be AsyncFunctionDef"

    # Check that body contains assignment with await
    assignment = func.body.statements[0]
    assert hasattr(assignment, 'value'), "Should have assignment"
    assert isinstance(assignment.value, AwaitExpr), f"Should be AwaitExpr, got {type(assignment.value)}"
    print("✅ Parser handles 'result = await fetch()'")

def test_parse_await_with_arguments():
    """Test parsing await with function call arguments"""
    code = """
async def main(): {
    data = await fetch("https://api.example.com")
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    func = ast.statements[0]
    assignment = func.body.statements[0]
    assert isinstance(assignment.value, AwaitExpr), "Should be AwaitExpr"
    print("✅ Parser handles 'await fetch(url)'")

def test_parse_multiple_awaits():
    """Test parsing multiple await expressions"""
    code = """
async def main(): {
    data1 = await fetch1()
    data2 = await fetch2()
    data3 = await fetch3()
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    func = ast.statements[0]
    assert len(func.body.statements) == 3, "Should have 3 statements"

    for i, stmt in enumerate(func.body.statements):
        assert isinstance(stmt.value, AwaitExpr), f"Statement {i} should have AwaitExpr"

    print("✅ Parser handles multiple await expressions")

def test_parse_nested_async_functions():
    """Test parsing nested async functions"""
    code = """
async def outer(): {
    async def inner(): {
        return 42
    }
    return await inner()
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    outer_func = ast.statements[0]
    assert isinstance(outer_func, AsyncFunctionDef), "Outer should be AsyncFunctionDef"

    # Check that body contains inner async function
    inner_func = outer_func.body.statements[0]
    assert isinstance(inner_func, AsyncFunctionDef), "Inner should be AsyncFunctionDef"
    print("✅ Parser handles nested async functions")

def test_parse_async_with_try_except():
    """Test parsing async function with try/except"""
    code = """
async def fetch_safe(): {
    try: {
        data = await fetch()
        return data
    } except: {
        return None
    }
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    func = ast.statements[0]
    assert isinstance(func, AsyncFunctionDef), "Should be AsyncFunctionDef"
    print("✅ Parser handles async with try/except")

def test_parse_async_for_loop():
    """Test parsing async function with for loop"""
    code = """
async def process_all(urls): {
    results = []
    for url in urls: {
        data = await fetch(url)
        results.append(data)
    }
    return results
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    func = ast.statements[0]
    assert isinstance(func, AsyncFunctionDef), "Should be AsyncFunctionDef"
    print("✅ Parser handles async with for loop")

if __name__ == "__main__":
    print("Testing Async/Await Functionality")
    print("=" * 50)
    
    test_lexer_async_keyword()
    test_lexer_await_keyword()
    test_parse_async_function_simple()
    test_parse_async_function_with_params()
    test_parse_await_expression()
    test_parse_await_with_arguments()
    test_parse_multiple_awaits()
    test_parse_nested_async_functions()
    test_parse_async_with_try_except()
    test_parse_async_for_loop()
    
    print("=" * 50)
    print("✅ All async/await tests passed!")

