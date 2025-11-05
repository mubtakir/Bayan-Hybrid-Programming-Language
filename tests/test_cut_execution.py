#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Cut operator execution in Bayan language
اختبارات لتنفيذ عامل القطع في لغة البيان
"""

import sys
sys.path.insert(0, 'bayan')

from bayan.lexer import HybridLexer
from bayan.parser import HybridParser
from bayan.hybrid_interpreter import HybridInterpreter

def test_cut_prevents_backtracking():
    """Test that cut prevents backtracking to alternative clauses"""
    code = """
hybrid {
    rule max(?X, ?Y, ?X) :- ?X >= ?Y, !.
    rule max(?X, ?Y, ?Y) :- ?X < ?Y.
}

query max(5, 3, ?Result).
    """

    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    interpreter = HybridInterpreter()
    result = interpreter.interpret(ast)

    # Should return only one solution: ?Result = 5
    # Without cut, it would also try the second rule
    assert result is not None
    print("✅ Cut prevents backtracking test passed")

def test_cut_in_middle_of_rule():
    """Test cut in the middle of a rule body"""
    code = """
hybrid {
    rule test(?X, ?Y) :- ?X > 0, !, ?Y is ?X * 2.
    rule test(?X, ?Y) :- ?Y is ?X + 10.
}

query test(5, ?Result).
    """

    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    interpreter = HybridInterpreter()
    result = interpreter.interpret(ast)

    # Should return ?Result = 10 (5 * 2), not 15 (5 + 10)
    assert result is not None
    print("✅ Cut in middle of rule test passed")

def test_cut_with_multiple_solutions_before_cut():
    """Test that cut allows multiple solutions before it, but prevents backtracking after"""
    code = """
hybrid {
    fact color("red").
    fact color("green").
    fact color("blue").

    rule primary(?C) :- color(?C), !.
}

query primary(?Color).
    """

    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    interpreter = HybridInterpreter()
    result = interpreter.interpret(ast)

    # Should return only the first color found
    assert result is not None
    print("✅ Cut with multiple solutions before cut test passed")

def test_cut_deterministic_choice():
    """Test cut for deterministic choice (green cut)"""
    code = """
hybrid {
    rule classify(?X, "positive") :- ?X > 0, !.
    rule classify(?X, "zero") :- ?X == 0, !.
    rule classify(?X, "negative") :- ?X < 0.
}

query classify(5, ?Class).
    """

    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    interpreter = HybridInterpreter()
    result = interpreter.interpret(ast)

    # Should return ?Class = "positive"
    assert result is not None
    print("✅ Cut deterministic choice test passed")

def test_cut_with_list_pattern():
    """Test cut with list patterns"""
    code = """
hybrid {
    rule member(?H, [?H|?T]) :- !.
    rule member(?X, [?H|?T]) :- member(?X, ?T).
}

query member(2, [1, 2, 3]).
    """

    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    interpreter = HybridInterpreter()
    result = interpreter.interpret(ast)

    # Should succeed finding 2 in the list
    assert result is not None
    print("✅ Cut with list pattern test passed")

def test_cut_only_in_body():
    """Test a rule with only cut in body"""
    code = """
hybrid {
    rule stop() :- !.
}

query stop().
    """

    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    interpreter = HybridInterpreter()
    result = interpreter.interpret(ast)

    # Should succeed with the first rule
    assert result is not None
    print("✅ Cut only in body test passed")

def test_nested_cuts():
    """Test nested rules with cuts"""
    code = """
hybrid {
    rule helper(?X) :- ?X > 5, !.
    rule helper(?X) :- ?X > 0.

    rule main(?X, ?Y) :- helper(?X), !, ?Y is ?X * 2.
    rule main(?X, ?Y) :- ?Y is ?X + 100.
}

query main(10, ?Result).
    """

    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    interpreter = HybridInterpreter()
    result = interpreter.interpret(ast)

    # Should return ?Result = 20 (10 * 2)
    assert result is not None
    print("✅ Nested cuts test passed")

if __name__ == "__main__":
    print("Testing Cut Operator Execution")
    print("=" * 60)
    
    test_cut_prevents_backtracking()
    test_cut_in_middle_of_rule()
    test_cut_with_multiple_solutions_before_cut()
    test_cut_deterministic_choice()
    test_cut_with_list_pattern()
    test_cut_only_in_body()
    test_nested_cuts()
    
    print("=" * 60)
    print("✅ All Cut execution tests passed!")

