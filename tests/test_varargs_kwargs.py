"""
Tests for *args and **kwargs support
اختبارات لدعم *args و **kwargs
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bayan'))

import pytest
from bayan import HybridLexer, HybridParser, HybridInterpreter


def test_varargs_basic():
    """Test basic *args functionality"""
    code = """
    def sum_all(*numbers):
    {
        total = 0
        for num in numbers:
        {
            total = total + num
        }
        return total
    }

    result1 = sum_all(1, 2, 3)
    result2 = sum_all(1, 2, 3, 4, 5)
    result3 = sum_all()
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['result1'] == 6
    assert interpreter.traditional.global_env['result2'] == 15
    assert interpreter.traditional.global_env['result3'] == 0


def test_varargs_with_regular_params():
    """Test *args with regular parameters"""
    code = """
    def greet(greeting, *names):
    {
        result = greeting + ": "
        for name in names:
        {
            result = result + name + " "
        }
        return result
    }
    
    result = greet("Hello", "Alice", "Bob", "Charlie")
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['result'] == "Hello: Alice Bob Charlie "


def test_kwargs_basic():
    """Test basic **kwargs functionality"""
    code = """
    def print_info(**info):
    {
        result = ""
        for key in info:
        {
            result = result + key + "=" + str(info[key]) + " "
        }
        return result
    }
    
    result = print_info(name="Alice", age=30, city="NYC")
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    # Note: dict iteration order is preserved in Python 3.7+
    result = interpreter.traditional.global_env['result']
    assert "name=Alice" in result
    assert "age=30" in result
    assert "city=NYC" in result


def test_varargs_and_kwargs():
    """Test *args and **kwargs together"""
    code = """
    def flexible_func(required, *args, **kwargs):
    {
        result = str(required) + "|"
        
        for arg in args:
        {
            result = result + str(arg) + ","
        }
        
        result = result + "|"
        
        for key in kwargs:
        {
            result = result + key + "=" + str(kwargs[key]) + ","
        }
        
        return result
    }
    
    result = flexible_func(1, 2, 3, x=10, y=20)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    result = interpreter.traditional.global_env['result']
    assert result.startswith("1|2,3,|")
    assert "x=10" in result
    assert "y=20" in result


def test_varargs_with_defaults():
    """Test *args with default parameters"""
    code = """
    def func(a, b=10, *args):
    {
        total = a + b
        for arg in args:
        {
            total = total + arg
        }
        return total
    }
    
    result1 = func(1)
    result2 = func(1, 2)
    result3 = func(1, 2, 3, 4)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['result1'] == 11  # 1 + 10
    assert interpreter.traditional.global_env['result2'] == 3   # 1 + 2
    assert interpreter.traditional.global_env['result3'] == 10  # 1 + 2 + 3 + 4


def test_neural_network_layer_example():
    """Test realistic AI/ML example: neural network layer with flexible inputs"""
    code = """
    def create_layer(input_size, output_size, *hidden_sizes, **options):
    {
        # Simulate creating a neural network layer
        layer_info = {
            "input": input_size,
            "output": output_size,
            "hidden": hidden_sizes,
            "activation": "relu",
            "dropout": 0.0
        }
        
        # Override with options
        for key in options:
        {
            layer_info[key] = options[key]
        }
        
        return layer_info
    }
    
    # Create a simple layer
    layer1 = create_layer(784, 10)
    
    # Create a layer with hidden layers
    layer2 = create_layer(784, 10, 128, 64)
    
    # Create a layer with custom options
    layer3 = create_layer(784, 10, 128, activation="sigmoid", dropout=0.5)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    layer1 = interpreter.traditional.global_env['layer1']
    assert layer1['input'] == 784
    assert layer1['output'] == 10
    assert layer1['hidden'] == []
    assert layer1['activation'] == "relu"
    
    layer2 = interpreter.traditional.global_env['layer2']
    assert layer2['hidden'] == [128, 64]
    
    layer3 = interpreter.traditional.global_env['layer3']
    assert layer3['activation'] == "sigmoid"
    assert layer3['dropout'] == 0.5


def test_varargs_empty():
    """Test *args with no extra arguments"""
    code = """
    def func(a, *args):
    {
        return len(args)
    }
    
    result = func(1)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['result'] == 0


def test_kwargs_empty():
    """Test **kwargs with no extra arguments"""
    code = """
    def func(a, **kwargs):
    {
        return len(kwargs)
    }
    
    result = func(1)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['result'] == 0


def test_varargs_in_class_method():
    """Test *args in class methods"""
    code = """
    class Calculator:
    {
        def sum(self, *numbers):
        {
            total = 0
            for num in numbers:
            {
                total = total + num
            }
            return total
        }
    }
    
    calc = Calculator()
    result = calc.sum(1, 2, 3, 4, 5)
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['result'] == 15

