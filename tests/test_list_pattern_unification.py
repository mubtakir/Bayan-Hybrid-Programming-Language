"""
Tests for List Pattern Unification
اختبارات توحيد أنماط القوائم
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bayan'))

from bayan.logical_engine import LogicalEngine, Term, Substitution

def test_simple_list_pattern_unification():
    """Test unifying [H|T] with [1, 2, 3]"""
    engine = LogicalEngine()
    
    # Create pattern [?H|?T]
    pattern = {
        'list_pattern': True,
        'head': [Term('H', is_variable=True)],
        'tail': Term('T', is_variable=True)
    }
    
    # Create list [1, 2, 3]
    lst = [1, 2, 3]
    
    # Unify
    sub = Substitution()
    result = engine._unify(pattern, lst, sub)
    
    assert result is not None, "Unification should succeed"
    assert result.lookup('H') == 1, f"H should be 1, got {result.lookup('H')}"
    assert result.lookup('T') == [2, 3], f"T should be [2, 3], got {result.lookup('T')}"
    
    print("✅ Simple list pattern [H|T] unifies with [1, 2, 3]")
    print(f"   H = {result.lookup('H')}")
    print(f"   T = {result.lookup('T')}")

def test_multiple_heads_pattern():
    """Test unifying [H1, H2|T] with [1, 2, 3, 4]"""
    engine = LogicalEngine()
    
    # Create pattern [?H1, ?H2|?T]
    pattern = {
        'list_pattern': True,
        'head': [Term('H1', is_variable=True), Term('H2', is_variable=True)],
        'tail': Term('T', is_variable=True)
    }
    
    # Create list [1, 2, 3, 4]
    lst = [1, 2, 3, 4]
    
    # Unify
    sub = Substitution()
    result = engine._unify(pattern, lst, sub)
    
    assert result is not None, "Unification should succeed"
    assert result.lookup('H1') == 1
    assert result.lookup('H2') == 2
    assert result.lookup('T') == [3, 4]
    
    print("✅ Multiple heads [H1, H2|T] unifies with [1, 2, 3, 4]")
    print(f"   H1 = {result.lookup('H1')}")
    print(f"   H2 = {result.lookup('H2')}")
    print(f"   T = {result.lookup('T')}")

def test_empty_tail():
    """Test unifying [H|T] with [1]"""
    engine = LogicalEngine()
    
    # Create pattern [?H|?T]
    pattern = {
        'list_pattern': True,
        'head': [Term('H', is_variable=True)],
        'tail': Term('T', is_variable=True)
    }
    
    # Create list [1]
    lst = [1]
    
    # Unify
    sub = Substitution()
    result = engine._unify(pattern, lst, sub)
    
    assert result is not None, "Unification should succeed"
    assert result.lookup('H') == 1
    assert result.lookup('T') == [], "Tail should be empty list"
    
    print("✅ Pattern [H|T] unifies with [1], T = []")
    print(f"   H = {result.lookup('H')}")
    print(f"   T = {result.lookup('T')}")

def test_pattern_too_long():
    """Test that [H1, H2|T] fails to unify with [1]"""
    engine = LogicalEngine()
    
    # Create pattern [?H1, ?H2|?T]
    pattern = {
        'list_pattern': True,
        'head': [Term('H1', is_variable=True), Term('H2', is_variable=True)],
        'tail': Term('T', is_variable=True)
    }
    
    # Create list [1] (too short)
    lst = [1]
    
    # Unify
    sub = Substitution()
    result = engine._unify(pattern, lst, sub)
    
    assert result is None, "Unification should fail"
    
    print("✅ Pattern [H1, H2|T] correctly fails with [1]")

def test_mixed_pattern():
    """Test unifying [1, ?X|?Rest] with [1, 2, 3]"""
    engine = LogicalEngine()
    
    # Create pattern [1, ?X|?Rest]
    pattern = {
        'list_pattern': True,
        'head': [1, Term('X', is_variable=True)],
        'tail': Term('Rest', is_variable=True)
    }
    
    # Create list [1, 2, 3]
    lst = [1, 2, 3]
    
    # Unify
    sub = Substitution()
    result = engine._unify(pattern, lst, sub)
    
    assert result is not None, "Unification should succeed"
    assert result.lookup('X') == 2
    assert result.lookup('Rest') == [3]
    
    print("✅ Mixed pattern [1, ?X|?Rest] unifies with [1, 2, 3]")
    print(f"   X = {result.lookup('X')}")
    print(f"   Rest = {result.lookup('Rest')}")

def test_regular_list_unification():
    """Test that regular list unification still works"""
    engine = LogicalEngine()
    
    # Two regular lists
    lst1 = [1, 2, 3]
    lst2 = [1, 2, 3]
    
    # Unify
    sub = Substitution()
    result = engine._unify(lst1, lst2, sub)
    
    assert result is not None, "Unification should succeed"
    
    print("✅ Regular list [1, 2, 3] unifies with [1, 2, 3]")

def test_regular_list_with_variables():
    """Test unifying [1, ?X, 3] with [1, 2, 3]"""
    engine = LogicalEngine()
    
    # List with variable
    lst1 = [1, Term('X', is_variable=True), 3]
    lst2 = [1, 2, 3]
    
    # Unify
    sub = Substitution()
    result = engine._unify(lst1, lst2, sub)
    
    assert result is not None, "Unification should succeed"
    assert result.lookup('X') == 2
    
    print("✅ List [1, ?X, 3] unifies with [1, 2, 3]")
    print(f"   X = {result.lookup('X')}")

if __name__ == '__main__':
    print("Testing List Pattern Unification...")
    print("=" * 60)
    
    test_simple_list_pattern_unification()
    print()
    test_multiple_heads_pattern()
    print()
    test_empty_tail()
    print()
    test_pattern_too_long()
    print()
    test_mixed_pattern()
    print()
    test_regular_list_unification()
    print()
    test_regular_list_with_variables()
    
    print("=" * 60)
    print("✅ All unification tests passed!")

