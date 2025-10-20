"""
Tests for the Traditional Interpreter
اختبارات المفسر التقليدي
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

def test_basic_assignment():
    """Test basic variable assignment"""
    code = "x = 5"
    result = run_code(code)
    print("✓ test_basic_assignment passed")

def test_arithmetic():
    """Test arithmetic operations"""
    code = """
x = 10
y = 5
z = x + y
"""
    result = run_code(code)
    print("✓ test_arithmetic passed")

def test_string_operations():
    """Test string operations"""
    code = """
s = "hello"
t = "world"
"""
    result = run_code(code)
    print("✓ test_string_operations passed")

def test_list_operations():
    """Test list operations"""
    code = """
lst = [1, 2, 3, 4, 5]
"""
    result = run_code(code)
    print("✓ test_list_operations passed")

def test_dict_operations():
    """Test dictionary operations"""
    code = """
d = {1: "one", 2: "two", 3: "three"}
"""
    result = run_code(code)
    print("✓ test_dict_operations passed")

def test_if_statement():
    """Test if statement"""
    code = """
x = 10
if x > 5:
{
    y = 1
}
"""
    result = run_code(code)
    print("✓ test_if_statement passed")

def test_for_loop():
    """Test for loop"""
    code = """
sum = 0
for i in [1, 2, 3, 4, 5]:
{
    sum = sum + i
}
"""
    result = run_code(code)
    print("✓ test_for_loop passed")

def test_while_loop():
    """Test while loop"""
    code = """
x = 0
while x < 5:
{
    x = x + 1
}
"""
    result = run_code(code)
    print("✓ test_while_loop passed")

def test_function_definition():
    """Test function definition"""
    code = """
def add(a, b):
{
    return a + b
}
"""
    result = run_code(code)
    print("✓ test_function_definition passed")

def test_function_call():
    """Test function call"""
    code = """
def multiply(a, b):
{
    return a * b
}
result = multiply(3, 4)
"""
    result = run_code(code)
    print("✓ test_function_call passed")

def test_boolean_operations():
    """Test boolean operations"""
    code = """
x = True
y = False
z = x and y
w = x or y
"""
    result = run_code(code)
    print("✓ test_boolean_operations passed")

def test_comparison_operations():
    """Test comparison operations"""
    code = """
x = 10
y = 5
a = x == y
b = x != y
c = x > y
d = x < y
e = x >= y
f = x <= y
"""
    result = run_code(code)
    print("✓ test_comparison_operations passed")

def test_nested_structures():
    """Test nested structures"""
    code = """
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
"""
    result = run_code(code)
    print("✓ test_nested_structures passed")

def test_print_statement():
    """Test print statement"""
    code = """
print("Hello, Bayan!")
"""
    result = run_code(code)
    print("✓ test_print_statement passed")

if __name__ == "__main__":
    test_basic_assignment()
    test_arithmetic()
    test_string_operations()
    test_list_operations()
    test_dict_operations()
    test_if_statement()
    test_for_loop()
    test_while_loop()
    test_function_definition()
    test_function_call()
    test_boolean_operations()
    test_comparison_operations()
    test_nested_structures()
    test_print_statement()
    print("\n✓ All traditional interpreter tests passed!")

