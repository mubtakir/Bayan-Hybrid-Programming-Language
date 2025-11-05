# Bayan Language Guide - دليل لغة بيان

## Introduction - المقدمة

Bayan is a hybrid programming language that combines traditional imperative programming with logical programming. It supports both Python-like syntax and Prolog-like logical constructs.

بيان هي لغة برمجية هجينة تجمع بين البرمجة الإجرائية التقليدية والبرمجة المنطقية. تدعم كلا من بناء جملة يشبه Python والبنى المنطقية التي تشبه Prolog.

## Basic Syntax - بناء الجملة الأساسي

### Variables and Assignment - المتغيرات والإسناد

```bayan
x = 10
name = "Ahmed"
items = [1, 2, 3]
person = {name: "Ali", age: 30}
```

### Data Types - أنواع البيانات

- **Numbers**: `42`, `3.14`
- **Strings**: `"hello"`, `'world'`
- **Booleans**: `True`, `False`
- **Lists**: `[1, 2, 3]`
- **Dictionaries**: `{key: value}`
- **Logical Variables**: `?X`, `?Name`

### Control Flow - التحكم في التدفق

```bayan
# If statement
if x > 5:
{
    print("x is greater than 5")
}

# For loop
for i in range(10):
{
    print(i)
}

# While loop
while x > 0:
{
    x = x - 1
}
```

### Functions - الدوال

```bayan
def add(a, b):
{
    return a + b
}

result = add(5, 3)
```

## Logical Programming - البرمجة المنطقية

### Facts - الحقائق

```bayan
parent("john", "mary").
parent("mary", "susan").
```

### Rules - القواعد

```bayan
grandparent(?X, ?Z) :- parent(?X, ?Y), parent(?Y, ?Z).
```

### Queries - الاستعلامات

```bayan
query parent("john", ?X).
```

## Hybrid Blocks - الكتل الهجينة

```bayan
hybrid {
    # Traditional code
    x = 10
    y = 20
    
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

## Built-in Functions - الدوال المدمجة

- `print(value)` - Print to console
- `len(list)` - Get length
- `range(n)` - Create range
- `str(value)` - Convert to string
- `int(value)` - Convert to integer
- `float(value)` - Convert to float

## Arabic Support - دعم اللغة العربية

```bayan
hybrid {
    الاسم = "أحمد"
    العمر = 30
    
    شخص("أحمد", 30).
    شخص("فاطمة", 25).
    
    print(الاسم)
}
```

## Examples - أمثلة

### Family Relations

```bayan
hybrid {
    parent("john", "mary").
    parent("mary", "susan").
    
    grandparent(?X, ?Z) :- parent(?X, ?Y), parent(?Y, ?Z).
    
    query grandparent("john", ?X).
}
```

### Calculator

```bayan
hybrid {
    def add(a, b):
    {
        return a + b
    }
    
    result = add(10, 5)
    print(result)
}
```

## Comments - التعليقات

```bayan
# This is a comment
# هذا تعليق
```

## Operators - المعاملات

### Arithmetic - الحسابية
- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division
- `%` Modulo

### Comparison - المقارنة
- `==` Equal
- `!=` Not equal
- `<` Less than
- `>` Greater than
- `<=` Less than or equal
- `>=` Greater than or equal

### Logical - المنطقية
- `and` AND
- `or` OR
- `not` NOT

## String Operations - عمليات النصوص

```bayan
s = "hello"
s2 = s + " world"
length = len(s)
```

## List Operations - عمليات القوائم

```bayan
items = [1, 2, 3]
items.append(4)
first = items[0]
```

## Dictionary Operations - عمليات القواميس

```bayan
person = {name: "Ali", age: 30}
name = person[name]
```

## Tips and Best Practices - نصائح وأفضل الممارسات

1. Use hybrid blocks to combine traditional and logical code
2. Use logical variables with `?` prefix
3. Use facts for static data
4. Use rules for relationships
5. Use queries to find solutions
6. Support Arabic identifiers for better readability


