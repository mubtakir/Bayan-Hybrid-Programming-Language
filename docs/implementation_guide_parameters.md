# دليل تطبيق المعاملات الافتراضية والمسماة
# Implementation Guide for Default and Named Parameters

## 📋 نظرة عامة على التطبيق

هذا الدليل يشرح خطوات تطبيق المعاملات الافتراضية والمسماة في المترجم.

---

## 1. تحديث AST (Abstract Syntax Tree)

### الملف: `bayanLBython/bayan/bayan/ast_nodes.py`

#### إضافة فئة جديدة للمعاملات:
```python
@dataclass
class Parameter:
    """تمثيل معامل دالة"""
    name: str
    default_value: Optional[Any] = None
    
    def has_default(self):
        return self.default_value is not None

@dataclass
class NamedArgument:
    """تمثيل معامل مسمى"""
    name: str
    value: Any
```

#### تحديث FunctionDef:
```python
@dataclass
class FunctionDef:
    name: str
    parameters: List[Parameter]  # تغيير من List[str]
    body: Any
```

---

## 2. تحديث المحلل (Parser)

### الملف: `bayanLBython/bayan/bayan/parser.py`

#### تحديث `parse_parameter_list()`:
```python
def parse_parameter_list(self):
    """Parse function parameters with optional defaults"""
    params = []
    
    if not self.match(TokenType.RPAREN):
        # Parse first parameter
        param_name = self.eat(TokenType.IDENTIFIER).value
        default_val = None
        
        if self.match(TokenType.ASSIGN):
            self.eat(TokenType.ASSIGN)
            default_val = self.parse_expression()
        
        params.append(Parameter(param_name, default_val))
        
        # Parse remaining parameters
        while self.match(TokenType.COMMA):
            self.eat(TokenType.COMMA)
            param_name = self.eat(TokenType.IDENTIFIER).value
            default_val = None
            
            if self.match(TokenType.ASSIGN):
                self.eat(TokenType.ASSIGN)
                default_val = self.parse_expression()
            
            params.append(Parameter(param_name, default_val))
    
    return params
```

#### تحديث `parse_argument_list()`:
```python
def parse_argument_list(self):
    """Parse function arguments (positional and named)"""
    args = []
    named_args = {}
    
    if not self.match(TokenType.RPAREN):
        # Check if first argument is named
        if self.match(TokenType.IDENTIFIER) and self.peek_ahead(1).type == TokenType.ASSIGN:
            # Named argument
            name = self.eat(TokenType.IDENTIFIER).value
            self.eat(TokenType.ASSIGN)
            value = self.parse_expression()
            named_args[name] = value
        else:
            # Positional argument
            args.append(self.parse_expression())
        
        # Parse remaining arguments
        while self.match(TokenType.COMMA):
            self.eat(TokenType.COMMA)
            
            if self.match(TokenType.IDENTIFIER) and self.peek_ahead(1).type == TokenType.ASSIGN:
                name = self.eat(TokenType.IDENTIFIER).value
                self.eat(TokenType.ASSIGN)
                value = self.parse_expression()
                named_args[name] = value
            else:
                args.append(self.parse_expression())
    
    return args, named_args
```

---

## 3. تحديث المترجم (Interpreter)

### الملف: `bayanLBython/bayan/bayan/traditional_interpreter.py`

#### تحديث `visit_function_call()`:
```python
def visit_function_call(self, node):
    """Visit a function call with support for default and named parameters"""
    
    if node.name in self.functions:
        func_def = self.functions[node.name]
        
        # Evaluate positional arguments
        positional_args = [self.interpret(arg) for arg in node.arguments]
        
        # Evaluate named arguments
        named_args = {}
        if hasattr(node, 'named_arguments'):
            for name, value in node.named_arguments.items():
                named_args[name] = self.interpret(value)
        
        # Create new local environment
        old_local_env = self.local_env
        self.local_env = {}
        
        # Bind parameters
        param_index = 0
        for param in func_def.parameters:
            if param.name in named_args:
                # Use named argument
                self.local_env[param.name] = named_args[param.name]
            elif param_index < len(positional_args):
                # Use positional argument
                self.local_env[param.name] = positional_args[param_index]
                param_index += 1
            elif param.has_default():
                # Use default value
                self.local_env[param.name] = self.interpret(param.default_value)
            else:
                # Missing required parameter
                raise TypeError(f"Missing required parameter: {param.name}")
        
        try:
            result = self.interpret(func_def.body)
        except ReturnValue as ret:
            result = ret.value
        finally:
            self.local_env = old_local_env
        
        return result
```

---

## 4. الاختبارات

### ملف الاختبار: `test_parameters.by`

```bayan
# اختبار المعاملات الافتراضية
def greet(name, greeting="مرحبا"):
{
    print(greeting + " " + name)
}

greet("أحمد")
greet("فاطمة", "السلام عليكم")

# اختبار المعاملات المسماة
def create_user(name, age, email):
{
    return { "name": name, "age": age, "email": email }
}

user1 = create_user(name="علي", age=25, email="ali@example.com")
user2 = create_user("محمد", email="m@example.com", age=30)
```

---

## 5. الخطوات التالية

1. ✅ تحديث AST
2. ✅ تحديث المحلل
3. ✅ تحديث المترجم
4. ✅ كتابة الاختبارات
5. ✅ تحديث الوثائق
6. ✅ دعم الأصناف والدوال الخاصة

---

## 6. الحالة الحالية

**الحالة:** ⏳ جاهز للتطبيق  
**الأولوية:** عالية جداً  
**التعقيد:** متوسط

