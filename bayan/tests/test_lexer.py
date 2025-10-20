"""
Tests for the Lexer
اختبارات المحلل المعجمي
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bayan.lexer import HybridLexer, TokenType

def test_basic_tokens():
    """Test basic token recognition"""
    code = "x = 5"
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == 'x'
    assert tokens[1].type == TokenType.ASSIGN
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].value == '5'
    print("✓ test_basic_tokens passed")

def test_keywords():
    """Test keyword recognition"""
    code = "def if else for while"
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.DEF
    assert tokens[1].type == TokenType.IF
    assert tokens[2].type == TokenType.ELSE
    assert tokens[3].type == TokenType.FOR
    assert tokens[4].type == TokenType.WHILE
    print("✓ test_keywords passed")

def test_logical_tokens():
    """Test logical token recognition"""
    code = "?X parent(john, ?Y) :-"
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.VARIABLE
    assert tokens[0].value == '?X'
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[2].type == TokenType.LPAREN
    assert tokens[3].type == TokenType.IDENTIFIER
    assert tokens[4].type == TokenType.COMMA
    assert tokens[5].type == TokenType.VARIABLE
    assert tokens[6].type == TokenType.RPAREN
    assert tokens[7].type == TokenType.IMPLIES
    print("✓ test_logical_tokens passed")

def test_strings():
    """Test string recognition"""
    code = '"hello" \'world\''
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == '"hello"'
    assert tokens[1].type == TokenType.STRING
    assert tokens[1].value == "'world'"
    print("✓ test_strings passed")

def test_numbers():
    """Test number recognition"""
    code = "42 3.14 0"
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == '42'
    assert tokens[1].type == TokenType.NUMBER
    assert tokens[1].value == '3.14'
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].value == '0'
    print("✓ test_numbers passed")

def test_operators():
    """Test operator recognition"""
    code = "+ - * / == != < > <= >="
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.OPERATOR
    assert tokens[0].value == '+'
    assert tokens[1].type == TokenType.OPERATOR
    assert tokens[1].value == '-'
    assert tokens[2].type == TokenType.OPERATOR
    assert tokens[2].value == '*'
    print("✓ test_operators passed")

def test_comments():
    """Test comment handling"""
    code = "x = 5  # this is a comment\ny = 10"
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    
    # Comments should be skipped
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == 'x'
    assert tokens[1].type == TokenType.ASSIGN
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].value == '5'
    assert tokens[3].type == TokenType.IDENTIFIER
    assert tokens[3].value == 'y'
    print("✓ test_comments passed")

def test_arabic_identifiers():
    """Test Arabic identifier support"""
    code = "اسم = 5"
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == 'اسم'
    assert tokens[1].type == TokenType.ASSIGN
    assert tokens[2].type == TokenType.NUMBER
    print("✓ test_arabic_identifiers passed")

def test_hybrid_block():
    """Test hybrid block recognition"""
    code = "hybrid { x = 5 parent(john, mary). }"
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.HYBRID
    assert tokens[1].type == TokenType.LBRACE
    assert tokens[2].type == TokenType.IDENTIFIER
    assert tokens[3].type == TokenType.ASSIGN
    assert tokens[4].type == TokenType.NUMBER
    assert tokens[5].type == TokenType.IDENTIFIER
    assert tokens[6].type == TokenType.LPAREN
    print("✓ test_hybrid_block passed")

if __name__ == "__main__":
    test_basic_tokens()
    test_keywords()
    test_logical_tokens()
    test_strings()
    test_numbers()
    test_operators()
    test_comments()
    test_arabic_identifiers()
    test_hybrid_block()
    print("\n✓ All lexer tests passed!")

