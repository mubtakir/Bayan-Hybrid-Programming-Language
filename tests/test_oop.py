"""
Tests for Object-Oriented Programming in Bayan Language
اختبارات البرمجة كائنية التوجه في لغة بيان
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bayan import HybridLexer, HybridParser, HybridInterpreter

def test_class_definition():
    """Test class definition"""
    code = """
    class Person:
    {
        def __init__(name):
        {
            self.name = name
        }
    }
    """
    
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    
    result = interpreter.interpret(ast)
    assert 'Person' in interpreter.traditional.classes

def test_object_instantiation():
    """Test object instantiation"""
    code = """
    class Person:
    {
        def __init__(name):
        {
            self.name = name
        }
    }
    
    person = Person("Ahmed")
    """
    
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    
    result = interpreter.interpret(ast)
    person = interpreter.traditional.global_env['person']
    assert person is not None
    assert person.get_attribute('name') == "Ahmed"

def test_method_call():
    """Test method call"""
    code = """
    class Calculator:
    {
        def add(a, b):
        {
            return a + b
        }
    }
    
    calc = Calculator()
    result = calc.add(5, 3)
    """
    
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    
    result = interpreter.interpret(ast)
    result_value = interpreter.traditional.global_env['result']
    assert result_value == 8

def test_attribute_access():
    """Test attribute access"""
    code = """
    class Person:
    {
        def __init__(name, age):
        {
            self.name = name
            self.age = age
        }
    }
    
    person = Person("Ali", 30)
    name = person.name
    age = person.age
    """
    
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    
    result = interpreter.interpret(ast)
    name = interpreter.traditional.global_env['name']
    age = interpreter.traditional.global_env['age']
    assert name == "Ali"
    assert age == 30

def test_multiple_objects():
    """Test multiple object instances"""
    code = """
    class Counter:
    {
        def __init__(start):
        {
            self.value = start
        }
        
        def increment():
        {
            self.value = self.value + 1
        }
    }
    
    c1 = Counter(0)
    c2 = Counter(10)
    c1.increment()
    """
    
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    
    result = interpreter.interpret(ast)
    c1 = interpreter.traditional.global_env['c1']
    c2 = interpreter.traditional.global_env['c2']
    assert c1.get_attribute('value') == 1
    assert c2.get_attribute('value') == 10

if __name__ == '__main__':
    test_class_definition()
    print("✓ test_class_definition passed")
    
    test_object_instantiation()
    print("✓ test_object_instantiation passed")
    
    test_method_call()
    print("✓ test_method_call passed")
    
    test_attribute_access()
    print("✓ test_attribute_access passed")
    
    test_multiple_objects()
    print("✓ test_multiple_objects passed")
    
    print("\n✅ All OOP tests passed!")


