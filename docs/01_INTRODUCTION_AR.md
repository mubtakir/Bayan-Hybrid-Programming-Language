# دليل لغة البيان - الجزء الأول: مقدمة وتعريف
# Bayan Language Guide - Part 1: Introduction

<div dir="rtl">

## 📚 جدول المحتويات

1. [ما هي لغة البيان؟](#ما-هي-لغة-البيان)
2. [المزايا الرئيسية](#المزايا-الرئيسية)
3. [الكلمات المفتاحية](#الكلمات-المفتاحية)
4. [التثبيت والتشغيل](#التثبيت-والتشغيل)
5. [طرق الاستخدام](#طرق-الاستخدام)
6. [التكامل مع Python](#التكامل-مع-python)
7. [أمثلة سريعة](#أمثلة-سريعة)

---

## ما هي لغة البيان؟

**لغة البيان** هي لغة برمجة ثورية تجمع **ثلاثة أنماط برمجية** في لغة واحدة متكاملة:

### 🎯 الأنماط البرمجية الثلاثة:

#### 1. **البرمجة الإجرائية** (Imperative Programming)
```bayan
x = 10
y = 20
result = x + y
print(result)
```

#### 2. **البرمجة الكائنية** (Object-Oriented Programming)
```bayan
class Person: {
    def __init__(self, name, age): {
        self.name = name
        self.age = age
    }
    
    def greet(self): {
        return "مرحباً، أنا " + self.name
    }
}

person = Person("أحمد", 25)
print(person.greet())
```

#### 3. **البرمجة المنطقية** (Logic Programming - Prolog Style)
```bayan
hybrid {
    # حقائق
    parent("أحمد", "محمد").
    parent("محمد", "علي").
    
    # قواعد
    grandparent(?X, ?Z) :- parent(?X, ?Y), parent(?Y, ?Z).
    
    # استعلام
    results = query grandparent(?GP, "علي")?
    for result in results: {
        print(result["?GP"])
    }
}
```

---

## المزايا الرئيسية

### 🌟 1. البرمجة الهجينة الفريدة
- **الميزة الوحيدة في العالم**: لا توجد لغة أخرى تجمع الثلاثة أنماط بهذا الشكل
- يمكنك استخدام البرمجة المنطقية مع OOP في نفس الكود
- مثالية للذكاء الاصطناعي والأنظمة الخبيرة

### 🌍 2. الدعم الكامل للغة العربية
- **كلمات مفتاحية عربية وإنجليزية**
- **معرّفات عربية** (أسماء متغيرات، دوال، أصناف)
- **تعليقات عربية**
- **نصوص عربية بدون مشاكل** (اتصال الحروف، التشكيل، RTL)

### 🚀 3. سهولة التعلم
- بناء جملة واضح مع أقواس معقوفة `{}`
- مشابه لـ Python و JavaScript
- رسائل خطأ واضحة

### 🔧 4. قوية ومرنة
- **255+ اختبار ناجح** (100% success rate)
- دعم كامل لـ:
  - Generators & Async/Await
  - Decorators & Context Managers
  - Exception Handling
  - Multiple Inheritance
  - Dynamic Knowledge Base (assert/retract)
  - Meta-predicates (findall/bagof/setof)

### 🤖 5. مثالية للذكاء الاصطناعي
- دوال مدمجة للـ ML: `sum`, `min`, `max`, `sorted`, `map`, `filter`
- دعم `*args` و `**kwargs` للمرونة
- البرمجة المنطقية للاستدلال
- قاعدة معرفة ديناميكية

---

## الكلمات المفتاحية

### 📝 الكلمات المفتاحية الإجرائية والكائنية

| العربية | English | الوصف |
|---------|---------|-------|
| اطبع | `print` | طباعة |
| اذا | `if` | شرط |
| والا_اذا | `elif` | شرط آخر |
| والا | `else` | خلاف ذلك |
| لكل | `for` | حلقة تكرار |
| في | `in` | عضوية |
| بينما | `while` | حلقة شرطية |
| دالة / def | `def` | تعريف دالة |
| ارجع | `return` | إرجاع قيمة |
| صنف | `class` | تعريف صنف |
| الذات | `self` | المرجع الذاتي |
| جديد | `new` | إنشاء كائن |
| صحيح | `True` | قيمة منطقية صحيحة |
| خطأ | `False` | قيمة منطقية خاطئة |
| لاشيء | `None` | قيمة فارغة |
| و | `and` | عامل منطقي و |
| او | `or` | عامل منطقي أو |
| ليس | `not` | عامل منطقي ليس |
| استورد | `import` | استيراد مكتبة |
| من | `from` | من مكتبة |
| حاول | `try` | محاولة تنفيذ |
| اعترض | `except` | اعتراض خطأ |
| اخيرا | `finally` | تنفيذ نهائي |
| ارفع | `raise` | رفع استثناء |
| مع | `with` | مدير سياق |
| غير_متزامن | `async` | دالة غير متزامنة |
| انتظر | `await` | انتظار نتيجة |
| انتج | `yield` | إنتاج قيمة (generator) |
| اكسر | `break` | كسر الحلقة |
| استمر | `continue` | استمرار الحلقة |
| مرر | `pass` | تمرير |
| حذف | `del` | حذف |
| عام | `global` | متغير عام |
| محلي | `local` | متغير محلي |
| تأكيد | `assert` | تأكيد شرط |
| هو | `is` | مقارنة هوية |
| lambda | `lambda` | دالة مجهولة |

### 🔍 الكلمات المفتاحية للبرمجة المنطقية

| الرمز | الوصف |
|-------|-------|
| `.` | نهاية حقيقة أو قاعدة |
| `:-` | فاصل بين رأس القاعدة وجسمها |
| `?-` | بداية استعلام |
| `?Variable` | متغير منطقي |
| `,` | عامل AND المنطقي |
| `;` | عامل OR المنطقي |
| `not(Goal)` | نفي الهدف |
| `findall/3` | جمع جميع الحلول |
| `bagof/3` | جمع الحلول (يفشل إذا لم توجد) |
| `setof/3` | جمع حلول فريدة ومرتبة |

---

## التثبيت والتشغيل

### 📦 المتطلبات

- **Python 3.8+** (يُفضل Python 3.10+)
- نظام التشغيل: Linux, Windows, macOS

### 🔧 التثبيت

#### على Linux / macOS:

```bash
# 1. استنساخ المشروع
git clone https://github.com/your-repo/bayan_python.git
cd bayan_python

# 2. إنشاء بيئة افتراضية (اختياري لكن مُوصى به)
python3 -m venv venv
source venv/bin/activate

# 3. تثبيت المتطلبات (إن وجدت)
pip install -r requirements.txt

# 4. اختبار التثبيت
python -m pytest tests/ -v
```

#### على Windows:

```cmd
REM 1. استنساخ المشروع
git clone https://github.com/your-repo/bayan_python.git
cd bayan_python

REM 2. إنشاء بيئة افتراضية
python -m venv venv
venv\Scripts\activate

REM 3. تثبيت المتطلبات
pip install -r requirements.txt

REM 4. اختبار التثبيت
python -m pytest tests/ -v
```

### ▶️ طرق التشغيل

#### 1. تشغيل ملف `.by`:

```bash
# الطريقة الأولى: باستخدام Python
python -c "
import sys
sys.path.insert(0, 'bayan')
from bayan import HybridLexer, HybridParser, HybridInterpreter

with open('myfile.by', 'r', encoding='utf-8') as f:
    code = f.read()

lexer = HybridLexer(code)
tokens = lexer.tokenize()
parser = HybridParser(tokens)
ast = parser.parse()
interpreter = HybridInterpreter()
interpreter.interpret(ast)
"
```

#### 2. تشغيل كود مباشر:

```python
import sys
sys.path.insert(0, 'bayan')
from bayan import HybridLexer, HybridParser, HybridInterpreter

code = """
hybrid {
    x = 10
    y = 20
    print(x + y)
}
"""

lexer = HybridLexer(code)
tokens = lexer.tokenize()
parser = HybridParser(tokens)
ast = parser.parse()
interpreter = HybridInterpreter()
interpreter.interpret(ast)
```

#### 3. الوضع التفاعلي (REPL):

```python
# يمكن إنشاء REPL بسيط
import sys
sys.path.insert(0, 'bayan')
from bayan import HybridLexer, HybridParser, HybridInterpreter

interpreter = HybridInterpreter()

while True:
    try:
        code = input("bayan> ")
        if code.strip() in ['exit', 'quit']:
            break
        
        lexer = HybridLexer(code)
        tokens = lexer.tokenize()
        parser = HybridParser(tokens)
        ast = parser.parse()
        result = interpreter.interpret(ast)
        
        if result is not None:
            print(result)
    except Exception as e:
        print(f"Error: {e}")
```

---

## طرق الاستخدام

### 📄 1. ملفات البيان (`.by`)

احفظ الكود في ملف بامتداد `.by`:

```bayan
# myprogram.by
hybrid {
    print("مرحباً بك في لغة البيان")
    
    x = 10
    y = 20
    print(x + y)
}
```

### 📦 2. استخراج ملف تنفيذي

يمكنك استخدام **PyInstaller** لإنشاء ملف تنفيذي:

```bash
# 1. تثبيت PyInstaller
pip install pyinstaller

# 2. إنشاء ملف Python wrapper
# bayan_runner.py
import sys
sys.path.insert(0, 'bayan')
from bayan import HybridLexer, HybridParser, HybridInterpreter

def main():
    if len(sys.argv) < 2:
        print("Usage: bayan_runner <file.by>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        code = f.read()
    
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)

if __name__ == '__main__':
    main()

# 3. إنشاء الملف التنفيذي
pyinstaller --onefile bayan_runner.py

# 4. التشغيل
./dist/bayan_runner myprogram.by
```

---

## التكامل مع Python

### 🔗 1. استخدام لغة البيان من Python

```python
import sys
sys.path.insert(0, 'bayan')
from bayan import HybridLexer, HybridParser, HybridInterpreter

# تشغيل كود البيان
def run_bayan_code(code):
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    return interpreter.interpret(ast)

# مثال
bayan_code = """
hybrid {
    x = 10
    y = 20
    result = x + y
}
"""

run_bayan_code(bayan_code)
```

### 🔗 2. الوصول إلى متغيرات البيان من Python

```python
import sys
sys.path.insert(0, 'bayan')
from bayan import HybridLexer, HybridParser, HybridInterpreter

code = """
hybrid {
    name = "أحمد"
    age = 25
    scores = [85, 90, 88]
}
"""

lexer = HybridLexer(code)
tokens = lexer.tokenize()
parser = HybridParser(tokens)
ast = parser.parse()
interpreter = HybridInterpreter()
interpreter.interpret(ast)

# الوصول إلى المتغيرات
name = interpreter.traditional.global_env['name']
age = interpreter.traditional.global_env['age']
scores = interpreter.traditional.global_env['scores']

print(f"Name: {name}, Age: {age}, Scores: {scores}")
```

### 🔗 3. استدعاء دوال Python من البيان

حالياً، يمكنك استخدام الدوال المدمجة في Python. لإضافة دوال مخصصة:

```python
import sys
sys.path.insert(0, 'bayan')
from bayan import HybridInterpreter

# إنشاء interpreter
interpreter = HybridInterpreter()

# إضافة دالة Python مخصصة
def my_custom_function(x, y):
    return x * y + 10

interpreter.traditional.global_env['custom_func'] = my_custom_function

# الآن يمكن استخدامها في كود البيان
# (يجب تشغيل الكود من خلال هذا الـ interpreter)
```

---

## أمثلة سريعة

### مثال 1: Hello World

```bayan
hybrid {
    print("Hello, World!")
    print("مرحباً بالعالم!")
}
```

### مثال 2: حساب المجموع

```bayan
hybrid {
    def calculate_sum(a, b): {
        return a + b
    }
    
    result = calculate_sum(10, 20)
    print(result)  # 30
}
```

### مثال 3: صنف بسيط

```bayan
hybrid {
    class Student: {
        def __init__(self, name, grade): {
            self.name = name
            self.grade = grade
        }
        
        def display(self): {
            print(self.name)
            print(self.grade)
        }
    }
    
    student = Student("محمد", 95)
    student.display()
}
```

### مثال 4: برمجة منطقية

```bayan
hybrid {
    # حقائق
    likes("أحمد", "برمجة").
    likes("فاطمة", "رياضيات").
    likes("علي", "برمجة").
    
    # استعلام
    results = query likes(?Person, "برمجة")?
    
    for result in results: {
        print(result["?Person"])
    }
}
```

---

## 📚 الخطوات التالية

الآن بعد أن تعرفت على لغة البيان، انتقل إلى:

- **[الجزء الثاني: البرمجة الإجرائية والكائنية](02_PROCEDURAL_OOP_AR.md)** - دليل شامل من المبتدئ إلى المحترف
- **[الجزء الثالث: البرمجة المنطقية](03_LOGIC_PROGRAMMING_AR.md)** - دليل البرمجة المنطقية الكامل

---

## 🆘 الدعم والمساعدة

- **الوثائق**: `docs/` folder
- **الأمثلة**: `examples/` folder
- **الاختبارات**: `tests/` folder

---

**لغة البيان - لغة برمجة عربية ثورية! 🚀**

</div>

