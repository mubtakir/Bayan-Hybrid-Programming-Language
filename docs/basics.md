# دليل أساسيات لغة بيان (Bayan) — Basics Guide

هذا الدليل يعطيك صورة عملية مختصرة عن أساسيات لغة «بيان»: البنية التقليدية (إجرائية/كائنية)، جزء المنطق (من نمط برولوغ)، والتكامل مع بايثون، مع أمثلة صغيرة جاهزة.

Contents (English)
- Getting started
- Syntax overview (values, variables, operators)
- Control flow (if, for, while, return)
- Functions and modules
- Classes, objects, inheritance (C3 MRO), super()
- Dunder methods (operators, containers, callables)
- Truthiness, iteration, membership
- Import system: Bayan modules + Python
- Hybrid logic: facts, rules, queries, hybrid { }
- Errors & debugging: stack + code frames (optional colors)

---

## البدء السريع (Getting started)

يمكن كتابة ملفات «بيان» بامتداد `.bayan` واستيرادها داخل برنامج أكبر، أو تشغيلها عبر مفسّر بايثون مضمّن في المستودع.

- ملف بسيط:
```bayan
# hello.bayan
print("مرحبا يا بيان")
```

- استيراده من «بيان» (ضمن مشروع واحد):
```bayan
import hello
```

- داخل الاختبارات/الأمثلة، تُستخدم الواجهة التالية في بايثون لتشغيل كود «بيان» الموجود كسلسلة نصية:
```python
from bayan import HybridLexer, HybridParser, HybridInterpreter
code = """
print("Hi")
"""
lexer = HybridLexer(code)
tokens = lexer.tokenize()
parser = HybridParser(tokens, filename="mem.by")
ast = parser.parse()
intr = HybridInterpreter()
# لإظهار إطار الشفرة في الأخطاء:
intr.traditional.set_source(code, filename="mem.by")
result = intr.interpret(ast)
```


## القيم والمتغيّرات (Values & Variables)

- الأعداد: `10`, `3.14`
- النصوص: `'مرحباً'`, `"hello"`
- المنطقية: `True`, `False`, والعدم: `None`
- القوائم: `[1, 2, 3]`
- القواميس: `{ "a": 1, "b": 2 }`
- المتغيّرات بأحرف لاتينية أو عربية: `س = 5`, `total = 42`

إسناد بسيط:
```bayan
x = 10
y = x + 2
```

الوصول بالفهارس (إن كان الكائن يدعم ذلك):
```bayan
xs = [10, 20, 30]
print(xs[0])
```

الوصول للخاصيات:
```bayan
obj.count = 0
obj.count = obj.count + 1
```


## العوامل (Operators)

- حسابية: `+ - * / %`
- مقارنة: `== != < <= > >=`
- منطقية: `and or not`
- العضوية: `in`

تُحاكي «بيان» دلالات بايثون وتدعم التحميل الزائد عبر دوال dunder (انظر أدناه).


## التدفق والتحكّم (Control Flow)

شرطية if/elif/else:
```bayan
if x > 10:
{
    print("كبير")
}
elif x == 10:
{
    print("عشرة")
}
else:
{
    print("صغير")
}
```

تكرار for (يدعم أي قابل للتكرار):
```bayan
for i in xs:
{
    print(i)
}
```

تكرار while:
```bayan
while x > 0:
{
    x = x - 1
}
```

إرجاع من دالة: `return expr`، وكذلك `break` و`continue` داخل الحلقات.


## الدوال (Functions)

تعريف واستدعاء:
```bayan
def add(a, b):
{
    return a + b
}

result = add(2, 3)
```

الطباعة:
```bayan
print("value:", 42)
```

الاستيراد:
```bayan
import my_package.utils as utils
from my_package.math import add, sub
```


## الصفوف والكائنات والوراثة (Classes, Objects, Inheritance)

تعريف صف بسيط:
```bayan
class Counter:
{
    def __init__(): { self.value = 0 }
    def inc():      { self.value = self.value + 1 }
    def get():      { return self.value }
}

c = Counter()
c.inc()
print(c.get())
```

وراثة مفردة أو متعددة (C3 MRO):
```bayan
class A: { def ping(): { print("A") } }
class B: { def ping(): { print("B") } }
class C(A, B): { }

C().ping()   # يتحلّى عبر MRO
```

super():
```bayan
class Base:
{
    def f(): { print("Base") }
}
class Child(Base):
{
    def f(): { super().f(); print("Child") }
}
Child().f()
```

سمات ودوال خاصّة (dunder) مدعومة لكتابة صنف يُعامل كالأعداد/الحاويات/الدوال.


## دوال dunder (تحميل زائد للسلوك)

- حسابية/مقارنات: `__add__`, `__sub__`, `__mul__`, `__truediv__`, `__mod__`, `__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__`, `__neg__`
- تمثيل نصي: `__repr__`
- منطقية/الطول: `__bool__`, `__len__`
- فهارس: `__getitem__`, `__setitem__`
- عضوية: `__contains__` (لعامل `in`)
- تكرار: `__iter__` (يُتوقع أن يُعيد قابل تكرار)
- قابل للاستدعاء: `__call__`

مثال مختصر:
```bayan
class Box:
{
    def __init__(): { self.data = [1,2,3] }
    def __len__():  { return 3 }
    def __getitem__(i): { return self.data[i] }
    def __contains__(x): { return x in self.data }
    def __repr__(): { return "<Box>" }
}

b = Box()
print(len(b))     # 3
print(b[0])       # 1
print(2 in b)     # True
print(repr(b))    # <Box>
```


## الحقيقة/العضوية/التكرار (Truthiness, Membership, Iteration)

- الحقيقة (if/while/not) تستخدم `__bool__` أو بديله `__len__` إن وُجد على كائنات «بيان».
- `in` يستخدم `__contains__` إن وُجد.
- `for` يعتمد `__iter__` إن كان الكائن من «بيان».


## نظام الاستيراد (Import System)

- أولاً يحاول استيراد وحدة «بيان» (`.bayan`) وفق مسارات البحث (المجلد الحالي، tests/، وغيرها حسب الإعداد).
- إن فشل، يعود للاستيراد الآمن من بايثون (بحسب لائحة السماح في ImportSystem).

أمثلة:
```bayan
import mypkg.m1 as m1
from mypkg.m2 import add
x = add(1, 2)
y = m1.make()
```

ملاحظة: وحدات «بيان» تُخزَّن في ذاكرة مؤقتة لمنع التحميل المتكرر.


## المنطق الهجين (Hybrid Logic)

يمكنك كتابة كتلة هجينة تجمع التقليدي والمنطقي:
```bayan
hybrid {
    # تصريحات تقليدية ممكنة هنا

    fact parent(Ali, Omar).
    fact parent(Omar, Lina).

    # قاعدة: الجدّ
    rule grandparent(X, Z) :- parent(X, Y), parent(Y, Z).

    # استعلام
    query grandparent(Ali, ?Who).
}
```
- الحقائق (facts) تنتهي بنقطة.
- القواعد (rules) تستخدم `:-` أو `←` بين الرأس والجسم.
- المتغيّرات المنطقية تسبقها `?` مثل `?X`.
- الاستعلام query يعيد حلولًا (في وضع الاختبار تُحوَّل لقوائم قواميس).


## الأخطاء والتنقيح (Errors & Debugging)

- أي خطأ يُغلّف برسالة تتضمن "Bayan stack" مع نوع العقد ووضعها `اسم_العقدة@الملف:السطر:العمود`.
- يمكن إظهار "إطار الشفرة" (code frame) مع ترقيم أسطر وسهم عند العمود:
  - وفِّر المصدر للمفسّر: `set_source(code, filename="mem.by")`
  - تفعيل التلوين والسياق:
```python
intr.traditional.set_error_formatting(colors=True, context_lines=1, tabstop=4)
```
المخرجات (مثال):
```
NameError: Undefined variable: b
Bayan stack: Assignment@mem.by:1:5 -> BinaryOp@mem.by:1:11 -> Variable@mem.by:1:9

File mem.by:1:9
>1 |     a = b + 1
             ^
 2 |     
```
- المؤشر (^) يحترم المحارف الواسعة والتبويبات عبر حساب عرض العرض.
- أسماء غير معرّفة تُقترح لها بدائل "Did you mean:" باستخدام مسافة Levenshtein مقابل رموز البيئة الحالية (المحلية/العامة + الدوال + الصفوف).


## تكامل بايثون (Python Interop)

- `import math` أو وحدات بايثون المسموحة.
- يمكنك استخدام الكائنات البايثونية جنبًا إلى جنب مع كائنات «بيان». بعض السلوكيات كالحقيقة/التكرار تتبع بايثون افتراضيًا، بينما كائنات «بيان» لها dunder خاصة بها عند توفرها.


## أفضل الممارسات (Best Practices)

- قسّم مشروعك إلى وحدات «بيان» صغيرة (`.bayan`) واستخدم `import`/`from`.
- عند كتابة صفوف مخصّصة، وفّر dunder المناسبة حسب السلوك (قابلية التكرار، الفهرسة...).
- عند مواجهة خطأ، فعّل إطارات الشفرة والألوان لتحصل على تشخيص أوضح.
- استخدم `super()` مع الوراثة لضمان احترام C3 MRO.


## ملاحظات
- المعرفات تدعم العربية واللاتينية: `[a-zA-Z_\u0600-\u06FF][a-zA-Z0-9_\u0600-\u06FF]*`
- الكتل تُكتب بأقواس معقوفة `{ ... }` مع `:` بعد عناوين البُنى (class/def/if/for/while).
- المنطق: facts/rules/queries داخل `hybrid { }` أو كتصريحات علوية عند الحاجة.

انتهى — هذا الدليل مختصر، وسيُستكمل لاحقًا بدليل مرجعي شامل وأمثلة موسّعة.

