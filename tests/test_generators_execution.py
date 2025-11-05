#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Execution tests for Generators in Bayan language
اختبارات تنفيذ للمولدات (Generators) في لغة البيان
"""

import sys
sys.path.insert(0, 'bayan')

from bayan.lexer import HybridLexer
from bayan.parser import HybridParser
from bayan.traditional_interpreter import TraditionalInterpreter


def run(code):
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interp = TraditionalInterpreter()
    interp.interpret(ast)
    return interp


def test_simple_generator_to_list():
    code = """
    def count(n): {
        i = 0
        while i < n: {
            yield i
            i = i + 1
        }
    }

    g = count(5)
    xs = list(g)
    """
    interp = run(code)
    assert interp.global_env.get('xs') == [0, 1, 2, 3, 4]


def test_generator_in_for_loop_sum():
    code = """
    def count(n): {
        i = 0
        while i < n: {
            yield i
            i = i + 1
        }
    }

    total = 0
    for x in count(5): {
        total = total + x
    }
    """
    interp = run(code)
    assert interp.global_env.get('total') == 10


def test_fibonacci_generator_prefix():
    code = """
    def fib(k): {
        a = 0
        b = 1
        i = 0
        while i < k: {
            yield a
            temp = a + b
            a = b
            b = temp
            i = i + 1
        }
    }

    first = list(fib(7))
    """
    interp = run(code)
    assert interp.global_env.get('first') == [0, 1, 1, 2, 3, 5, 8]

