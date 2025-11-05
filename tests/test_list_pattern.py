"""
Tests for List Pattern [H|T] feature
اختبارات لميزة نمط القوائم [H|T]
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bayan'))

from bayan.lexer import HybridLexer, TokenType
from bayan.parser import HybridParser
from bayan.ast_nodes import ListPattern, Variable

def test_lexer_pipe_token():
    """Test that lexer recognizes PIPE token"""
    code = '|'
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.PIPE
    print("✅ Lexer recognizes PIPE token")

def test_simple_list_pattern():
    """Test parsing [H|T]"""
    code = '[?H|?T]'
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse_primary()
    
    assert isinstance(ast, ListPattern)
    assert len(ast.head_elements) == 1
    assert isinstance(ast.head_elements[0], Variable)
    assert ast.head_elements[0].name == '?H'
    assert isinstance(ast.tail, Variable)
    assert ast.tail.name == '?T'
    print("✅ Simple list pattern [H|T] works")

def test_multiple_heads_pattern():
    """Test parsing [H1, H2, H3|T]"""
    code = '[?H1, ?H2, ?H3|?T]'
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse_primary()
    
    assert isinstance(ast, ListPattern)
    assert len(ast.head_elements) == 3
    assert ast.head_elements[0].name == '?H1'
    assert ast.head_elements[1].name == '?H2'
    assert ast.head_elements[2].name == '?H3'
    assert ast.tail.name == '?T'
    print("✅ Multiple heads pattern [H1, H2, H3|T] works")

def test_mixed_pattern():
    """Test parsing [1, 2, ?X|?Rest]"""
    code = '[1, 2, ?X|?Rest]'
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse_primary()
    
    assert isinstance(ast, ListPattern)
    assert len(ast.head_elements) == 3
    print("✅ Mixed pattern [1, 2, ?X|?Rest] works")

def test_regular_list_still_works():
    """Test that regular lists [1, 2, 3] still work"""
    code = '[1, 2, 3]'
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse_primary()
    
    # Should be a regular List, not ListPattern
    assert type(ast).__name__ == 'List'
    assert len(ast.elements) == 3
    print("✅ Regular lists [1, 2, 3] still work")

def test_empty_list_still_works():
    """Test that empty lists [] still work"""
    code = '[]'
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse_primary()
    
    assert type(ast).__name__ == 'List'
    assert len(ast.elements) == 0
    print("✅ Empty lists [] still work")

if __name__ == '__main__':
    print("Testing List Pattern [H|T] Feature...")
    print("=" * 50)
    
    test_lexer_pipe_token()
    test_simple_list_pattern()
    test_multiple_heads_pattern()
    test_mixed_pattern()
    test_regular_list_still_works()
    test_empty_list_still_works()
    
    print("=" * 50)
    print("✅ All tests passed!")

