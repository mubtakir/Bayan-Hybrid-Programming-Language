#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Execution tests for async/await functionality in Bayan language
اختبارات تنفيذ async/await في لغة البيان
"""

import sys
sys.path.insert(0, 'bayan')

from bayan.lexer import HybridLexer
from bayan.parser import HybridParser
from bayan.hybrid_interpreter import HybridInterpreter

def test_simple_async_function_execution():
    """Test executing a simple async function that returns a value"""
    code = """
async def fetch(): {
    return 42
}

result = await fetch()
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)

    result = interpreter.traditional.global_env.get('result')
    assert result == 42, f"Expected 42, got {result}"
    print("✅ Simple async function execution works")

def test_async_function_with_parameters():
    """Test async function with parameters"""
    code = """
async def add(a, b): {
    return a + b
}

result = await add(10, 20)
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)

    result = interpreter.traditional.global_env.get('result')
    assert result == 30, f"Expected 30, got {result}"
    print("✅ Async function with parameters works")

def test_async_function_with_computation():
    """Test async function with computation"""
    code = """
async def compute(n): {
    total = 0
    i = 1
    while i <= n: {
        total = total + i
        i = i + 1
    }
    return total
}

result = await compute(5)
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    interpreter = HybridInterpreter()
    interpreter.interpret(ast)

    result = interpreter.traditional.global_env.get('result')
    assert result == 15, f"Expected 15 (1+2+3+4+5), got {result}"
    print("✅ Async function with computation works")

def test_multiple_async_calls():
    """Test multiple async function calls"""
    code = """
async def get_value(x): {
    return x * 2
}

a = await get_value(5)
b = await get_value(10)
c = await get_value(15)
total = a + b + c
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    interpreter = HybridInterpreter()
    interpreter.interpret(ast)

    a = interpreter.traditional.global_env.get('a')
    b = interpreter.traditional.global_env.get('b')
    c = interpreter.traditional.global_env.get('c')
    total = interpreter.traditional.global_env.get('total')
    
    assert a == 10, f"Expected a=10, got {a}"
    assert b == 20, f"Expected b=20, got {b}"
    assert c == 30, f"Expected c=30, got {c}"
    assert total == 60, f"Expected total=60, got {total}"
    print("✅ Multiple async calls work")

def test_async_calling_async():
    """Test async function calling another async function"""
    code = """
async def fetch_data(): {
    return 100
}

async def process_data(): {
    data = await fetch_data()
    return data * 2
}

result = await process_data()
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)

    result = interpreter.traditional.global_env.get('result')
    assert result == 200, f"Expected 200, got {result}"
    print("✅ Async calling async works")

def test_async_with_if_statement():
    """Test async function with if statement"""
    code = """
async def check_value(x): {
    if x > 10: {
        return "large"
    } else: {
        return "small"
    }
}

result1 = await check_value(15)
result2 = await check_value(5)
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    interpreter = HybridInterpreter()
    interpreter.interpret(ast)

    result1 = interpreter.traditional.global_env.get('result1')
    result2 = interpreter.traditional.global_env.get('result2')

    assert result1 == "large", f"Expected 'large', got {result1}"
    assert result2 == "small", f"Expected 'small', got {result2}"
    print("✅ Async with if statement works")

def test_async_with_for_loop():
    """Test async function with for loop"""
    code = """
async def sum_list(items): {
    total = 0
    for item in items: {
        total = total + item
    }
    return total
}

result = await sum_list([1, 2, 3, 4, 5])
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    interpreter = HybridInterpreter()
    interpreter.interpret(ast)

    result = interpreter.traditional.global_env.get('result')
    assert result == 15, f"Expected 15, got {result}"
    print("✅ Async with for loop works")

def test_async_with_try_except():
    """Test async function with try/except"""
    code = """
async def safe_divide(a, b): {
    try: {
        return a / b
    } except: {
        return -1
    }
}

result1 = await safe_divide(10, 2)
result2 = await safe_divide(10, 0)
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)

    result1 = interpreter.traditional.global_env.get('result1')
    result2 = interpreter.traditional.global_env.get('result2')

    assert result1 == 5.0, f"Expected 5.0, got {result1}"
    assert result2 == -1, f"Expected -1, got {result2}"
    print("✅ Async with try/except works")

def test_async_with_default_parameters():
    """Test async function with default parameters"""
    code = """
async def greet(name, greeting="Hello"): {
    return greeting + " " + name
}

result1 = await greet("Alice")
result2 = await greet("Bob", "Hi")
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    interpreter = HybridInterpreter()
    interpreter.interpret(ast)

    result1 = interpreter.traditional.global_env.get('result1')
    result2 = interpreter.traditional.global_env.get('result2')

    assert result1 == "Hello Alice", f"Expected 'Hello Alice', got {result1}"
    assert result2 == "Hi Bob", f"Expected 'Hi Bob', got {result2}"
    print("✅ Async with default parameters works")

def test_async_with_named_arguments():
    """Test async function with named arguments"""
    code = """
async def create_user(name, age, city): {
    return name + " is " + str(age) + " years old from " + city
}

result = await create_user(city="Cairo", name="Ahmed", age=25)
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()

    interpreter = HybridInterpreter()
    interpreter.interpret(ast)

    result = interpreter.traditional.global_env.get('result')
    assert result == "Ahmed is 25 years old from Cairo", f"Expected 'Ahmed is 25 years old from Cairo', got {result}"
    print("✅ Async with named arguments works")

if __name__ == "__main__":
    print("Testing Async/Await Execution")
    print("=" * 50)
    
    test_simple_async_function_execution()
    test_async_function_with_parameters()
    test_async_function_with_computation()
    test_multiple_async_calls()
    test_async_calling_async()
    test_async_with_if_statement()
    test_async_with_for_loop()
    test_async_with_try_except()
    test_async_with_default_parameters()
    test_async_with_named_arguments()
    
    print("=" * 50)
    print("✅ All async/await execution tests passed!")

