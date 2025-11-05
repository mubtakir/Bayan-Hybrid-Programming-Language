#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for context manager functionality (with) in Bayan language
اختبارات لمديري السياق (with) في لغة البيان
"""

import sys
sys.path.insert(0, 'bayan')

from bayan.lexer import HybridLexer, TokenType
from bayan.parser import HybridParser
from bayan.ast_nodes import WithStatement

def test_lexer_with_keyword():
    """Test that lexer recognizes 'with' keyword"""
    code = "with file as f:"
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    
    # Find WITH token
    with_tokens = [t for t in tokens if t.type == TokenType.WITH]
    assert len(with_tokens) == 1, "Should have one WITH token"
    print("✅ Lexer recognizes 'with' keyword")

def test_parse_with_simple():
    """Test parsing simple with statement"""
    code = """
with open("file.txt") as f: {
    print(f)
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    assert len(ast.statements) == 1, "Should have one statement"
    with_stmt = ast.statements[0]
    assert isinstance(with_stmt, WithStatement), f"Should be WithStatement, got {type(with_stmt)}"
    assert with_stmt.target_var == "f", f"Target var should be 'f', got {with_stmt.target_var}"
    print("✅ Parser handles 'with open(file) as f: { ... }'")

def test_parse_with_no_as():
    """Test parsing with statement without 'as' clause"""
    code = """
with lock: {
    critical_section()
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    with_stmt = ast.statements[0]
    assert isinstance(with_stmt, WithStatement), "Should be WithStatement"
    assert with_stmt.target_var is None, "Target var should be None"
    print("✅ Parser handles 'with lock: { ... }' without 'as'")

def test_parse_with_file_operations():
    """Test parsing with statement for file operations"""
    code = """
with open("data.txt") as file: {
    data = file.read()
    print(data)
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    with_stmt = ast.statements[0]
    assert isinstance(with_stmt, WithStatement), "Should be WithStatement"
    assert with_stmt.target_var == "file", "Target var should be 'file'"
    assert len(with_stmt.body.statements) == 2, "Should have 2 statements in body"
    print("✅ Parser handles file operations with 'with'")

def test_parse_with_complex_expression():
    """Test parsing with statement with complex context expression"""
    code = """
with create_connection("localhost", 8080) as conn: {
    conn.send("Hello")
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    with_stmt = ast.statements[0]
    assert isinstance(with_stmt, WithStatement), "Should be WithStatement"
    assert with_stmt.target_var == "conn", "Target var should be 'conn'"
    print("✅ Parser handles complex context expression")

def test_parse_nested_with():
    """Test parsing nested with statements"""
    code = """
with open("file1.txt") as f1: {
    with open("file2.txt") as f2: {
        data1 = f1.read()
        data2 = f2.read()
    }
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    outer_with = ast.statements[0]
    assert isinstance(outer_with, WithStatement), "Outer should be WithStatement"
    
    inner_with = outer_with.body.statements[0]
    assert isinstance(inner_with, WithStatement), "Inner should be WithStatement"
    print("✅ Parser handles nested with statements")

def test_parse_with_in_function():
    """Test parsing with statement inside function"""
    code = """
def read_file(filename): {
    with open(filename) as f: {
        return f.read()
    }
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    func = ast.statements[0]
    with_stmt = func.body.statements[0]
    assert isinstance(with_stmt, WithStatement), "Should be WithStatement"
    print("✅ Parser handles with inside function")

def test_parse_with_multiple_statements():
    """Test parsing with statement with multiple body statements"""
    code = """
with database.transaction() as tx: {
    tx.insert("user", data)
    tx.update("stats", count)
    tx.commit()
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    with_stmt = ast.statements[0]
    assert isinstance(with_stmt, WithStatement), "Should be WithStatement"
    assert len(with_stmt.body.statements) == 3, "Should have 3 statements in body"
    print("✅ Parser handles multiple statements in with body")

def test_parse_with_try_except():
    """Test parsing with statement containing try/except"""
    code = """
with open("file.txt") as f: {
    try: {
        data = f.read()
    } except: {
        print("Error reading file")
    }
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    with_stmt = ast.statements[0]
    assert isinstance(with_stmt, WithStatement), "Should be WithStatement"
    print("✅ Parser handles with containing try/except")

def test_parse_with_for_loop():
    """Test parsing with statement containing for loop"""
    code = """
with open("file.txt") as f: {
    for line in f: {
        print(line)
    }
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    with_stmt = ast.statements[0]
    assert isinstance(with_stmt, WithStatement), "Should be WithStatement"
    print("✅ Parser handles with containing for loop")

def test_parse_with_conditional():
    """Test parsing with statement with conditional"""
    code = """
with get_resource() as resource: {
    if resource.is_valid(): {
        resource.use()
    } else: {
        print("Invalid resource")
    }
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    with_stmt = ast.statements[0]
    assert isinstance(with_stmt, WithStatement), "Should be WithStatement"
    print("✅ Parser handles with containing conditional")

if __name__ == "__main__":
    print("Testing Context Manager Functionality (with)")
    print("=" * 50)
    
    test_lexer_with_keyword()
    test_parse_with_simple()
    test_parse_with_no_as()
    test_parse_with_file_operations()
    test_parse_with_complex_expression()
    test_parse_nested_with()
    test_parse_with_in_function()
    test_parse_with_multiple_statements()
    test_parse_with_try_except()
    test_parse_with_for_loop()
    test_parse_with_conditional()
    
    print("=" * 50)
    print("✅ All context manager tests passed!")

