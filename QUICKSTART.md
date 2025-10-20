# Bayan Language - Quick Start Guide - دليل البدء السريع

## Installation - التثبيت

```bash
cd bayanLang/bayan
```

## Running Examples - تشغيل الأمثلة

### Family Relations Example
```bash
python main.py examples/family.by
```

### Calculator Example
```bash
python main.py examples/calculator.by
```

## Running Tests - تشغيل الاختبارات

```bash
# Run all tests
python tests/test_lexer.py
python tests/test_logical_engine.py
python tests/test_traditional_interpreter.py
python tests/test_hybrid_interpreter.py
```

## Interactive Mode - الوضع التفاعلي

```bash
python main.py
```

Then type Bayan code:
```
>>> x = 10
>>> print(x)
10
>>> exit
```

## Basic Syntax - بناء الجملة الأساسي

### Variables and Assignment
```bayan
x = 10
name = "Ahmed"
items = [1, 2, 3]
```

### Arithmetic
```bayan
result = 10 + 5
print(result)  # Output: 15
```

### Control Flow
```bayan
if x > 5:
{
    print("x is greater than 5")
}
```

### Functions
```bayan
def add(a, b):
{
    return a + b
}

result = add(5, 3)
print(result)  # Output: 8
```

### Loops
```bayan
for i in range(5):
{
    print(i)
}
```

## Logical Programming - البرمجة المنطقية

### Facts
```bayan
parent("john", "mary").
parent("mary", "susan").
```

### Rules
```bayan
grandparent(?X, ?Z) :- parent(?X, ?Y), parent(?Y, ?Z).
```

### Queries
```bayan
query parent("john", ?X).
```

## Hybrid Programming - البرمجة الهجينة

```bayan
hybrid {
    # Traditional code
    x = 10
    
    # Logical facts
    number(10).
    number(20).
    
    # Mixed code
    if number(x):
    {
        print("x is a number")
    }
}
```

## Arabic Support - دعم اللغة العربية

```bayan
hybrid {
    الاسم = "أحمد"
    العمر = 30
    
    شخص("أحمد", 30).
    
    print(الاسم)
}
```

## Built-in Functions - الدوال المدمجة

- `print(value)` - Print to console
- `len(list)` - Get length
- `range(n)` - Create range
- `str(value)` - Convert to string
- `int(value)` - Convert to integer
- `float(value)` - Convert to float
- `upper(string)` - Uppercase
- `lower(string)` - Lowercase
- `type(value)` - Get type

## File Extension - امتداد الملف

Use `.by` extension for Bayan files:
```
program.by
family.by
calculator.by
```

## Common Patterns - الأنماط الشائعة

### List Iteration
```bayan
items = [1, 2, 3]
for item in items:
{
    print(item)
}
```

### Dictionary Access
```bayan
person = {name: "Ali", age: 30}
print(person[name])
```

### String Concatenation
```bayan
greeting = "Hello " + "World"
print(greeting)
```

### Conditional Logic
```bayan
x = 10
if x > 5:
{
    print("Greater")
}
else:
{
    print("Less or equal")
}
```

## Logical Variables - المتغيرات المنطقية

Use `?` prefix for logical variables:
```bayan
query parent("john", ?X).  # Find all children of john
```

## Comments - التعليقات

```bayan
# This is a comment
# هذا تعليق
```

## Error Handling - معالجة الأخطاء

If you get an error, check:
1. File syntax - Use `.by` extension
2. Indentation - Use proper indentation
3. Brackets - Match all `{` with `}`
4. Quotes - Match all quotes
5. Logical variables - Use `?` prefix

## Documentation - التوثيق

For more information, see:
- `README.md` - Project overview
- `LANGUAGE_GUIDE.md` - Complete language guide
- `EXAMPLES.md` - More examples
- `ARCHITECTURE.md` - Internal design
- `PROJECT_STATUS.md` - Project status

## Tips - نصائح

1. Start with simple programs
2. Use hybrid blocks to combine paradigms
3. Use logical variables with `?` prefix
4. Test your code with different inputs
5. Use comments to explain complex logic
6. Check examples for patterns
7. Use Arabic identifiers for clarity
8. Run tests to verify functionality

## Next Steps - الخطوات التالية

1. Read LANGUAGE_GUIDE.md for complete syntax
2. Study EXAMPLES.md for more examples
3. Review example programs (family.by, calculator.by)
4. Create your own programs
5. Explore the source code
6. Contribute improvements

## Support - الدعم

For issues or questions:
1. Check documentation
2. Review examples
3. Examine test files
4. Read source code
5. Check error messages

## Version - الإصدار

- **Version**: 0.1.0
- **Status**: Complete and Ready
- **Python**: 3.7+
- **License**: MIT

---

**Happy coding with Bayan!**
**برمجة سعيدة مع بيان!**


