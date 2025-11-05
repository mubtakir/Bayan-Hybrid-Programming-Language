# Contributing to Bayan - المساهمة في بيان

## Getting Started - البدء

1. Clone the repository
2. Install Python 3.7+
3. Run tests to verify setup

```bash
cd bayan
python tests/test_lexer.py
python tests/test_logical_engine.py
python tests/test_traditional_interpreter.py
python tests/test_hybrid_interpreter.py
```

## Development Workflow - سير العمل

1. Create a new branch for your feature
2. Make your changes
3. Write tests for new functionality
4. Run all tests to ensure nothing breaks
5. Submit a pull request

## Code Style - أسلوب الكود

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Add comments for complex logic
- Keep functions small and focused

## Testing - الاختبار

### Running Tests

```bash
# Run all tests
python tests/test_lexer.py
python tests/test_logical_engine.py
python tests/test_traditional_interpreter.py
python tests/test_hybrid_interpreter.py

# Run specific test
python tests/test_lexer.py
```

### Writing Tests

```python
def test_new_feature():
    """Test description"""
    # Setup
    code = "..."
    
    # Execute
    result = run_code(code)
    
    # Assert
    assert result == expected
    print("✓ test_new_feature passed")
```

## Adding New Features - إضافة ميزات جديدة

### Adding a New Keyword

1. Add token type to `lexer.py`
2. Add keyword to `KEYWORDS` dictionary
3. Add parsing logic to `parser.py`
4. Add AST node to `ast_nodes.py`
5. Add interpretation logic to appropriate interpreter
6. Add tests

### Adding a Built-in Function

1. Add function to `traditional_interpreter.py`
2. Add tests in `test_traditional_interpreter.py`
3. Update documentation

### Adding a Logical Predicate

1. Add predicate to `logical_engine.py`
2. Add tests in `test_logical_engine.py`
3. Update documentation

## File Structure - هيكل الملفات

```
bayan/
├── bayan/
│   ├── __init__.py              # Package initialization
│   ├── lexer.py                 # Tokenizer
│   ├── parser.py                # Parser
│   ├── ast_nodes.py             # AST definitions
│   ├── logical_engine.py        # Logical inference
│   ├── traditional_interpreter.py  # Imperative interpreter
│   ├── hybrid_interpreter.py    # Hybrid interpreter
│   └── builtins.py              # Built-in functions
├── main.py                      # Entry point
├── examples/                    # Example programs
├── tests/                       # Test suite
├── docs/                        # Documentation
└── README.md
```

## Common Tasks - المهام الشائعة

### Adding a New Token Type

1. Add to `TokenType` enum in `lexer.py`
2. Add recognition logic in `Lexer.tokenize()`
3. Update parser to handle new token

### Adding a New AST Node

1. Create class in `ast_nodes.py`
2. Add visitor method to interpreters
3. Add parsing logic to `parser.py`

### Adding a New Operator

1. Add token type to `lexer.py`
2. Add parsing logic to `parser.py`
3. Add interpretation logic to interpreter
4. Add tests

## Debugging - تصحيح الأخطاء

### Enable Debug Output

```python
# In your code
print(f"DEBUG: {variable}")
```

### Common Issues

1. **Token not recognized** - Check lexer token types
2. **Parse error** - Check parser grammar
3. **Interpretation error** - Check interpreter logic
4. **Logical query fails** - Check unification algorithm

## Performance Optimization - تحسين الأداء

1. Profile code to find bottlenecks
2. Optimize hot paths
3. Consider caching/memoization
4. Reduce unnecessary copying

## Documentation - التوثيق

- Update README.md for user-facing changes
- Update LANGUAGE_GUIDE.md for language features
- Update ARCHITECTURE.md for internal changes
- Add docstrings to code

## Reporting Issues - الإبلاغ عن المشاكل

When reporting issues, include:
1. Description of the problem
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Environment (Python version, OS)

## Code Review - مراجعة الكود

All contributions will be reviewed for:
1. Correctness
2. Code quality
3. Test coverage
4. Documentation
5. Performance

## License - الترخيص

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions - الأسئلة

For questions, please open an issue or contact the development team.


