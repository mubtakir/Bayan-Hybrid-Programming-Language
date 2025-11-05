# Bayan Language - Quick Reference for LLMs

## Essential Rules

1. **Wrap all code in `hybrid { ... }`**
2. **Use `:` before `{` in functions, classes, and control structures**
3. **Use `{ }` braces for all blocks**
4. **End logic facts/rules with `.`**
5. **Logic variables start with `?`**

## Syntax Template

```bayan
hybrid {
    # Imperative
    x = 10
    
    # Function
    def function_name(param): {
        return param * 2
    }
    
    # Class
    class ClassName: {
        def __init__(self, value): {
            self.value = value
        }
    }
    
    # Control flow
    if condition: {
        statement
    }
    
    for item in items: {
        statement
    }
    
    # Logic
    fact("data").
    rule(?X) :- condition(?X).
    results = query rule(?X)?
}
```

## Keywords

**English**: `if`, `elif`, `else`, `for`, `in`, `while`, `def`, `return`, `class`, `self`, `True`, `False`, `None`, `and`, `or`, `not`, `try`, `except`, `finally`, `raise`, `with`, `async`, `await`, `yield`, `lambda`, `import`, `from`, `global`, `del`, `pass`, `break`, `continue`

**Arabic**: `اذا`, `والا_اذا`, `والا`, `لكل`, `في`, `بينما`, `دالة`, `ارجع`, `صنف`, `الذات`, `صحيح`, `خطأ`, `لاشيء`

## Data Types

```bayan
hybrid {
    integer = 42
    floating = 3.14
    string = "text"
    arabic_string = "نص عربي"
    boolean = True
    none_value = None
    list_data = [1, 2, 3]
    dict_data = {"key": "value"}
    set_data = {1, 2, 3}
}
```

## Control Flow

```bayan
hybrid {
    # If-elif-else
    if x > 0: {
        print("positive")
    }
    elif x < 0: {
        print("negative")
    }
    else: {
        print("zero")
    }
    
    # For loop
    for i in range(5): {
        print(i)
    }
    
    # While loop
    while x < 10: {
        x = x + 1
    }
}
```

## Functions

```bayan
hybrid {
    # Basic
    def add(a, b): {
        return a + b
    }
    
    # Default params
    def greet(name, msg="Hello"): {
        return msg + " " + name
    }
    
    # *args
    def sum_all(*nums): {
        total = 0
        for n in nums: {
            total = total + n
        }
        return total
    }
    
    # **kwargs
    def print_info(**info): {
        for key in info: {
            print(key + ": " + str(info[key]))
        }
    }
}
```

## Classes

```bayan
hybrid {
    class Person: {
        def __init__(self, name, age): {
            self.name = name
            self.age = age
        }
        
        def greet(self): {
            return "Hello, " + self.name
        }
    }
    
    person = Person("أحمد", 25)
    print(person.greet())
}
```

## Logic Programming

```bayan
hybrid {
    # Facts (end with .)
    parent("أحمد", "محمد").
    parent("محمد", "علي").
    
    # Rules (use :-)
    grandparent(?X, ?Z) :- parent(?X, ?Y), parent(?Y, ?Z).
    
    # Query (use ?)
    results = query grandparent(?GP, "علي")?
    
    for result in results: {
        print(result["?GP"])
    }
    
    # Dynamic KB
    assertz(new_fact("data"))
    retract(old_fact("data"))
    
    # Meta-predicates
    all_results = query findall(?X, fact(?X), ?List)?
}
```

## Built-in Functions

```bayan
hybrid {
    # Type conversion
    int("123"), float("3.14"), str(456)
    
    # String
    upper("text"), lower("TEXT"), len("text")
    
    # List/Collection
    len([1,2,3]), sorted([3,1,2]), sum([1,2,3])
    min([1,2,3]), max([1,2,3]), reversed([1,2,3])
    
    # Functional
    list(map(lambda x: x*2, [1,2,3]))
    list(filter(lambda x: x>0, [-1,0,1]))
    enumerate([1,2,3]), zip([1,2], [3,4])
}
```

## Common Patterns

### Pattern 1: Hybrid OOP + Logic
```bayan
hybrid {
    class Student: {
        def __init__(self, name, grade): {
            self.name = name
            self.grade = grade
            assertz(student(name, grade))
        }
    }
    
    s1 = Student("أحمد", 85)
    s2 = Student("فاطمة", 95)
    
    results = query student(?N, ?G), ?G >= 90?
    for r in results: {
        print(r["?N"])
    }
}
```

### Pattern 2: Expert System
```bayan
hybrid {
    symptom("p1", "fever").
    symptom("p1", "cough").
    
    diagnosis(?P, "flu") :- symptom(?P, "fever"), symptom(?P, "cough").
    
    results = query diagnosis("p1", ?D)?
    print(results[0]["?D"])
}
```

### Pattern 3: Data Processing
```bayan
hybrid {
    data = [85, 92, 78, 95, 88]
    
    avg = sum(data) / len(data)
    high = list(filter(lambda x: x >= 90, data))
    
    print("Average: " + str(avg))
    print("High: " + str(high))
}
```

## ✅ Checklist for LLMs

- [ ] Code wrapped in `hybrid { }`
- [ ] `:` before `{` in def/class/if/for/while
- [ ] `{ }` braces for all blocks
- [ ] `.` at end of facts/rules
- [ ] `?` prefix for logic variables
- [ ] String concatenation with `+` (not multiple print args)
- [ ] Arabic text supported in strings

## Common Mistakes to Avoid

❌ **Wrong**: Missing `hybrid`
```bayan
x = 10  # ERROR
```

❌ **Wrong**: Missing `:`
```bayan
hybrid {
    def f(x) {  # ERROR: missing :
        return x
    }
}
```

❌ **Wrong**: Missing braces
```bayan
hybrid {
    if x > 0:  # ERROR: missing { }
        print(x)
}
```

❌ **Wrong**: Missing `.` in logic
```bayan
hybrid {
    parent("a", "b")  # ERROR: missing .
}
```

✅ **Correct**:
```bayan
hybrid {
    def f(x): {
        return x
    }
    
    if x > 0: {
        print(x)
    }
    
    parent("a", "b").
}
```

---

**Use this reference when generating Bayan code. Follow the syntax strictly!**

