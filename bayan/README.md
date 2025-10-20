# Bayan Language - لغة بيان

A hybrid programming language combining traditional imperative programming with logical programming.

لغة برمجية هجينة تجمع بين البرمجة الإجرائية التقليدية والبرمجة المنطقية

## Features - الميزات

### Traditional Programming - البرمجة التقليدية
- Variables and assignments
- Arithmetic and logical operations
- Control flow (if/else, for, while)
- Functions and classes
- Lists and dictionaries
- String operations

### Logical Programming - البرمجة المنطقية
- Facts and rules
- Queries and unification
- Backtracking
- Pattern matching
- Logical inference

### Hybrid Features - الميزات الهجينة
- Combine traditional and logical code
- Use logical queries in traditional code
- Use traditional functions in logical rules
- Arabic language support

## Installation - التثبيت

```bash
cd bayan
python main.py
```

## Usage - الاستخدام

### Running a file
```bash
python main.py examples/family.by
```

### Interactive mode
```bash
python main.py
```

## Examples - أمثلة

### Simple Assignment
```bayan
x = 10
y = 20
z = x + y
print(z)
```

### Logical Facts and Rules
```bayan
hybrid {
    parent("john", "mary").
    parent("mary", "susan").
    
    grandparent(?X, ?Z) :- parent(?X, ?Y), parent(?Y, ?Z).
    
    query grandparent("john", ?X).
}
```

### Hybrid Block
```bayan
hybrid {
    # Traditional code
    people = ["john", "mary", "tom"]
    
    # Logical facts
    person("john", 30).
    person("mary", 28).
    person("tom", 35).
    
    # Mixed code
    for name in people:
    {
        print(name)
    }
}
```

## Language Syntax - بناء الجملة

### Traditional Statements
- `x = value` - Assignment
- `if condition: { ... }` - If statement
- `for var in iterable: { ... }` - For loop
- `while condition: { ... }` - While loop
- `def func(params): { ... }` - Function definition
- `class Name: { ... }` - Class definition
- `print(value)` - Print statement
- `return value` - Return statement

### Logical Statements
- `predicate(arg1, arg2).` - Fact
- `head :- body.` - Rule
- `query goal.` - Query
- `?X, ?Y` - Variables
- `,` - Conjunction (AND)
- `;` - Disjunction (OR)

### Hybrid Blocks
- `hybrid { ... }` - Hybrid block containing both traditional and logical code

## Data Types - أنواع البيانات

- Numbers: `42`, `3.14`
- Strings: `"hello"`, `'world'`
- Booleans: `True`, `False`
- Lists: `[1, 2, 3]`
- Dictionaries: `{key: value}`
- Logical variables: `?X`, `?Name`

## Built-in Functions - الدوال المدمجة

### List Functions
- `len(list)` - Get length
- `range(n)` - Create range
- `list(iterable)` - Convert to list

### String Functions
- `str(value)` - Convert to string
- `upper(string)` - Uppercase
- `lower(string)` - Lowercase
- `split(string, delimiter)` - Split string

### Type Functions
- `type(value)` - Get type
- `int(value)` - Convert to integer
- `float(value)` - Convert to float

## Project Structure - هيكل المشروع

```
bayan/
├── bayan/
│   ├── __init__.py
│   ├── lexer.py              # Tokenizer
│   ├── parser.py             # Parser
│   ├── ast_nodes.py          # AST definitions
│   ├── logical_engine.py     # Logical inference engine
│   ├── traditional_interpreter.py  # Traditional interpreter
│   ├── hybrid_interpreter.py       # Hybrid interpreter
│   └── builtins.py           # Built-in functions
├── main.py                   # Entry point
├── examples/                 # Example programs
│   ├── family.by
│   └── calculator.by
├── tests/                    # Test suite
│   ├── test_lexer.py
│   ├── test_logical_engine.py
│   ├── test_traditional_interpreter.py
│   └── test_hybrid_interpreter.py
└── README.md
```

## Running Tests - تشغيل الاختبارات

```bash
python tests/test_lexer.py
python tests/test_logical_engine.py
python tests/test_traditional_interpreter.py
python tests/test_hybrid_interpreter.py
```

## Version - الإصدار

Version 0.1.0 - Initial Release

## Author - المؤلف

Bayan Development Team

## License - الترخيص

MIT License

