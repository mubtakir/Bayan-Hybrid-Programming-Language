# البدء السريع - Quick Start Guide
## لغة البيان - Bayan Programming Language

---

## 🚀 البدء في 5 دقائق | Get Started in 5 Minutes

---

## الخطوة 1: التحقق من المتطلبات | Step 1: Check Requirements

### المتطلبات | Requirements
- Python 3.8 أو أحدث
- pytest (للاختبارات فقط)

### التحقق | Verification
```bash
python3 --version
# يجب أن يكون 3.8 أو أحدث
```

---

## الخطوة 2: تشغيل الاختبارات | Step 2: Run Tests

```bash
cd bayan_python/bayan
python -m pytest tests/ -v
```

### النتيجة المتوقعة | Expected Output
```
======================== 79 passed in X.XXs ========================
```

✅ إذا رأيت هذه الرسالة، فكل شيء يعمل بشكل صحيح!

---

## الخطوة 3: تجربة الأمثلة | Step 3: Try Examples

### مثال 1: البرمجة المنطقية (العائلة)
```bash
cd bayan_python/bayan
python main.py examples/family.by
```

**ماذا يفعل؟**
- يعرّف علاقات عائلية (أب، أم، أخ، أخت)
- يستخدم قواعد منطقية للاستدلال
- يستعلم عن العلاقات

### مثال 2: البرمجة الكائنية (الآلة الحاسبة)
```bash
cd bayan_python/bayan
python main.py examples/calculator.by
```

**ماذا يفعل؟**
- يعرّف فئة Calculator
- يستخدم الوراثة
- يطبق البرمجة الكائنية

### مثال 3: الوضع التفاعلي
```bash
cd bayan_python/bayan
python main.py
```

**جرب هذا الكود:**
```bayan
# البرمجة الإجرائية
x = 10
y = 20
print(x + y)

# البرمجة الكائنية
class Person:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        print("مرحباً، أنا", self.name)

person = Person("أحمد")
person.greet()

# البرمجة المنطقية
hybrid {
    fact likes(ahmad, programming).
    fact likes(fatima, math).
    
    rule smart(?X) :- likes(?X, programming).
}

query smart(?Who)?
```

---

## الخطوة 4: كتابة برنامجك الأول | Step 4: Write Your First Program

### إنشاء ملف جديد
```bash
cd bayan_python/bayan
nano my_first_program.by
```

### مثال بسيط: حساب الأعداد الأولية
```bayan
# برنامج لحساب الأعداد الأولية
# Prime numbers calculator

def is_prime(n):
    """تحقق إذا كان العدد أولياً"""
    if n < 2:
        return False
    
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    
    return True

# طباعة الأعداد الأولية من 1 إلى 50
print("الأعداد الأولية من 1 إلى 50:")
for num in range(1, 51):
    if is_prime(num):
        print(num, end=" ")

print()  # سطر جديد
```

### تشغيل البرنامج
```bash
python main.py my_first_program.by
```

---

## الخطوة 5: استكشاف المزيد | Step 5: Explore More

### قراءة التوثيق | Read Documentation
```bash
# الأساسيات
cat docs/basics.md

# المرجع الكامل
cat docs/reference.md

# البنية المعمارية
cat docs/architecture.md
```

### تجربة الحلول المتقدمة | Try Advanced Solutions
```bash
# معادلات لغوية
python main.py bayan_solutions/linguistic_equations.by

# استدلال منطقي
python main.py bayan_solutions/logical_inference.by

# معالجة الأحداث
python main.py bayan_solutions/event_processing.by
```

---

## 📚 أمثلة سريعة | Quick Examples

### 1. البرمجة الإجرائية | Imperative Programming

```bayan
# المتغيرات والعمليات
x = 10
y = 20
z = x + y
print("المجموع:", z)

# الحلقات
for i in range(5):
    print("العدد:", i)

# الشروط
if x > 5:
    print("x أكبر من 5")
else:
    print("x أصغر من أو يساوي 5")

# الدوال
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

print("5! =", factorial(5))
```

### 2. البرمجة الكائنية | Object-Oriented Programming

```bayan
# تعريف فئة
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        print(self.name, "يصدر صوتاً")

# الوراثة
class Dog(Animal):
    def speak(self):
        print(self.name, "ينبح: نباح!")

class Cat(Animal):
    def speak(self):
        print(self.name, "يموء: مواء!")

# استخدام الفئات
dog = Dog("كلب")
cat = Cat("قطة")

dog.speak()
cat.speak()
```

### 3. البرمجة المنطقية | Logic Programming

```bayan
hybrid {
    # حقائق عن الحيوانات
    fact animal(dog).
    fact animal(cat).
    fact animal(bird).
    
    fact has_legs(dog, 4).
    fact has_legs(cat, 4).
    fact has_legs(bird, 2).
    
    fact can_fly(bird).
    
    # قاعدة: الحيوان ثديي إذا كان له 4 أرجل ولا يطير
    rule mammal(?X) :- 
        animal(?X), 
        has_legs(?X, 4), 
        not can_fly(?X).
}

# استعلام: ما هي الثدييات؟
print("الثدييات:")
results = query mammal(?M)?
for result in results:
    print("-", result["?M"])
```

### 4. البرمجة الهجينة | Hybrid Programming

```bayan
# دمج البرمجة التقليدية مع المنطقية

# تعريف فئة Student
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def info(self):
        print("الطالب:", self.name, "- العمر:", self.age)

# إنشاء طلاب
ahmad = Student("أحمد", 20)
fatima = Student("فاطمة", 19)
ali = Student("علي", 21)

# استخدام البرمجة المنطقية لتعريف العلاقات
hybrid {
    fact student(ahmad).
    fact student(fatima).
    fact student(ali).
    
    fact enrolled(ahmad, "رياضيات").
    fact enrolled(ahmad, "فيزياء").
    fact enrolled(fatima, "رياضيات").
    fact enrolled(fatima, "كيمياء").
    fact enrolled(ali, "فيزياء").
    
    rule classmates(?S1, ?S2) :- 
        enrolled(?S1, ?Course), 
        enrolled(?S2, ?Course), 
        ?S1 != ?S2.
}

# استخدام البرمجة التقليدية للمعالجة
print("الزملاء في الصف:")
results = query classmates(?A, ?B)?
for result in results:
    student1 = result["?A"]
    student2 = result["?B"]
    student1.info()
    student2.info()
    print("---")
```

---

## 🎯 نصائح سريعة | Quick Tips

### 1. الكلمات المفتاحية العربية | Arabic Keywords
```bayan
# يمكنك استخدام الكلمات المفتاحية بالعربية
صنف شخص:
    دالة __init__(الذات، الاسم):
        الذات.الاسم = الاسم
    
    دالة تحية(الذات):
        اطبع("مرحباً،", الذات.الاسم)

شخص1 = شخص("أحمد")
شخص1.تحية()
```

### 2. التعليقات | Comments
```bayan
# تعليق سطر واحد

"""
تعليق متعدد الأسطر
يمكن أن يمتد على عدة أسطر
"""
```

### 3. معالجة الأخطاء | Error Handling
```bayan
try:
    x = 10 / 0
except ZeroDivisionError:
    print("خطأ: القسمة على صفر!")
```

### 4. القوائم والقواميس | Lists and Dictionaries
```bayan
# قوائم
numbers = [1, 2, 3, 4, 5]
print(numbers[0])  # 1

# قواميس
person = {"name": "أحمد", "age": 25}
print(person["name"])  # أحمد
```

---

## 🔍 استكشاف الأخطاء | Troubleshooting

### المشكلة: الاختبارات لا تعمل
**الحل:**
```bash
# تثبيت pytest
pip install pytest

# تشغيل الاختبارات مرة أخرى
cd bayan_python/bayan
python -m pytest tests/ -v
```

### المشكلة: خطأ في الاستيراد
**الحل:**
```bash
# تأكد من أنك في المجلد الصحيح
cd bayan_python/bayan

# تشغيل البرنامج
python main.py examples/family.by
```

### المشكلة: خطأ في الترميز (Encoding)
**الحل:**
- تأكد من حفظ الملفات بترميز UTF-8
- استخدم محرر نصوص يدعم UTF-8

---

## 📖 المراجع السريعة | Quick References

### الملفات المهمة | Important Files
- **README.md** - الدليل الرئيسي
- **EVALUATION_GUIDE.md** - دليل التقييم
- **FILE_INDEX.md** - فهرس الملفات
- **docs/basics.md** - الأساسيات
- **docs/reference.md** - المرجع الكامل

### الأوامر المهمة | Important Commands
```bash
# تشغيل برنامج
python main.py <file.by>

# الوضع التفاعلي
python main.py

# تشغيل الاختبارات
python -m pytest tests/ -v

# تشغيل اختبار محدد
python -m pytest tests/test_oop.py -v
```

---

## 🎓 التعلم التدريجي | Progressive Learning

### المستوى 1: المبتدئ (1-2 ساعة)
1. اقرأ README.md
2. جرب الأمثلة الأساسية
3. اكتب برنامج بسيط

### المستوى 2: المتوسط (3-5 ساعات)
1. اقرأ docs/basics.md
2. جرب البرمجة الكائنية
3. جرب البرمجة المنطقية
4. اكتب برنامج متوسط

### المستوى 3: المتقدم (6-10 ساعات)
1. اقرأ docs/reference.md
2. اقرأ docs/architecture.md
3. جرب البرمجة الهجينة
4. ادرس الكود المصدري
5. اكتب برنامج متقدم

---

## ✅ الخطوات التالية | Next Steps

1. ✅ جرب جميع الأمثلة
2. ✅ اقرأ التوثيق الكامل
3. ✅ اكتب برامجك الخاصة
4. ✅ استكشف الكود المصدري
5. ✅ شارك تجربتك مع الآخرين

---

**مرحباً بك في عالم لغة البيان البرمجية!**

**Welcome to the world of Bayan programming language!**

---

**للمزيد من المعلومات، راجع README.md و EVALUATION_GUIDE.md**

**For more information, see README.md and EVALUATION_GUIDE.md**

