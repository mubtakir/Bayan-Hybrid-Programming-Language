#!/usr/bin/env python3
"""
Generic runner for Bayan .bayan files.
Usage:
  python3 scripts/bayan_run.py path/to/file.bayan [--colors] [--tabstop=4] [--context=1]
"""
import os
import sys
import argparse

# Ensure the Bayan package is on sys.path. This script lives in <repo>/scripts.
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
BAYAN_PKG_PARENT = os.path.join(REPO_DIR, '...')  # placeholder to compute below
# We expect the Bayan package at <repo>/bayan (package root), import path 'bayan.lexer'
BAYAN_PKG_DIR = os.path.normpath(os.path.join(REPO_DIR, '..', 'bayan'))
if BAYAN_PKG_DIR not in sys.path:
    sys.path.insert(0, BAYAN_PKG_DIR)

from bayan.lexer import HybridLexer
from bayan.parser import HybridParser
from bayan.hybrid_interpreter import HybridInterpreter


def main():
    ap = argparse.ArgumentParser(description='Run Bayan source files (.bayan)')
    ap.add_argument('path', help='Path to .bayan file')
    ap.add_argument('--colors', action='store_true', help='Enable ANSI colors in error frames')
    ap.add_argument('--context', type=int, default=1, help='Context lines around errors (default: 1)')
    ap.add_argument('--tabstop', type=int, default=4, help='Tab width for caret alignment (default: 4)')
    args = ap.parse_args()

    src_path = os.path.abspath(args.path)
    with open(src_path, 'r', encoding='utf-8') as f:
        code = f.read()

    lexer = HybridLexer(code)
    toks = lexer.tokenize()
    parser = HybridParser(toks, filename=args.path)
    ast = parser.parse()

    intr = HybridInterpreter()
    intr.traditional.set_source(code, filename=args.path)
    intr.traditional.set_error_formatting(colors=args.colors, context_lines=args.context, tabstop=args.tabstop)

    try:
        intr.interpret(ast)
    except Exception as e:
        # Let stacktraces surface; Bayan should format runtime errors itself
        raise


if __name__ == '__main__':
    main()

