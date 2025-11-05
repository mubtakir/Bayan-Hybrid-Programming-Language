#!/usr/bin/env python3
"""
Bayan Language - Main Entry Point
لغة بيان - نقطة الدخول الرئيسية
"""

import sys
import os

# Add the bayan package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bayan import run_code, HybridLexer, HybridParser, HybridInterpreter

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Bayan Language Interpreter")
        print("لغة بيان - مفسر اللغة")
        print()
        print("Usage: python main.py <file.by>")
        print("الاستخدام: python main.py <file.by>")
        print()
        print("Or run in interactive mode:")
        print("أو قم بالتشغيل في الوضع التفاعلي:")
        interactive_mode()
    else:
        file_path = sys.argv[1]
        run_file(file_path)

def run_file(file_path):
    """Run a Bayan file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        result = run_code(code)
        if result is not None:
            print(result)
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def interactive_mode():
    """Run in interactive mode"""
    print("Bayan Interactive Mode")
    print("اكتب 'exit' للخروج")
    print()
    
    interpreter = HybridInterpreter()
    
    while True:
        try:
            code = input(">>> ")
            
            if code.lower() == 'exit':
                break
            
            if not code.strip():
                continue
            
            lexer = HybridLexer(code)
            tokens = lexer.tokenize()
            
            parser = HybridParser(tokens)
            ast = parser.parse()
            
            result = interpreter.interpret(ast)
            
            if result is not None:
                print(result)
        
        except KeyboardInterrupt:
            print("\nInterrupted")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

