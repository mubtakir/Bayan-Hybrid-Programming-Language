"""
Tests for bagof/setof meta-predicates
اختبارات لـ bagof/setof
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bayan'))

import pytest
from bayan.logical_engine import LogicalEngine, Fact, Rule, Predicate, Term


def test_bagof_basic():
    """Test bagof to collect all solutions"""
    engine = LogicalEngine()
    
    # Add facts
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('bob')])))
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('liz')])))
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('ann')])))
    
    # Query using bagof
    goal = Predicate('bagof', [
        Term('X', is_variable=True),
        Predicate('parent', [Term('tom'), Term('X', is_variable=True)]),
        Term('List', is_variable=True)
    ])
    solutions = engine.query(goal)
    
    # Should have 1 solution with a list of 3 children
    assert len(solutions) == 1
    result_list = solutions[0].bindings['List']
    assert len(result_list) == 3
    assert 'bob' in result_list
    assert 'liz' in result_list
    assert 'ann' in result_list


def test_bagof_fails_on_no_solutions():
    """Test that bagof fails when there are no solutions"""
    engine = LogicalEngine()
    
    # Add facts
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('bob')])))
    
    # Query for non-existent parent
    goal = Predicate('bagof', [
        Term('X', is_variable=True),
        Predicate('parent', [Term('john'), Term('X', is_variable=True)]),
        Term('List', is_variable=True)
    ])
    solutions = engine.query(goal)
    
    # Should have no solutions (bagof fails on empty result)
    assert len(solutions) == 0


def test_setof_basic():
    """Test setof to collect unique sorted solutions"""
    engine = LogicalEngine()
    
    # Add facts with duplicates
    engine.add_fact(Fact(Predicate('likes', [Term('john'), Term('pizza')])))
    engine.add_fact(Fact(Predicate('likes', [Term('mary'), Term('pizza')])))
    engine.add_fact(Fact(Predicate('likes', [Term('bob'), Term('pizza')])))
    engine.add_fact(Fact(Predicate('likes', [Term('john'), Term('pasta')])))
    
    # Query using setof to get all people who like pizza
    goal = Predicate('setof', [
        Term('X', is_variable=True),
        Predicate('likes', [Term('X', is_variable=True), Term('pizza')]),
        Term('List', is_variable=True)
    ])
    solutions = engine.query(goal)
    
    # Should have 1 solution with a sorted list of 3 people
    assert len(solutions) == 1
    result_list = solutions[0].bindings['List']
    assert len(result_list) == 3
    # Should be sorted
    assert result_list == ['bob', 'john', 'mary']


def test_setof_removes_duplicates():
    """Test that setof removes duplicate solutions"""
    engine = LogicalEngine()
    
    # Add facts that will produce duplicate solutions
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('bob')])))
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('liz')])))
    engine.add_fact(Fact(Predicate('grandparent', [Term('tom'), Term('ann')])))
    
    # Add a rule that might produce duplicates
    head = Predicate('ancestor', [Term('X', is_variable=True), Term('Y', is_variable=True)])
    body = [Predicate('parent', [Term('X', is_variable=True), Term('Y', is_variable=True)])]
    engine.add_rule(Rule(head, body))
    
    # Query using setof
    goal = Predicate('setof', [
        Term('Y', is_variable=True),
        Predicate('ancestor', [Term('tom'), Term('Y', is_variable=True)]),
        Term('List', is_variable=True)
    ])
    solutions = engine.query(goal)
    
    # Should have 1 solution with unique sorted children
    assert len(solutions) == 1
    result_list = solutions[0].bindings['List']
    assert len(result_list) == 2
    assert result_list == ['bob', 'liz']


def test_setof_fails_on_no_solutions():
    """Test that setof fails when there are no solutions"""
    engine = LogicalEngine()
    
    # Add facts
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('bob')])))
    
    # Query for non-existent parent
    goal = Predicate('setof', [
        Term('X', is_variable=True),
        Predicate('parent', [Term('john'), Term('X', is_variable=True)]),
        Term('List', is_variable=True)
    ])
    solutions = engine.query(goal)
    
    # Should have no solutions (setof fails on empty result)
    assert len(solutions) == 0


def test_bagof_vs_findall():
    """Test difference between bagof and findall"""
    engine = LogicalEngine()
    
    # Add facts
    engine.add_fact(Fact(Predicate('parent', [Term('tom'), Term('bob')])))
    
    # Query for non-existent parent using findall
    goal_findall = Predicate('findall', [
        Term('X', is_variable=True),
        Predicate('parent', [Term('john'), Term('X', is_variable=True)]),
        Term('List', is_variable=True)
    ])
    solutions_findall = engine.query(goal_findall)
    
    # findall should succeed with empty list
    assert len(solutions_findall) == 1
    assert solutions_findall[0].bindings['List'] == []
    
    # Query for non-existent parent using bagof
    goal_bagof = Predicate('bagof', [
        Term('X', is_variable=True),
        Predicate('parent', [Term('john'), Term('X', is_variable=True)]),
        Term('List', is_variable=True)
    ])
    solutions_bagof = engine.query(goal_bagof)
    
    # bagof should fail (no solutions)
    assert len(solutions_bagof) == 0


def test_setof_for_data_analysis():
    """Test setof for data analysis use case"""
    engine = LogicalEngine()
    
    # Add facts about students and their grades
    engine.add_fact(Fact(Predicate('grade', [Term('john'), Term('math'), Term(90)])))
    engine.add_fact(Fact(Predicate('grade', [Term('mary'), Term('math'), Term(85)])))
    engine.add_fact(Fact(Predicate('grade', [Term('bob'), Term('math'), Term(78)])))
    engine.add_fact(Fact(Predicate('grade', [Term('john'), Term('physics'), Term(88)])))
    engine.add_fact(Fact(Predicate('grade', [Term('mary'), Term('physics'), Term(92)])))
    
    # Get all students who took math (sorted)
    goal = Predicate('setof', [
        Term('Student', is_variable=True),
        Predicate('grade', [Term('Student', is_variable=True), Term('math'), Term('G', is_variable=True)]),
        Term('Students', is_variable=True)
    ])
    solutions = engine.query(goal)
    
    # Should have 1 solution with sorted list of students
    assert len(solutions) == 1
    students = solutions[0].bindings['Students']
    assert students == ['bob', 'john', 'mary']


def test_bagof_for_ml_feature_collection():
    """Test bagof for collecting ML features"""
    engine = LogicalEngine()
    
    # Add facts about features
    engine.add_fact(Fact(Predicate('feature', [Term('sample1'), Term('age'), Term(25)])))
    engine.add_fact(Fact(Predicate('feature', [Term('sample1'), Term('height'), Term(175)])))
    engine.add_fact(Fact(Predicate('feature', [Term('sample1'), Term('weight'), Term(70)])))
    
    # Collect all feature values for sample1
    goal = Predicate('bagof', [
        Term('Value', is_variable=True),
        Predicate('feature', [Term('sample1'), Term('F', is_variable=True), Term('Value', is_variable=True)]),
        Term('Features', is_variable=True)
    ])
    solutions = engine.query(goal)
    
    # Should have 1 solution with all feature values
    assert len(solutions) == 1
    features = solutions[0].bindings['Features']
    assert len(features) == 3
    assert 25 in features
    assert 175 in features
    assert 70 in features

