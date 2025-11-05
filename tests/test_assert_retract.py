"""
Tests for assert/retract dynamic knowledge base
اختبارات لقاعدة المعرفة الديناميكية (assert/retract)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bayan'))

import pytest
from bayan.logical_engine import LogicalEngine, Fact, Rule, Predicate, Term


def test_assertz_fact():
    """Test assertz to add facts dynamically"""
    engine = LogicalEngine()

    # Add initial facts
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('bob')])))
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('liz')])))

    # Query
    goal = Predicate('parent', [Term('tom'), Term('X', is_variable=True)])
    solutions = engine.query(goal)

    # Should have 2 solutions
    assert len(solutions) == 2

    # Now add a new fact using assertz
    new_fact = Fact(Predicate('parent', [Term('tom'), Term('ann')]))
    engine.assertz(new_fact)

    # Query again
    solutions2 = engine.query(goal)

    # Should now have 3 solutions
    assert len(solutions2) == 3


def test_asserta_fact():
    """Test asserta to add facts at the beginning"""
    engine = LogicalEngine()

    # Add initial facts
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('bob')])))
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('liz')])))

    # Add a new fact at the beginning
    new_fact = Fact(Predicate('parent', [Term('tom'), Term('ann')]))
    engine.asserta(new_fact)

    # Query
    goal = Predicate('parent', [Term('tom'), Term('X', is_variable=True)])
    solutions = engine.query(goal)

    # Should have 3 solutions, with 'ann' first
    assert len(solutions) == 3
    assert solutions[0].bindings['X'].value == 'ann'


def test_retract_fact():
    """Test retract to remove a fact"""
    engine = LogicalEngine()

    # Add initial facts
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('bob')])))
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('liz')])))
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('ann')])))

    # Query
    goal = Predicate('parent', [Term('tom'), Term('X', is_variable=True)])
    solutions = engine.query(goal)

    # Should have 3 solutions
    assert len(solutions) == 3

    # Retract one fact
    fact_to_remove = Predicate('parent', [Term('tom'), Term('liz')])
    success = engine.retract(fact_to_remove)
    assert success == True

    # Query again
    solutions2 = engine.query(goal)

    # Should now have 2 solutions
    assert len(solutions2) == 2
    # liz should not be in the results
    names = [s.bindings['X'].value for s in solutions2]
    assert 'liz' not in names


def test_retractall_facts():
    """Test retractall to remove all matching facts"""
    engine = LogicalEngine()

    # Add initial facts
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('bob')])))
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('liz')])))
    engine.add_fact(Fact(Predicate('parent', [Term('bob'), Term('ann')])))
    engine.add_fact(Fact(Predicate('parent', [Term('bob'), Term('pat')])))

    # Query for bob's children
    goal1 = Predicate('parent', [Term('bob'), Term('X', is_variable=True)])
    solutions1 = engine.query(goal1)

    # Should have 2 solutions for bob
    assert len(solutions1) == 2

    # Retract all facts with bob as parent
    pattern = Predicate('parent', [Term('bob'), Term('X', is_variable=True)])
    count = engine.retractall(pattern)
    assert count == 2

    # Query again
    solutions2 = engine.query(goal1)

    # Should have no solutions
    assert len(solutions2) == 0

    # But tom's children should still be there
    goal2 = Predicate('parent', [Term('tom'), Term('X', is_variable=True)])
    solutions3 = engine.query(goal2)
    assert len(solutions3) == 2


def test_dynamic_learning_expert_system():
    """Test a simple expert system that learns dynamically"""
    engine = LogicalEngine()

    # Add initial knowledge
    engine.add_fact(Fact(Predicate('symptom', [Term('john'), Term('fever')])))
    engine.add_fact(Fact(Predicate('symptom', [Term('john'), Term('cough')])))

    # Add rule: if fever and cough, then flu
    head = Predicate('diagnosis', [Term('X', is_variable=True), Term('flu')])
    body = [
        Predicate('symptom', [Term('X', is_variable=True), Term('fever')]),
        Predicate('symptom', [Term('X', is_variable=True), Term('cough')])
    ]
    engine.add_rule(Rule(head, body))

    # Query john's diagnosis
    goal1 = Predicate('diagnosis', [Term('john'), Term('D', is_variable=True)])
    solutions1 = engine.query(goal1)

    # John should be diagnosed with flu
    assert len(solutions1) == 1
    assert solutions1[0].bindings['D'].value == 'flu'

    # Now add a new symptom for mary
    new_symptom1 = Fact(Predicate('symptom', [Term('mary'), Term('fever')]))
    new_symptom2 = Fact(Predicate('symptom', [Term('mary'), Term('cough')]))
    engine.assertz(new_symptom1)
    engine.assertz(new_symptom2)

    # Query for mary's diagnosis
    goal2 = Predicate('diagnosis', [Term('mary'), Term('D', is_variable=True)])
    solutions2 = engine.query(goal2)

    # Mary should also be diagnosed with flu
    assert len(solutions2) == 1
    assert solutions2[0].bindings['D'].value == 'flu'

    # Now retract john's fever
    fever_fact = Predicate('symptom', [Term('john'), Term('fever')])
    engine.retract(fever_fact)

    # Query john's diagnosis again
    solutions3 = engine.query(goal1)

    # John should no longer be diagnosed with flu
    assert len(solutions3) == 0


def test_assertz_rule():
    """Test assertz to add rules dynamically"""
    engine = LogicalEngine()

    # Add initial facts
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('bob')])))
    engine.add_fact(Fact(Predicate('parent', [Term('bob'), Term('ann')])))

    # Query for grandparent (should have no solutions - no grandparent rule)
    goal = Predicate('grandparent', [Term('tom'), Term('ann')])
    solutions1 = engine.query(goal)

    # Should have no solutions (no grandparent rule)
    assert len(solutions1) == 0

    # Add grandparent rule dynamically
    head = Predicate('grandparent', [Term('X', is_variable=True), Term('Z', is_variable=True)])
    body = [
        Predicate('parent', [Term('X', is_variable=True), Term('Y', is_variable=True)]),
        Predicate('parent', [Term('Y', is_variable=True), Term('Z', is_variable=True)])
    ]
    new_rule = Rule(head, body)
    engine.assertz(new_rule)

    # Query again
    solutions2 = engine.query(goal)

    # Should now have a solution
    assert len(solutions2) == 1

