# Bayan Language Examples - أمثلة لغة بيان

## Example 1: Family Relations - العلاقات العائلية

This example demonstrates logical programming with facts and rules.

```bayan
hybrid {
    # Facts - الحقائق
    parent("خالد", "أحمد").
    parent("فاطمة", "أحمد").
    parent("أحمد", "محمد").
    parent("أحمد", "سارة").
    parent("محمد", "علي").
    
    # Rules - القواعد
    grandparent(?X, ?Z) :- parent(?X, ?Y), parent(?Y, ?Z).
    sibling(?X, ?Y) :- parent(?P, ?X), parent(?P, ?Y).
    ancestor(?X, ?Y) :- parent(?X, ?Y).
    ancestor(?X, ?Z) :- parent(?X, ?Y), ancestor(?Y, ?Z).
    
    # Queries
    print("Grandparents of محمد:")
    query grandparent(?GP, "محمد").
    
    print("Siblings of أحمد:")
    query sibling("أحمد", ?SIB).
}
```

**Output:**
```
Grandparents of محمد:
Siblings of أحمد:
```

## Example 2: Calculator - الآلة الحاسبة

This example demonstrates traditional programming with functions.

```bayan
hybrid {
    def add(a, b):
    {
        return a + b
    }
    
    def subtract(a, b):
    {
        return a - b
    }
    
    def multiply(a, b):
    {
        return a * b
    }
    
    def divide(a, b):
    {
        if b == 0:
        {
            print("Error: Division by zero")
            return None
        }
        return a / b
    }
    
    x = 10
    y = 5
    
    print("x + y = " + str(add(x, y)))
    print("x - y = " + str(subtract(x, y)))
    print("x * y = " + str(multiply(x, y)))
    print("x / y = " + str(divide(x, y)))
}
```

**Output:**
```
x + y = 15
x - y = 5
x * y = 50
x / y = 2.0
```

## Example 3: List Operations - عمليات القوائم

```bayan
hybrid {
    numbers = [1, 2, 3, 4, 5]
    
    print("Original list: " + str(numbers))
    
    # Iterate through list
    for num in numbers:
    {
        print("Number: " + str(num))
    }
    
    # List operations
    print("Length: " + str(len(numbers)))
    print("First: " + str(numbers[0]))
}
```

## Example 4: Dictionary Operations - عمليات القواموس

```bayan
hybrid {
    person = {name: "Ahmed", age: 30, city: "Cairo"}
    
    print("Name: " + person[name])
    print("Age: " + str(person[age]))
    print("City: " + person[city])
}
```

## Example 5: Control Flow - التحكم في التدفق

```bayan
hybrid {
    x = 10
    
    if x > 5:
    {
        print("x is greater than 5")
    }
    else:
    {
        print("x is less than or equal to 5")
    }
    
    # For loop
    for i in range(5):
    {
        print("i = " + str(i))
    }
    
    # While loop
    count = 0
    while count < 3:
    {
        print("count = " + str(count))
        count = count + 1
    }
}
```

## Example 6: Hybrid Logic - المنطق الهجين

```bayan
hybrid {
    # Define facts
    student("Ahmed", "Math").
    student("Fatima", "Science").
    student("Ali", "Math").
    
    # Define rules
    classmate(?X, ?Y) :- student(?X, ?C), student(?Y, ?C).
    
    # Traditional code
    print("Students in Math class:")
    
    # Use logical query in traditional code
    if student("Ahmed", ?Subject):
    {
        print("Ahmed studies: " + ?Subject)
    }
}
```

## Example 7: String Operations - عمليات النصوص

```bayan
hybrid {
    text = "Hello Bayan"
    
    print("Original: " + text)
    print("Length: " + str(len(text)))
    print("Uppercase: " + upper(text))
    print("Lowercase: " + lower(text))
}
```

## Example 8: Arithmetic Operations - العمليات الحسابية

```bayan
hybrid {
    a = 10
    b = 3
    
    print("a + b = " + str(a + b))
    print("a - b = " + str(a - b))
    print("a * b = " + str(a * b))
    print("a / b = " + str(a / b))
    print("a % b = " + str(a % b))
}
```

## Example 9: Boolean Operations - العمليات المنطقية

```bayan
hybrid {
    x = True
    y = False
    
    print("x and y = " + str(x and y))
    print("x or y = " + str(x or y))
    print("not x = " + str(not x))
}
```

## Example 10: Arabic Identifiers - المعرفات العربية

```bayan
hybrid {
    الاسم = "أحمد"
    العمر = 30
    المدينة = "القاهرة"
    
    print("الاسم: " + الاسم)
    print("العمر: " + str(العمر))
    print("المدينة: " + المدينة)
    
    # Logical facts with Arabic
    شخص("أحمد", 30).
    شخص("فاطمة", 25).
    
    print("الأشخاص:")
    query شخص(?اسم, ?عمر).
}
```

## Running Examples - تشغيل الأمثلة

```bash
# Run family example
python main.py examples/family.by

# Run calculator example
python main.py examples/calculator.by

# Run custom code
python main.py your_file.by
```

## Tips for Writing Bayan Code - نصائح لكتابة كود بيان

1. Use hybrid blocks to combine traditional and logical code
2. Use logical variables with `?` prefix
3. Use facts for static data
4. Use rules for relationships
5. Use queries to find solutions
6. Support Arabic identifiers for better readability
7. Add comments to explain complex logic
8. Test your code with different inputs


