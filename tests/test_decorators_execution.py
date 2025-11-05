#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Decorator execution in Bayan language
اختبارات لتنفيذ المزخرفات في لغة البيان
"""

import sys
sys.path.insert(0, 'bayan')

from bayan.lexer import HybridLexer
from bayan.parser import HybridParser
from bayan.traditional_interpreter import TraditionalInterpreter

def test_simple_decorator():
    """Test simple decorator without arguments"""
    code = """
def uppercase_decorator(func): {
    def wrapper(): {
        result = func()
        if isinstance(result, str): {
            return result.upper()
        }
        return result
    }
    return wrapper
}

@uppercase_decorator
def greet(): {
    return "hello"
}

x = greet()
    """
    
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    interpreter = TraditionalInterpreter()
    interpreter.interpret(ast)
    
    # Check that the decorated function returns uppercase
    result = interpreter.global_env.get('x')
    assert result == "HELLO", f"Expected 'HELLO', got {result}"
    print("✅ Simple decorator test passed")

def test_decorator_with_arguments():
    """Test decorator with arguments"""
    code = """
def repeat(times): {
    def decorator(func): {
        def wrapper(): {
            result = ""
            for i in range(times): {
                result = result + func()
            }
            return result
        }
        return wrapper
    }
    return decorator
}

@repeat(3)
def say_hi(): {
    return "Hi"
}

x = say_hi()
    """
    
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    interpreter = TraditionalInterpreter()
    interpreter.interpret(ast)
    
    # Check that the function is called 3 times
    result = interpreter.global_env.get('x')
    assert result == "HiHiHi", f"Expected 'HiHiHi', got {result}"
    print("✅ Decorator with arguments test passed")

def test_multiple_decorators():
    """Test multiple decorators stacked"""
    code = """
def add_prefix(func): {
    def wrapper(): {
        return "PREFIX_" + func()
    }
    return wrapper
}

def add_suffix(func): {
    def wrapper(): {
        return func() + "_SUFFIX"
    }
    return wrapper
}

@add_prefix
@add_suffix
def get_text(): {
    return "MIDDLE"
}

x = get_text()
    """
    
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    interpreter = TraditionalInterpreter()
    interpreter.interpret(ast)
    
    # Decorators are applied bottom to top: add_suffix first, then add_prefix
    result = interpreter.global_env.get('x')
    assert result == "PREFIX_MIDDLE_SUFFIX", f"Expected 'PREFIX_MIDDLE_SUFFIX', got {result}"
    print("✅ Multiple decorators test passed")

def test_decorator_with_function_args():
    """Test decorator on function with arguments"""
    code = """
def double_result(func): {
    def wrapper(x): {
        return func(x) * 2
    }
    return wrapper
}

@double_result
def square(n): {
    return n * n
}

x = square(5)
    """
    
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    interpreter = TraditionalInterpreter()
    interpreter.interpret(ast)
    
    # square(5) = 25, doubled = 50
    result = interpreter.global_env.get('x')
    assert result == 50, f"Expected 50, got {result}"
    print("✅ Decorator with function arguments test passed")

def test_decorator_preserves_function():
    """Test that decorator preserves original function behavior"""
    code = """
def log_call(func): {
    def wrapper(x): {
        # In a real scenario, this would log
        return func(x)
    }
    return wrapper
}

@log_call
def add_ten(n): {
    return n + 10
}

x = add_ten(5)
    """
    
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    interpreter = TraditionalInterpreter()
    interpreter.interpret(ast)
    
    result = interpreter.global_env.get('x')
    assert result == 15, f"Expected 15, got {result}"
    print("✅ Decorator preserves function test passed")

if __name__ == "__main__":
    print("Testing Decorator Execution")
    print("=" * 60)
    
    test_simple_decorator()
    test_decorator_with_arguments()
    test_multiple_decorators()
    test_decorator_with_function_args()
    test_decorator_preserves_function()
    
    print("=" * 60)
    print("✅ All Decorator execution tests passed!")

