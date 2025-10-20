"""
Bayan Language - لغة بيان
A hybrid programming language combining traditional imperative programming with logical programming.
لغة برمجية هجينة تجمع بين البرمجة الإجرائية التقليدية والبرمجة المنطقية

Version: 0.1.0
Author: Bayan Development Team
"""

__version__ = "0.1.0"
__author__ = "Bayan Development Team"

from .lexer import HybridLexer, Token, TokenType
from .ast_nodes import *
from .parser import HybridParser
from .logical_engine import LogicalEngine, Fact, Rule, Predicate, Term
from .traditional_interpreter import TraditionalInterpreter
from .hybrid_interpreter import HybridInterpreter
from .object_system import BayanObject, ClassSystem
from .import_system import ImportSystem

__all__ = [
    'HybridLexer',
    'Token',
    'TokenType',
    'HybridParser',
    'LogicalEngine',
    'Fact',
    'Rule',
    'Predicate',
    'Term',
    'TraditionalInterpreter',
    'HybridInterpreter',
    'BayanObject',
    'ClassSystem',
    'ImportSystem',
]

def run_code(code):
    """
    Run Bayan code
    تشغيل كود بيان
    """
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    
    parser = HybridParser(tokens)
    ast = parser.parse()
    
    interpreter = HybridInterpreter()
    result = interpreter.interpret(ast)
    
    return result

