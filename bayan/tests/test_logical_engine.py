"""
Tests for the Logical Engine
اختبارات المحرك المنطقي
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bayan.logical_engine import (
    LogicalEngine, Term, Predicate, Fact, Rule, Substitution
)

def test_term_creation():
    """Test term creation"""
    const = Term("john", is_variable=False)
    var = Term("X", is_variable=True)
    
    assert const.value == "john"
    assert not const.is_variable
    assert var.value == "X"
    assert var.is_variable
    print("✓ test_term_creation passed")

def test_predicate_creation():
    """Test predicate creation"""
    args = [Term("john", False), Term("mary", False)]
    pred = Predicate("parent", args)
    
    assert pred.name == "parent"
    assert len(pred.args) == 2
    assert pred.args[0].value == "john"
    print("✓ test_predicate_creation passed")

def test_fact_addition():
    """Test adding facts to knowledge base"""
    engine = LogicalEngine()
    
    args = [Term("john", False), Term("mary", False)]
    pred = Predicate("parent", args)
    fact = Fact(pred)
    
    engine.add_fact(fact)
    
    assert "parent" in engine.knowledge_base
    assert len(engine.knowledge_base["parent"]) == 1
    print("✓ test_fact_addition passed")

def test_simple_query():
    """Test simple query"""
    engine = LogicalEngine()
    
    # Add facts
    fact1 = Fact(Predicate("parent", [Term("john", False), Term("mary", False)]))
    fact2 = Fact(Predicate("parent", [Term("john", False), Term("tom", False)]))
    
    engine.add_fact(fact1)
    engine.add_fact(fact2)
    
    # Query
    goal = Predicate("parent", [Term("john", False), Term("X", True)])
    solutions = engine.query(goal)
    
    assert len(solutions) == 2
    assert solutions[0].lookup("X").value == "mary"
    assert solutions[1].lookup("X").value == "tom"
    print("✓ test_simple_query passed")

def test_rule_application():
    """Test rule application"""
    engine = LogicalEngine()

    # Add facts
    engine.add_fact(Fact(Predicate("parent", [Term("john", False), Term("mary", False)])))
    engine.add_fact(Fact(Predicate("parent", [Term("mary", False), Term("susan", False)])))

    # Add rule: grandparent(X, Z) :- parent(X, Y), parent(Y, Z)
    head = Predicate("grandparent", [Term("X", True), Term("Z", True)])
    body = [
        Predicate("parent", [Term("X", True), Term("Y", True)]),
        Predicate("parent", [Term("Y", True), Term("Z", True)])
    ]
    rule = Rule(head, body)
    engine.add_rule(rule)

    # Query
    goal = Predicate("grandparent", [Term("john", False), Term("Z", True)])
    solutions = engine.query(goal)

    assert len(solutions) >= 1, f"Expected at least 1 solution, got {len(solutions)}"
    # Check if Z is bound to susan
    z_value = solutions[0].lookup("Z")
    assert z_value is not None, "Z should be bound"
    # The value might be a Term object
    if isinstance(z_value, Term):
        assert z_value.value == "susan", f"Expected susan, got {z_value.value}"
    else:
        assert z_value == "susan", f"Expected susan, got {z_value}"
    print("✓ test_rule_application passed")

def test_unification():
    """Test unification"""
    engine = LogicalEngine()
    
    term1 = Term("X", True)
    term2 = Term("john", False)
    
    sub = Substitution()
    result = engine._unify(term1, term2, sub)
    
    assert result is not None
    assert result.lookup("X").value == "john"
    print("✓ test_unification passed")

def test_occurs_check():
    """Test occurs check"""
    engine = LogicalEngine()
    
    var = Term("X", True)
    term = Predicate("f", [Term("X", True)])
    
    sub = Substitution()
    result = engine._unify(var, term, sub)
    
    # Should fail due to occurs check
    assert result is None
    print("✓ test_occurs_check passed")

def test_multiple_solutions():
    """Test multiple solutions"""
    engine = LogicalEngine()
    
    # Add facts
    engine.add_fact(Fact(Predicate("color", [Term("red", False)])))
    engine.add_fact(Fact(Predicate("color", [Term("blue", False)])))
    engine.add_fact(Fact(Predicate("color", [Term("green", False)])))
    
    # Query
    goal = Predicate("color", [Term("X", True)])
    solutions = engine.query(goal)
    
    assert len(solutions) == 3
    colors = [sol.lookup("X").value for sol in solutions]
    assert "red" in colors
    assert "blue" in colors
    assert "green" in colors
    print("✓ test_multiple_solutions passed")

def test_complex_rule():
    """Test complex rule with multiple conditions"""
    engine = LogicalEngine()
    
    # Add facts
    engine.add_fact(Fact(Predicate("parent", [Term("john", False), Term("mary", False)])))
    engine.add_fact(Fact(Predicate("parent", [Term("mary", False), Term("susan", False)])))
    engine.add_fact(Fact(Predicate("male", [Term("john", False)])))
    engine.add_fact(Fact(Predicate("male", [Term("tom", False)])))
    
    # Add rule: grandfather(X, Z) :- parent(X, Y), parent(Y, Z), male(X)
    head = Predicate("grandfather", [Term("X", True), Term("Z", True)])
    body = [
        Predicate("parent", [Term("X", True), Term("Y", True)]),
        Predicate("parent", [Term("Y", True), Term("Z", True)]),
        Predicate("male", [Term("X", True)])
    ]
    rule = Rule(head, body)
    engine.add_rule(rule)
    
    # Query
    goal = Predicate("grandfather", [Term("john", False), Term("Z", True)])
    solutions = engine.query(goal)
    
    assert len(solutions) == 1
    assert solutions[0].lookup("Z").value == "susan"
    print("✓ test_complex_rule passed")

if __name__ == "__main__":
    test_term_creation()
    test_predicate_creation()
    test_fact_addition()
    test_simple_query()
    test_rule_application()
    test_unification()
    test_occurs_check()
    test_multiple_solutions()
    test_complex_rule()
    print("\n✓ All logical engine tests passed!")

