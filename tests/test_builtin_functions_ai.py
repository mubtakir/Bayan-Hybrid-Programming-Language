"""
Tests for AI/ML-related built-in functions
اختبارات للدوال المدمجة المتعلقة بالذكاء الاصطناعي
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bayan'))

import pytest
from bayan import HybridLexer, HybridParser, HybridInterpreter


def test_sum_function():
    """Test sum() function"""
    code = """
    numbers = [1, 2, 3, 4, 5]
    total = sum(numbers)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)

    assert interpreter.traditional.global_env['total'] == 15


def test_sum_with_start():
    """Test sum() with start value"""
    code = """
    numbers = [1, 2, 3]
    total = sum(numbers, 10)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['total'] == 16


def test_min_function():
    """Test min() function"""
    code = """
    numbers = [5, 2, 8, 1, 9]
    minimum = min(numbers)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['minimum'] == 1


def test_min_multiple_args():
    """Test min() with multiple arguments"""
    code = """
    minimum = min(5, 2, 8, 1, 9)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['minimum'] == 1


def test_max_function():
    """Test max() function"""
    code = """
    numbers = [5, 2, 8, 1, 9]
    maximum = max(numbers)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['maximum'] == 9


def test_max_multiple_args():
    """Test max() with multiple arguments"""
    code = """
    maximum = max(5, 2, 8, 1, 9)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['maximum'] == 9


def test_sorted_function():
    """Test sorted() function"""
    code = """
    numbers = [5, 2, 8, 1, 9]
    sorted_nums = sorted(numbers)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['sorted_nums'] == [1, 2, 5, 8, 9]


def test_sorted_reverse():
    """Test sorted() with reverse"""
    code = """
    numbers = [5, 2, 8, 1, 9]
    sorted_nums = sorted(numbers, True)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['sorted_nums'] == [9, 8, 5, 2, 1]


def test_enumerate_function():
    """Test enumerate() function"""
    code = """
    items = ["a", "b", "c"]
    enumerated = enumerate(items)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    result = interpreter.traditional.global_env['enumerated']
    assert result == [(0, "a"), (1, "b"), (2, "c")]


def test_enumerate_with_start():
    """Test enumerate() with start value"""
    code = """
    items = ["a", "b", "c"]
    enumerated = enumerate(items, 1)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    result = interpreter.traditional.global_env['enumerated']
    assert result == [(1, "a"), (2, "b"), (3, "c")]


def test_zip_function():
    """Test zip() function"""
    code = """
    list1 = [1, 2, 3]
    list2 = ["a", "b", "c"]
    zipped = zip(list1, list2)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    result = interpreter.traditional.global_env['zipped']
    assert result == [(1, "a"), (2, "b"), (3, "c")]


def test_zip_multiple_lists():
    """Test zip() with multiple lists"""
    code = """
    list1 = [1, 2]
    list2 = ["a", "b"]
    list3 = [True, False]
    zipped = zip(list1, list2, list3)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    result = interpreter.traditional.global_env['zipped']
    assert result == [(1, "a", True), (2, "b", False)]


def test_map_function():
    """Test map() function with user-defined function"""
    code = """
    def square(x): {
        return x * x
    }
    
    numbers = [1, 2, 3, 4]
    squared = map(square, numbers)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    result = interpreter.traditional.global_env['squared']
    assert result == [1, 4, 9, 16]


def test_filter_function():
    """Test filter() function with user-defined function"""
    code = """
    def is_even(x): {
        return x % 2 == 0
    }
    
    numbers = [1, 2, 3, 4, 5, 6]
    evens = filter(is_even, numbers)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    result = interpreter.traditional.global_env['evens']
    assert result == [2, 4, 6]


def test_all_function():
    """Test all() function"""
    code = """
    all_true = all([True, True, True])
    has_false = all([True, False, True])
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['all_true'] == True
    assert interpreter.traditional.global_env['has_false'] == False


def test_any_function():
    """Test any() function"""
    code = """
    has_true = any([False, True, False])
    all_false = any([False, False, False])
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['has_true'] == True
    assert interpreter.traditional.global_env['all_false'] == False


def test_abs_function():
    """Test abs() function"""
    code = """
    positive = abs(5)
    negative = abs(-5)
    zero = abs(0)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['positive'] == 5
    assert interpreter.traditional.global_env['negative'] == 5
    assert interpreter.traditional.global_env['zero'] == 0


def test_round_function():
    """Test round() function"""
    code = """
    rounded = round(3.7)
    rounded_down = round(3.2)
    rounded_decimals = round(3.14159, 2)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['rounded'] == 4
    assert interpreter.traditional.global_env['rounded_down'] == 3
    assert interpreter.traditional.global_env['rounded_decimals'] == 3.14


def test_pow_function():
    """Test pow() function"""
    code = """
    power = pow(2, 3)
    power_mod = pow(2, 3, 5)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['power'] == 8
    assert interpreter.traditional.global_env['power_mod'] == 3  # (2^3) % 5 = 8 % 5 = 3


def test_reversed_function():
    """Test reversed() function"""
    code = """
    numbers = [1, 2, 3, 4, 5]
    reversed_nums = reversed(numbers)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['reversed_nums'] == [5, 4, 3, 2, 1]

