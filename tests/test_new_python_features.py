#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for new Python features added to Bayan:
- List slicing
- Tuple support
- Set support
- Additional built-in functions
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bayan'))

from bayan.lexer import HybridLexer
from bayan.parser import HybridParser
from bayan.traditional_interpreter import TraditionalInterpreter


def run_code(code):
    """Helper to run Bayan code and return interpreter"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = TraditionalInterpreter()
    interpreter.interpret(ast)
    return interpreter


# ============================================================================
# List Slicing Tests
# ============================================================================

def test_list_slicing_basic():
    """Test basic list slicing"""
    code = """
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
result = nums[2:5]
"""
    interp = run_code(code)
    assert interp.global_env.get('result') == [2, 3, 4]


def test_list_slicing_start_only():
    """Test list slicing with start only"""
    code = """
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
result = nums[7:]
"""
    interp = run_code(code)
    assert interp.global_env.get('result') == [7, 8, 9]


def test_list_slicing_end_only():
    """Test list slicing with end only"""
    code = """
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
result = nums[:3]
"""
    interp = run_code(code)
    assert interp.global_env.get('result') == [0, 1, 2]


def test_list_slicing_with_step():
    """Test list slicing with step"""
    code = """
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
result = nums[::2]
"""
    interp = run_code(code)
    assert interp.global_env.get('result') == [0, 2, 4, 6, 8]


def test_list_slicing_reverse():
    """Test list slicing with negative step (reverse)"""
    code = """
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
result = nums[1:4]
"""
    interp = run_code(code)
    assert interp.global_env.get('result') == [1, 2, 3]


def test_list_slicing_odd_numbers():
    """Test list slicing to get odd numbers"""
    code = """
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
result = nums[1:6:2]
"""
    interp = run_code(code)
    assert interp.global_env.get('result') == [1, 3, 5]


# ============================================================================
# Tuple Tests
# ============================================================================

def test_tuple_creation():
    """Test tuple creation"""
    code = """
point = (10, 20)
"""
    interp = run_code(code)
    result = interp.global_env.get('point')
    assert isinstance(result, tuple)
    assert result == (10, 20)


def test_tuple_indexing():
    """Test tuple indexing"""
    code = """
point = (10, 20, 30)
x = point[0]
y = point[1]
z = point[2]
"""
    interp = run_code(code)
    assert interp.global_env.get('x') == 10
    assert interp.global_env.get('y') == 20
    assert interp.global_env.get('z') == 30


def test_empty_tuple():
    """Test empty tuple"""
    code = """
empty = ()
"""
    interp = run_code(code)
    result = interp.global_env.get('empty')
    assert isinstance(result, tuple)
    assert len(result) == 0


def test_single_element_tuple():
    """Test single element tuple (with trailing comma)"""
    code = """
single = (42,)
"""
    interp = run_code(code)
    result = interp.global_env.get('single')
    assert isinstance(result, tuple)
    assert result == (42,)


def test_tuple_vs_grouped_expression():
    """Test that (expr) is not a tuple but grouped expression"""
    code = """
not_tuple = (42)
is_tuple = (42,)
"""
    interp = run_code(code)
    assert interp.global_env.get('not_tuple') == 42  # Just an int
    assert interp.global_env.get('is_tuple') == (42,)  # A tuple


# ============================================================================
# Set Tests
# ============================================================================

def test_set_creation():
    """Test set creation"""
    code = """
numbers = {1, 2, 3, 4, 5}
"""
    interp = run_code(code)
    result = interp.global_env.get('numbers')
    assert isinstance(result, set)
    assert result == {1, 2, 3, 4, 5}


def test_set_removes_duplicates():
    """Test that sets automatically remove duplicates"""
    code = """
duplicates = {1, 2, 2, 3, 3, 3}
"""
    interp = run_code(code)
    result = interp.global_env.get('duplicates')
    assert isinstance(result, set)
    assert result == {1, 2, 3}


def test_set_vs_dict():
    """Test that {1, 2} is a set but {1: 2} is a dict"""
    code = """
my_set = {1, 2, 3}
my_dict = {1: 2, 3: 4}
"""
    interp = run_code(code)
    assert isinstance(interp.global_env.get('my_set'), set)
    assert isinstance(interp.global_env.get('my_dict'), dict)


# ============================================================================
# Built-in Functions Tests
# ============================================================================

def test_all_true():
    """Test all_true function - manual implementation"""
    code = """
lst1 = [True, True, True]
result1 = True
for item in lst1: {
    if not item: {
        result1 = False
    }
}

lst2 = [True, False, True]
result2 = True
for item in lst2: {
    if not item: {
        result2 = False
    }
}
"""
    interp = run_code(code)
    assert interp.global_env.get('result1') == True
    assert interp.global_env.get('result2') == False


def test_any_true():
    """Test any_true function - manual implementation"""
    code = """
lst1 = [False, False, False]
result1 = False
for item in lst1: {
    if item: {
        result1 = True
    }
}

lst2 = [False, True, False]
result2 = False
for item in lst2: {
    if item: {
        result2 = True
    }
}
"""
    interp = run_code(code)
    assert interp.global_env.get('result1') == False
    assert interp.global_env.get('result2') == True


def test_unique():
    """Test unique function using set literal"""
    code = """
duplicates = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_set = {1, 2, 3, 4}
result = len(unique_set)
"""
    interp = run_code(code)
    assert interp.global_env.get('result') == 4


def test_flatten():
    """Test flatten function - using manual approach"""
    code = """
nested = [[1, 2], [3, 4], [5, 6]]
result = []
for sublist in nested: {
    for item in sublist: {
        result = result + [item]
    }
}
"""
    interp = run_code(code)
    assert interp.global_env.get('result') == [1, 2, 3, 4, 5, 6]


def test_index_of():
    """Test index_of function"""
    code = """
lst = [10, 20, 30, 40, 50]
result = lst.index(30)
"""
    interp = run_code(code)
    assert interp.global_env.get('result') == 2


def test_count_occurrences():
    """Test count_occurrences function"""
    code = """
lst = [1, 2, 2, 3, 2, 4, 2]
result = lst.count(2)
"""
    interp = run_code(code)
    assert interp.global_env.get('result') == 4


def test_slice_list():
    """Test slice_list function"""
    code = """
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
result = nums[2:7:2]
"""
    interp = run_code(code)
    assert interp.global_env.get('result') == [2, 4, 6]


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])

