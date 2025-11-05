# 🔧 الدليل التقني للتنفيذ - لغة البيان
# Technical Implementation Guide - Bayan Language

**الجمهور | Audience**: نموذج ذكاء اصطناعي متقدم  
**الهدف | Goal**: تنفيذ الميزات المتبقية بجودة عالية

---

## 📐 البنية التقنية | Technical Architecture

### 1. Lexer (المحلل المعجمي)

**الملف**: `bayan/bayan/lexer.py`

**المسؤوليات**:
- تحويل النص المصدري إلى tokens
- التعرف على الكلمات المفتاحية
- معالجة Unicode (العربية)
- معالجة الأرقام والسلاسل النصية

**Token Types المُضافة حديثاً**:
```python
class TokenType(Enum):
    # ... existing tokens
    PIPE = auto()      # | for list patterns
    IS = auto()        # is for arithmetic
    ASYNC = auto()     # async keyword
    AWAIT = auto()     # await keyword
    YIELD = auto()     # yield keyword
    WITH = auto()      # with keyword
    CUT = auto()       # ! for cut operator
    AT = auto()        # @ for decorators
```

**كيفية إضافة token جديد**:
1. أضف في `TokenType` enum
2. أضف في `KEYWORDS` dict (إذا كان keyword)
3. أضف في `tokenize()` method للتعرف عليه

---

### 2. Parser (المحلل اللغوي)

**الملف**: `bayan/bayan/parser.py`

**المسؤوليات**:
- تحويل tokens إلى AST
- التحقق من صحة البناء اللغوي
- معالجة الأخطاء

**Methods الرئيسية**:
```python
class HybridParser:
    def parse(self):
        """Parse entire program"""
        
    def parse_statement(self):
        """Parse single statement"""
        
    def parse_expression(self):
        """Parse expression"""
        
    def parse_logical_goal(self):
        """Parse logical goal (for hybrid blocks)"""
        
    def parse_logical_term(self):
        """Parse logical term (variable, atom, list, etc.)"""
```

**كيفية إضافة statement جديد**:
1. أضف case في `parse_statement()`
2. أنشئ method جديد `parse_xxx()`
3. أنشئ AST node جديد في `ast_nodes.py`

---

### 3. AST Nodes (عقد الشجرة التجريدية)

**الملف**: `bayan/bayan/ast_nodes.py`

**المسؤوليات**:
- تمثيل عناصر اللغة
- توفير بنية موحدة للمفسر

**AST Nodes المُضافة حديثاً**:
```python
class ListPattern:
    """[?H|?T] pattern"""
    def __init__(self, heads, tail):
        self.heads = heads
        self.tail = tail

class IsExpression:
    """?X is 5 + 3"""
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

class AsyncFunctionDef:
    """async def func(): {...}"""
    def __init__(self, name, params, body, decorators=None):
        self.name = name
        self.params = params
        self.body = body
        self.decorators = decorators or []

class AwaitExpr:
    """await expr"""
    def __init__(self, expr):
        self.expr = expr

class YieldExpr:
    """yield value"""
    def __init__(self, value):
        self.value = value

class WithStatement:
    """with expr as var: {...}"""
    def __init__(self, context_expr, var_name, body):
        self.context_expr = context_expr
        self.var_name = var_name
        self.body = body

class Cut:
    """! operator"""
    def __repr__(self):
        return "Cut(!)"

class Decorator:
    """@decorator or @decorator(args)"""
    def __init__(self, name, args=None):
        self.name = name
        self.args = args or []
```

**كيفية إضافة AST node جديد**:
1. أنشئ class جديد
2. أضف `__init__` مع المعاملات المطلوبة
3. أضف `__repr__` للتمثيل النصي
4. أضف visitor method في المفسر

---

### 4. Logical Engine (المحرك المنطقي)

**الملف**: `bayan/bayan/logical_engine.py`

**المسؤوليات**:
- تنفيذ facts و rules
- التوحيد (unification)
- الرجوع للخلف (backtracking)
- معالجة queries

**Methods الرئيسية**:
```python
class LogicalEngine:
    def add_fact(self, fact):
        """Add a fact to knowledge base"""
        
    def add_rule(self, rule):
        """Add a rule to knowledge base"""
        
    def query(self, goal):
        """Query the knowledge base"""
        
    def unify(self, term1, term2, bindings):
        """Unify two terms"""
        
    def _solve_goals(self, goals, bindings, depth=0):
        """Solve a list of goals (with backtracking)"""
```

**التوحيد مع List Patterns**:
```python
def unify(self, term1, term2, bindings):
    """Unify two terms with list pattern support"""
    # ... existing code
    
    # List pattern unification
    if isinstance(term1, ListPattern) and isinstance(term2, list):
        # Unify heads
        if len(term2) < len(term1.heads):
            return None
        
        for i, head in enumerate(term1.heads):
            bindings = self.unify(head, term2[i], bindings)
            if bindings is None:
                return None
        
        # Unify tail
        tail_list = term2[len(term1.heads):]
        bindings = self.unify(term1.tail, tail_list, bindings)
        
        return bindings
```

**معالجة is operator**:
```python
def _solve_goals(self, goals, bindings, depth=0):
    """Solve goals with is operator support"""
    # ... existing code
    
    if isinstance(goal, IsExpression):
        # Evaluate arithmetic expression
        value = self._evaluate_arithmetic(goal.expr, bindings)
        
        # Unify with variable
        bindings = self.unify(goal.var, value, bindings)
        
        if bindings is not None:
            # Continue with remaining goals
            for result in self._solve_goals(rest, bindings, depth):
                yield result
```

---

### 5. Traditional Interpreter (المفسر التقليدي)

**الملف**: `bayan/bayan/traditional_interpreter.py`

**المسؤوليات**:
- تنفيذ الكود الإجرائي والكائني
- معالجة المتغيرات والدوال
- معالجة الأصناف والكائنات

**Visitor Pattern**:
```python
class TraditionalInterpreter:
    def visit(self, node):
        """Visit a node using visitor pattern"""
        method_name = f'visit_{node.__class__.__name__.lower()}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def visit_functiondef(self, node):
        """Visit function definition"""
        # Implementation
    
    def visit_classdef(self, node):
        """Visit class definition"""
        # Implementation
```

---

## 🎯 المهام التقنية المطلوبة | Required Technical Tasks

### المهمة 1: تنفيذ Cut في المحرك المنطقي

**الملف**: `bayan/bayan/logical_engine.py`

**التحدي**: منع الرجوع للخلف بعد Cut

**الحل المقترح**:
```python
class LogicalEngine:
    def _solve_goals(self, goals, bindings, depth=0):
        """Solve goals with cut support"""
        if not goals:
            yield bindings
            return
        
        goal = goals[0]
        rest = goals[1:]
        
        # Handle cut operator
        if isinstance(goal, Cut):
            # Execute remaining goals WITHOUT backtracking
            for result in self._solve_goals(rest, bindings, depth):
                yield result
            return  # Stop here - no more solutions
        
        # Handle regular goals
        for new_bindings in self._solve_goal(goal, bindings, depth):
            # Check if any remaining goal is a cut
            has_cut = any(isinstance(g, Cut) for g in rest)
            
            for result in self._solve_goals(rest, new_bindings, depth):
                yield result
                
                # If we found a cut, stop backtracking
                if has_cut:
                    return
```

**الاختبار**:
```python
def test_cut_prevents_backtracking():
    code = """
    hybrid {
        rule max(?X, ?Y, ?X) :- ?X >= ?Y, !.
        rule max(?X, ?Y, ?Y).
        
        query max(5, 3, ?Result).
    }
    """
    # Should return only ?Result = 5, not backtrack to second rule
```

---

### المهمة 2: تنفيذ Decorators في المفسر

**الملف**: `bayan/bayan/traditional_interpreter.py`

**التحدي**: تطبيق decorators بالترتيب الصحيح

**الحل المقترح**:
```python
def visit_functiondef(self, node):
    """Visit function definition with decorator support"""
    # Create the base function
    def base_function(*args, **kwargs):
        # Create local environment
        local_env = Environment(parent=self.env)
        
        # Bind parameters
        for param, arg in zip(node.params, args):
            local_env[param] = arg
        
        # Execute body
        old_env = self.env
        self.env = local_env
        try:
            result = None
            for stmt in node.body:
                result = self.visit(stmt)
                if isinstance(stmt, Return):
                    break
            return result
        finally:
            self.env = old_env
    
    # Apply decorators (bottom to top)
    func = base_function
    for decorator in reversed(node.decorators):
        # Get decorator function
        decorator_func = self.visit(Identifier(decorator.name))
        
        if decorator.args:
            # Decorator with arguments: @decorator(args)
            args = [self.visit(arg) for arg in decorator.args]
            # Call decorator factory
            decorator_func = decorator_func(*args)
        
        # Apply decorator
        func = decorator_func(func)
    
    # Store decorated function
    self.env[node.name] = func
```

**الاختبار**:
```python
def test_decorator_application():
    code = """
    def log_decorator(func): {
        def wrapper(*args): {
            print("Calling:", func.__name__)
            result = func(*args)
            print("Result:", result)
            return result
        }
        return wrapper
    }
    
    @log_decorator
    def add(x, y): {
        return x + y
    }
    
    result = add(2, 3)
    """
    # Should print: "Calling: add", "Result: 5"
    # result should be 5
```

---

### المهمة 3: تنفيذ Async/Await

**الملف**: `bayan/bayan/traditional_interpreter.py`

**التحدي**: دعم البرمجة غير المتزامنة

**الحل المقترح**:
```python
import asyncio

def visit_asyncfunctiondef(self, node):
    """Visit async function definition"""
    async def async_function(*args, **kwargs):
        # Create local environment
        local_env = Environment(parent=self.env)
        
        # Bind parameters
        for param, arg in zip(node.params, args):
            local_env[param] = arg
        
        # Execute body
        old_env = self.env
        self.env = local_env
        try:
            result = None
            for stmt in node.body:
                result = self.visit(stmt)
                if isinstance(stmt, Return):
                    break
            return result
        finally:
            self.env = old_env
    
    # Apply decorators if any
    func = async_function
    for decorator in reversed(node.decorators):
        decorator_func = self.visit(Identifier(decorator.name))
        if decorator.args:
            args = [self.visit(arg) for arg in decorator.args]
            decorator_func = decorator_func(*args)
        func = decorator_func(func)
    
    self.env[node.name] = func

def visit_awaitexpr(self, node):
    """Visit await expression"""
    expr = self.visit(node.expr)
    
    # If it's a coroutine, await it
    if asyncio.iscoroutine(expr):
        # We need to be in an async context
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(expr)
    
    return expr
```

**الاختبار**:
```python
def test_async_await():
    code = """
    async def fetch_data(url): {
        # Simulate async operation
        return "Data from " + url
    }
    
    async def main(): {
        result = await fetch_data("https://example.com")
        return result
    }
    
    # Run async function
    result = asyncio.run(main())
    """
    # result should be "Data from https://example.com"
```

---

### المهمة 4: تنفيذ Generators

**الملف**: `bayan/bayan/traditional_interpreter.py`

**التحدي**: دعم yield expressions

**الحل المقترح**:
```python
def _contains_yield(self, node):
    """Check if node contains yield expression"""
    if isinstance(node, YieldExpr):
        return True
    if isinstance(node, list):
        return any(self._contains_yield(n) for n in node)
    if hasattr(node, '__dict__'):
        return any(self._contains_yield(v) for v in node.__dict__.values())
    return False

def visit_functiondef(self, node):
    """Visit function definition (check for yield)"""
    # Check if function contains yield
    has_yield = self._contains_yield(node.body)
    
    if has_yield:
        # Create generator function
        def generator_function(*args, **kwargs):
            # Create local environment
            local_env = Environment(parent=self.env)
            
            # Bind parameters
            for param, arg in zip(node.params, args):
                local_env[param] = arg
            
            # Execute body as generator
            old_env = self.env
            self.env = local_env
            try:
                for stmt in node.body:
                    if isinstance(stmt, YieldExpr):
                        value = self.visit(stmt.value)
                        yield value
                    else:
                        self.visit(stmt)
            finally:
                self.env = old_env
        
        self.env[node.name] = generator_function
    else:
        # Regular function (existing implementation)
        # ... existing code
```

**الاختبار**:
```python
def test_generator():
    code = """
    def fibonacci(n): {
        a = 0
        b = 1
        for i in range(n): {
            yield a
            temp = a
            a = b
            b = temp + b
        }
    }
    
    result = list(fibonacci(5))
    """
    # result should be [0, 1, 1, 2, 3]
```

---

### المهمة 5: تنفيذ Context Managers

**الملف**: `bayan/bayan/traditional_interpreter.py`

**التحدي**: دعم with statements

**الحل المقترح**:
```python
def visit_withstatement(self, node):
    """Visit with statement"""
    # Evaluate context expression
    context = self.visit(node.context_expr)
    
    # Call __enter__ method
    if hasattr(context, '__enter__'):
        value = context.__enter__()
    else:
        value = context
    
    # Bind to variable if specified
    if node.var_name:
        self.env[node.var_name] = value
    
    # Execute body
    exception_occurred = False
    exception_info = (None, None, None)
    
    try:
        result = None
        for stmt in node.body:
            result = self.visit(stmt)
        return result
    except Exception as e:
        exception_occurred = True
        exception_info = (type(e), e, e.__traceback__)
        raise
    finally:
        # Call __exit__ method
        if hasattr(context, '__exit__'):
            context.__exit__(*exception_info)
```

**الاختبار**:
```python
def test_context_manager():
    code = """
    class FileManager: {
        def __init__(self, filename): {
            self.filename = filename
        }
        
        def __enter__(self): {
            print("Opening file:", self.filename)
            return self
        }
        
        def __exit__(self, exc_type, exc_val, exc_tb): {
            print("Closing file:", self.filename)
        }
    }
    
    with FileManager("test.txt") as f: {
        print("Using file:", f.filename)
    }
    """
    # Should print:
    # Opening file: test.txt
    # Using file: test.txt
    # Closing file: test.txt
```

---

## 📝 معايير الجودة | Quality Standards

### 1. الاختبارات | Testing

**كل ميزة يجب أن تحتوي على**:
- ✅ اختبار parsing (AST structure)
- ✅ اختبار execution (runtime behavior)
- ✅ اختبار edge cases
- ✅ اختبار error handling

**مثال**:
```python
def test_feature_parsing():
    """Test that feature parses correctly"""
    code = "..."
    lexer = HybridLexer(code)
    parser = HybridParser(lexer.tokenize())
    ast = parser.parse()
    assert isinstance(ast, ExpectedNode)

def test_feature_execution():
    """Test that feature executes correctly"""
    code = "..."
    result = execute_code(code)
    assert result == expected_value

def test_feature_edge_case():
    """Test edge cases"""
    # Test with empty input, large input, etc.

def test_feature_error_handling():
    """Test error handling"""
    code = "invalid code"
    with pytest.raises(ExpectedError):
        execute_code(code)
```

### 2. التوثيق | Documentation

**كل ميزة يجب أن تحتوي على**:
- ✅ وصف بالعربية والإنجليزية
- ✅ أمثلة واضحة
- ✅ حالات الاستخدام
- ✅ ملاحظات تقنية

### 3. الأمثلة | Examples

**كل ميزة يجب أن تحتوي على**:
- ✅ مثال بسيط
- ✅ مثال متقدم
- ✅ مثال عملي (real-world use case)

---

## 🚀 خطة التنفيذ | Implementation Plan

### الأسبوع 1: تنفيذ الميزات الموجودة
1. ✅ Cut في المحرك المنطقي
2. ✅ Decorators في المفسر
3. ✅ Async/Await في المفسر
4. ✅ Generators في المفسر
5. ✅ Context Managers في المفسر

### الأسبوع 2-5: الميزات الجديدة
- الأسبوع 2: Pattern Matching
- الأسبوع 3: Type Hints
- الأسبوع 4: Modules & Imports
- الأسبوع 5: Error Handling & Testing

---

**حظاً موفقاً! 🚀**

