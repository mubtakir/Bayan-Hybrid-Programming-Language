"""
Tests for 'is' operator in logical programming
اختبارات لعامل 'is' في البرمجة المنطقية
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bayan'))

from bayan.lexer import HybridLexer, TokenType
from bayan.parser import HybridParser
from bayan.ast_nodes import IsExpression

def test_lexer_is_keyword():
    """Test that lexer recognizes 'is' keyword"""
    code = 'is'
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.IS
    print("✅ Lexer recognizes 'is' keyword")

def test_parse_simple_is_expression():
    """Test parsing ?X is 5 + 3"""
    code = '?X is 5 + 3'
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    
    # Parse as logical goal
    ast = parser.parse_logical_goal()
    
    assert isinstance(ast, IsExpression)
    assert ast.variable.value == 'X'
    assert ast.variable.is_variable == True
    print("✅ Parser handles '?X is 5 + 3'")

def test_parse_complex_is_expression():
    """Test parsing ?Result is (?N * 2) + 1"""
    code = '?Result is ?N * 2 + 1'
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    
    ast = parser.parse_logical_goal()
    
    assert isinstance(ast, IsExpression)
    assert ast.variable.value == 'Result'
    print("✅ Parser handles complex arithmetic: '?Result is ?N * 2 + 1'")

def test_evaluate_simple_is():
    """Test evaluating ?X is 5 + 3"""
    from bayan.logical_engine import LogicalEngine, Substitution, Term
    from bayan.ast_nodes import IsExpression, BinaryOp, Number

    engine = LogicalEngine()

    # Create: ?X is 5 + 3
    is_expr = IsExpression(
        Term('X', is_variable=True),
        BinaryOp('+', Number(5), Number(3))
    )

    sub = Substitution()
    result = engine._evaluate_is_expression(is_expr, sub)

    assert result is not None
    assert result.lookup('X') == 8
    print("✅ Evaluation: ?X is 5 + 3 → X = 8")

def test_evaluate_is_with_variable():
    """Test evaluating ?Y is ?X + 3 where X = 5"""
    from bayan.logical_engine import LogicalEngine, Substitution, Term
    from bayan.ast_nodes import IsExpression, BinaryOp, Number, Variable

    engine = LogicalEngine()

    # Create: ?Y is ?X + 3
    is_expr = IsExpression(
        Term('Y', is_variable=True),
        BinaryOp('+', Variable('?X'), Number(3))
    )

    # Pre-bind X = 5
    sub = Substitution()
    sub.bind('X', 5)

    result = engine._evaluate_is_expression(is_expr, sub)

    assert result is not None
    assert result.lookup('Y') == 8
    print("✅ Evaluation: ?Y is ?X + 3 where X=5 → Y = 8")

def test_evaluate_multiplication():
    """Test ?Result is 6 * 7"""
    from bayan.logical_engine import LogicalEngine, Substitution, Term
    from bayan.ast_nodes import IsExpression, BinaryOp, Number

    engine = LogicalEngine()

    is_expr = IsExpression(
        Term('Result', is_variable=True),
        BinaryOp('*', Number(6), Number(7))
    )

    sub = Substitution()
    result = engine._evaluate_is_expression(is_expr, sub)

    assert result is not None
    assert result.lookup('Result') == 42
    print("✅ Evaluation: ?Result is 6 * 7 → Result = 42")

def test_evaluate_division():
    """Test ?Result is 10 / 2"""
    from bayan.logical_engine import LogicalEngine, Substitution, Term
    from bayan.ast_nodes import IsExpression, BinaryOp, Number

    engine = LogicalEngine()

    is_expr = IsExpression(
        Term('Result', is_variable=True),
        BinaryOp('/', Number(10), Number(2))
    )

    sub = Substitution()
    result = engine._evaluate_is_expression(is_expr, sub)

    assert result is not None
    assert result.lookup('Result') == 5.0
    print("✅ Evaluation: ?Result is 10 / 2 → Result = 5.0")

def test_evaluate_power():
    """Test ?Result is 2 ** 3"""
    from bayan.logical_engine import LogicalEngine, Substitution, Term
    from bayan.ast_nodes import IsExpression, BinaryOp, Number

    engine = LogicalEngine()

    is_expr = IsExpression(
        Term('Result', is_variable=True),
        BinaryOp('**', Number(2), Number(3))
    )

    sub = Substitution()
    result = engine._evaluate_is_expression(is_expr, sub)

    assert result is not None
    assert result.lookup('Result') == 8
    print("✅ Evaluation: ?Result is 2 ** 3 → Result = 8")

def test_comparison_greater_than():
    """Test ?N > 0"""
    from bayan.logical_engine import LogicalEngine, Substitution, Predicate, Term
    
    engine = LogicalEngine()
    
    # Create comparison predicate
    comp = Predicate('_compare_>', [Term('N', is_variable=True), Term(0, is_variable=False)])
    
    # Test with N = 5
    sub = Substitution()
    sub.bind('N', 5)
    
    result = engine._evaluate_comparison(comp, sub)
    assert result is not None
    print("✅ Comparison: ?N > 0 where N=5 → True")
    
    # Test with N = -1
    sub2 = Substitution()
    sub2.bind('N', -1)
    
    result2 = engine._evaluate_comparison(comp, sub2)
    assert result2 is None
    print("✅ Comparison: ?N > 0 where N=-1 → False")

def test_complex_arithmetic():
    """Test ?Result is (?N - 1) * 2"""
    from bayan.logical_engine import LogicalEngine, Substitution, Term
    from bayan.ast_nodes import IsExpression, BinaryOp, Number, Variable

    engine = LogicalEngine()

    # Create: ?Result is (?N - 1) * 2
    is_expr = IsExpression(
        Term('Result', is_variable=True),
        BinaryOp('*',
            BinaryOp('-', Variable('?N'), Number(1)),
            Number(2)
        )
    )

    # Pre-bind N = 5
    sub = Substitution()
    sub.bind('N', 5)

    result = engine._evaluate_is_expression(is_expr, sub)

    assert result is not None
    assert result.lookup('Result') == 8  # (5 - 1) * 2 = 8
    print("✅ Complex: ?Result is (?N - 1) * 2 where N=5 → Result = 8")

if __name__ == '__main__':
    print("Testing 'is' Operator...")
    print("=" * 60)
    
    test_lexer_is_keyword()
    test_parse_simple_is_expression()
    test_parse_complex_is_expression()
    print()
    
    test_evaluate_simple_is()
    test_evaluate_is_with_variable()
    test_evaluate_multiplication()
    test_evaluate_division()
    test_evaluate_power()
    test_comparison_greater_than()
    test_complex_arithmetic()
    
    print("=" * 60)
    print("✅ All 'is' operator tests passed!")

