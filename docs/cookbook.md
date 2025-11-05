# Bayan Cookbook — وصفات عملية من المبتدئ إلى المتقدم

هذه الوصفات أمثلة قصيرة قابلة للنسخ واللصق للتعلّم السريع. إذا لم يكن لديك سطر أوامر لتشغيل ملفات .bayan بعد، يمكنك تشغيل الأمثلة من خلال بايثون باستخدام المكوّنات المضمّنة:

```python
from bayan.lexer import Lexer
from bayan.parser import HybridParser
from bayan.hybrid_interpreter import HybridInterpreter

def run(code, filename="<mem>"):
    toks = Lexer(code).tokenize()
    ast = HybridParser(toks, filename=filename).parse()
    intr = HybridInterpreter()
    intr.traditional.set_source(code, filename=filename)
    return intr.interpret(ast)
```

---

## 1) مرحبًا يا عالم
```bayan
print("Hello, Bayan!")
```

## 2) متغيرات وعملية حسابية
```bayan
x = 40
y = 2
print(x + y)   # 42
```

## 3) شرط if/elif/else
```bayan
n = 7
if n % 2 == 0:
{
    print("even")
}
elif n % 3 == 0:
{
    print("div by 3")
}
else:
{
    print("odd")
}
```

## 4) القوائم والحلقات
```bayan
nums = [1, 2, 3, 4]
for a in nums:
{
    print(a)
}
```

## 5) القواميس والتكرار
```bayan
m = { "a": 1, "b": 2 }
print(m["a"])   # 1
for k in ["a", "b"]:
{
    print(k)
}
```

## 6) الدوال
```bayan
def add(a, b):
{
    return a + b
}

print(add(10, 32))
```
ملاحظة: لا توجد معاملات افتراضية/مسماة حاليًا.

## 7) الأصناف والكائنات
```bayan
class Counter:
{
    def __init__(): { self.value = 0 }
    def inc(): { self.value = self.value + 1 }
    def get(): { return self.value }
}

c = Counter()
c.inc()
print(c.get())   # 1
```

## 8) الوراثة وsuper()
```bayan
class A:
{
    def greet(): { print("A") }
}

class B(A):
{
    def greet():
    {
        super().greet()   # يستدعي A.greet
        print("B")
    }
}

b = B()
b.greet()
# المخرجات:
# A
# B
```

## 9) تحميل وحدات بيان
ملف mymod.bayan:
```bayan
def mul(a, b): { return a * b }
```
الاستعمال:
```bayan
import mymod
print(mymod.mul(6, 7))   # 42
```

## 10) استيراد من بايثون (عند الإتاحة)
```bayan
import math
print(math.sqrt(49))
```
قد يتطلب الأمر ضبط قائمة سماح آمنة للاستيراد من بايثون.

## 11) الدوال السحرية — تعريف سلوك خاص
```bayan
class Vec2:
{
    def __init__(): { self.x = 0; self.y = 0 }
    def __repr__(): { return "<Vec2>" }
    def __add__(other): { return self.x + self.y + other }
}

v = Vec2()
print(repr(v))        # <Vec2>
print(v + 10)         # يستدعي __add__
```

## 12) العضوية والفهرسة
```bayan
class Bag:
{
    def __init__(): { self.data = [1, 2, 3] }
    def __contains__(x): { return x in self.data }
    def __getitem__(i): { return self.data[i] }
}

b = Bag()
print(2 in b)     # True
print(b[1])       # 2
```

## 13) منطق هجيني سريع
```bayan
hybrid:
{
    fact parent(Ali, Omar).
    fact parent(Omar, Zaid).

    # جدّية: ancestor(X,Y) حين parent(X,Y) أو parent(X,Z) & ancestor(Z,Y)
    rule ancestor(X, Y) :- parent(X, Y).
    rule ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

    query ancestor(Ali, ?Who).
}
```
المفسّر سيُعيد نتائج الاستعلام (حسب آلية الإخراج الحالية في بيئتك).

## 14) إطار أخطاء ملوّن (اختياري)
عند إعداد المفسّر من بايثون:
```python
intr.traditional.set_error_formatting(colors=True, context_lines=1, tabstop=4)
```
ثم عند وجود خطأ ستظهر أسطر مرقّمة وسهم ^ عند العمود مع تلوين اختياري.

## 15) مشروع صغير: عدّاد مع مشغّلات
```bayan
class Counter:
{
    def __init__(): { self.v = 0 }
    def inc(): { self.v = self.v + 1 }
    def __repr__(): { return "Counter(" + self.v + ")" }
}

c = Counter()
for _ in [1, 2, 3]:
{
    c.inc()
}
print(repr(c))
```

انتهى.

