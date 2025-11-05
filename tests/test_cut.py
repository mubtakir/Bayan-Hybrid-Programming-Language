#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for cut operator (!) in Bayan language
اختبارات لعامل القطع (!) في لغة البيان
"""

import sys
sys.path.insert(0, 'bayan')

from bayan.lexer import HybridLexer, TokenType
from bayan.parser import HybridParser
from bayan.ast_nodes import Cut, HybridBlock

def test_lexer_cut_operator():
    """Test that lexer recognizes '!' as CUT token"""
    code = "!"
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    
    # Find CUT token
    cut_tokens = [t for t in tokens if t.type == TokenType.CUT]
    assert len(cut_tokens) == 1, "Should have one CUT token"
    print("✅ Lexer recognizes '!' as CUT")

def test_parse_cut_simple():
    """Test parsing simple cut in rule"""
    code = """
hybrid {
    rule max(?X, ?Y, ?X) :- ?X >= ?Y, !.
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    assert len(ast.statements) == 1, "Should have one statement"
    hybrid_block = ast.statements[0]
    assert isinstance(hybrid_block, HybridBlock), "Should be HybridBlock"

    # Check that rule contains cut
    rule = hybrid_block.logical_stmts[0]
    # The cut should be in the body
    has_cut = any(isinstance(goal, Cut) for goal in rule.body)
    assert has_cut, "Rule should contain cut operator"
    print("✅ Parser handles 'rule max(?X, ?Y, ?X) :- ?X >= ?Y, !.'")

def test_parse_cut_in_middle():
    """Test parsing cut in middle of rule body"""
    code = """
hybrid {
    rule process(?X) :- check(?X), !, action(?X).
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    hybrid_block = ast.statements[0]
    rule = hybrid_block.logical_stmts[0]
    
    # Check that cut is in the middle
    has_cut = any(isinstance(goal, Cut) for goal in rule.body)
    assert has_cut, "Rule should contain cut operator"
    print("✅ Parser handles cut in middle of rule body")

def test_parse_multiple_cuts():
    """Test parsing multiple cuts (though unusual)"""
    code = """
hybrid {
    rule test(?X) :- a(?X), !, b(?X), !, c(?X).
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    hybrid_block = ast.statements[0]
    rule = hybrid_block.logical_stmts[0]

    # Count cuts
    cut_count = sum(1 for goal in rule.body if isinstance(goal, Cut))
    assert cut_count == 2, f"Should have 2 cuts, got {cut_count}"
    print("✅ Parser handles multiple cuts in rule")

def test_parse_cut_only():
    """Test parsing rule with only cut"""
    code = """
hybrid {
    rule stop() :- !.
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    hybrid_block = ast.statements[0]
    rule = hybrid_block.logical_stmts[0]
    
    assert len(rule.body) == 1, "Rule should have one goal"
    assert isinstance(rule.body[0], Cut), "Goal should be Cut"
    print("✅ Parser handles rule with only cut")

def test_parse_cut_with_is():
    """Test parsing cut with 'is' operator"""
    code = """
hybrid {
    rule factorial(?N, ?F) :- 
        ?N > 0,
        !,
        ?N1 is ?N - 1,
        factorial(?N1, ?F1),
        ?F is ?N * ?F1.
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    hybrid_block = ast.statements[0]
    rule = hybrid_block.logical_stmts[0]

    has_cut = any(isinstance(goal, Cut) for goal in rule.body)
    assert has_cut, "Rule should contain cut"
    print("✅ Parser handles cut with 'is' operator")

def test_parse_cut_deterministic_choice():
    """Test parsing cut for deterministic choice"""
    code = """
hybrid {
    rule classify(?X, "positive") :- ?X > 0, !.
    rule classify(?X, "zero") :- ?X == 0, !.
    rule classify(?X, "negative") :- ?X < 0.
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    hybrid_block = ast.statements[0]

    # Check that first two rules have cuts
    rule1 = hybrid_block.logical_stmts[0]
    rule2 = hybrid_block.logical_stmts[1]
    
    has_cut1 = any(isinstance(goal, Cut) for goal in rule1.body)
    has_cut2 = any(isinstance(goal, Cut) for goal in rule2.body)
    
    assert has_cut1, "First rule should have cut"
    assert has_cut2, "Second rule should have cut"
    print("✅ Parser handles cut for deterministic choice")

def test_parse_cut_with_list_pattern():
    """Test parsing cut with list patterns"""
    code = """
hybrid {
    rule member(?H, [?H|?T]) :- !.
    rule member(?X, [?H|?T]) :- member(?X, ?T).
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    hybrid_block = ast.statements[0]
    rule1 = hybrid_block.logical_stmts[0]

    has_cut = any(isinstance(goal, Cut) for goal in rule1.body)
    assert has_cut, "First member rule should have cut"
    print("✅ Parser handles cut with list patterns")

def test_parse_cut_ast_structure():
    """Test that Cut AST node is created correctly"""
    code = """
hybrid {
    rule test() :- !.
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    hybrid_block = ast.statements[0]
    rule = hybrid_block.logical_stmts[0]
    cut_node = rule.body[0]
    
    assert isinstance(cut_node, Cut), "Should be Cut instance"
    assert repr(cut_node) == "Cut(!)", f"Repr should be 'Cut(!)', got {repr(cut_node)}"
    print("✅ Cut AST node structure is correct")

def test_parse_cut_green_cut():
    """Test parsing green cut (doesn't change semantics)"""
    code = """
hybrid {
    rule min(?X, ?Y, ?X) :- ?X <= ?Y, !.
}
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    hybrid_block = ast.statements[0]
    rule1 = hybrid_block.logical_stmts[0]

    has_cut = any(isinstance(goal, Cut) for goal in rule1.body)
    assert has_cut, "Min rule should have cut"
    print("✅ Parser handles green cut")

if __name__ == "__main__":
    print("Testing Cut Operator (!)")
    print("=" * 50)
    
    test_lexer_cut_operator()
    test_parse_cut_simple()
    test_parse_cut_in_middle()
    test_parse_multiple_cuts()
    test_parse_cut_only()
    test_parse_cut_with_is()
    test_parse_cut_deterministic_choice()
    test_parse_cut_with_list_pattern()
    test_parse_cut_ast_structure()
    test_parse_cut_green_cut()
    
    print("=" * 50)
    print("✅ All cut operator tests passed!")

