"""
Tests for the Hybrid Interpreter
اختبارات المفسر الهجين
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bayan import HybridLexer, HybridParser, HybridInterpreter

def run_code(code):
    """Helper function to run code"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    return interpreter.interpret(ast)

def test_logical_fact():
    """Test adding logical facts"""
    code = """
hybrid {
    parent("john", "mary").
    parent("john", "tom").
}
"""
    result = run_code(code)
    print("✓ test_logical_fact passed")

def test_logical_query():
    """Test logical queries"""
    code = """
hybrid {
    parent("john", "mary").
    parent("john", "tom").
    query parent("john", ?X).
}
"""
    result = run_code(code)
    print("✓ test_logical_query passed")

def test_logical_rule():
    """Test logical rules"""
    code = """
hybrid {
    parent("john", "mary").
    parent("mary", "susan").
    grandparent(?X, ?Z) :- parent(?X, ?Y), parent(?Y, ?Z).
}
"""
    result = run_code(code)
    print("✓ test_logical_rule passed")

def test_hybrid_block_traditional():
    """Test hybrid block with traditional code"""
    code = """
hybrid {
    x = 10
    y = 20
    z = x + y
}
"""
    result = run_code(code)
    print("✓ test_hybrid_block_traditional passed")

def test_hybrid_block_mixed():
    """Test hybrid block with mixed code"""
    code = """
hybrid {
    x = 5
    parent("john", "mary").
    parent("john", "tom").
    y = x + 10
}
"""
    result = run_code(code)
    print("✓ test_hybrid_block_mixed passed")

def test_family_relations():
    """Test family relations example"""
    code = """
hybrid {
    parent("خالد", "أحمد").
    parent("فاطمة", "أحمد").
    parent("أحمد", "محمد").
    parent("أحمد", "سارة").
    
    grandparent(?X, ?Z) :- parent(?X, ?Y), parent(?Y, ?Z).
    sibling(?X, ?Y) :- parent(?P, ?X), parent(?P, ?Y).
}
"""
    result = run_code(code)
    print("✓ test_family_relations passed")

def test_multiple_facts():
    """Test multiple facts"""
    code = """
hybrid {
    color("red").
    color("blue").
    color("green").
    color("yellow").
}
"""
    result = run_code(code)
    print("✓ test_multiple_facts passed")

def test_complex_predicates():
    """Test complex predicates"""
    code = """
hybrid {
    person("john", 30, "engineer").
    person("mary", 28, "doctor").
    person("tom", 35, "teacher").
}
"""
    result = run_code(code)
    print("✓ test_complex_predicates passed")

def test_nested_hybrid_structures():
    """Test nested structures in hybrid block"""
    code = """
hybrid {
    people = ["john", "mary", "tom"]
    parent("john", "mary").
    parent("john", "tom").
    
    for person in people:
    {
        print(person)
    }
}
"""
    result = run_code(code)
    print("✓ test_nested_hybrid_structures passed")

def test_arabic_identifiers_hybrid():
    """Test Arabic identifiers in hybrid block"""
    code = """
hybrid {
    الاسم = "محمد"
    العمر = 25
    والد("محمد", "أحمد").
    والد("أحمد", "علي").
}
"""
    result = run_code(code)
    print("✓ test_arabic_identifiers_hybrid passed")

def test_function_in_hybrid():
    """Test function definition in hybrid block"""
    code = """
hybrid {
    def greet(name):
    {
        print("Hello, " + name)
    }
    
    greet("Bayan")
}
"""
    result = run_code(code)
    print("✓ test_function_in_hybrid passed")

def test_if_with_logical_condition():
    """Test if statement with logical condition"""
    code = """
hybrid {
    parent("john", "mary").
    
    if parent("john", ?X):
    {
        print("John has a child")
    }
}
"""
    result = run_code(code)
    print("✓ test_if_with_logical_condition passed")

if __name__ == "__main__":
    test_logical_fact()
    test_logical_query()
    test_logical_rule()
    test_hybrid_block_traditional()
    test_hybrid_block_mixed()
    test_family_relations()
    test_multiple_facts()
    test_complex_predicates()
    test_nested_hybrid_structures()
    test_arabic_identifiers_hybrid()
    test_function_in_hybrid()
    test_if_with_logical_condition()
    print("\n✓ All hybrid interpreter tests passed!")

