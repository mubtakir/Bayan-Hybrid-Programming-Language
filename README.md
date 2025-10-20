# Bayan — Hybrid Programming Language (لغة بيان)
Basil Yahya Abdullah
Bayan is a hybrid language that combines traditional imperative/OOP programming with a Prolog-like logical layer, all in one source. It supports Arabic and Latin identifiers, Python interop, multiple inheritance with C3 MRO, and advanced error reporting with code frames and optional colors.

- Language: Arabic-friendly identifiers `[a-zA-Z_\u0600-\u06FF][a-zA-Z0-9_\u0600-\u06FF]*`
- Paradigms: Imperative, OOP, and Logic (facts/rules/queries)
- OOP: classes, objects, methods, multiple inheritance (C3 MRO), `super()`
- Interop: Native Bayan modules + safe Python imports
- Errors: Bayan stack traces + numbered code frames, Unicode-aware caret, ANSI colors (optional)

## Getting Started

### Prerequisites
- Python 3.10+
- Git

### Clone & (optional) venv
```bash
git clone https://github.com/mubtakir/Bayan-Hybrid-Programming-Language.git
cd Bayan-Hybrid-Programming-Language
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
```

### Run tests
```bash
cd bayan
pytest -q
```

### Running Bayan code (embedded from Python)
Use the embedded API (see docs/cookbook.md) to execute Bayan snippets from Python:
```python
from bayan.lexer import Lexer
from bayan.parser import HybridParser
from bayan.hybrid_interpreter import HybridInterpreter

code = """
print("Hello, Bayan!")
"""

toks = Lexer(code).tokenize()
ast = HybridParser(toks, filename="<mem>").parse()
intr = HybridInterpreter()
intr.traditional.set_source(code, filename="<mem>")
intr.interpret(ast)
```

## Documentation
- Basics guide: docs/basics.md
- Language reference: docs/reference.md
- Developer guide: docs/developer_guide.md
- Architecture (with Mermaid diagrams): docs/architecture.md
- Cookbook (copy-paste examples): docs/cookbook.md
- Contributing: CONTRIBUTING.md

## Error reporting — code frames & colors
Configure error formatting:
```python
intr.traditional.set_error_formatting(colors=True, context_lines=1, tabstop=4)
```
You’ll see a file header, numbered code lines, and a caret (^) aligned correctly even with tabs/wide characters. The current line can be highlighted when colors are enabled.

## Roadmap (high-level)
- Optional default/named parameters for functions
- Expanded string escapes and multi-line strings
- First-class exceptions (raise/try/except)
- Richer Python interop (typed bridges)
- CLI runner and interactive REPL

## Contributing
See CONTRIBUTING.md — please run tests locally (`pytest -q`) and update docs for user-visible changes.

