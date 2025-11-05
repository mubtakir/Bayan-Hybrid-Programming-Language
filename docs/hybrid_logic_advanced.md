# المنطق الهجين المتقدم (Advanced Hybrid Logic)

دليل متقدم للعمل مع المنطق الهجين في لغة بيان.

---

## 1. أساسيات المنطق الهجين

### الحقائق (Facts):
```bayan
hybrid {
    # حقيقة بسيطة
    fact parent(Ali, Omar).
    
    # حقائق متعددة
    fact parent(Omar, Lina).
    fact parent(Fatima, Lina).
    
    # حقائق مع أنواع مختلفة
    fact age(Ali, 50).
    fact city(Ali, "Cairo").
}
```

### القواعد (Rules):
```bayan
hybrid {
    # قاعدة بسيطة
    rule grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
    
    # قاعدة مع شروط متعددة
    rule ancestor(X, Y) :- parent(X, Y).
    rule ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
    
    # قاعدة مع عمليات حسابية
    rule adult(X) :- age(X, Age), Age >= 18.
}
```

### الاستعلامات (Queries):
```bayan
hybrid {
    fact parent(Ali, Omar).
    fact parent(Omar, Lina).
    
    rule grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
    
    # استعلام بسيط
    query parent(Ali, ?Who).
    
    # استعلام مع متغيرات متعددة
    query grandparent(?GP, ?GC).
}
```

---

## 2. المتغيرات المنطقية (Logic Variables)

### التعريف:
```bayan
hybrid {
    fact parent(Ali, Omar).
    
    # متغير واحد
    query parent(Ali, ?Child).
    
    # متغيرات متعددة
    query parent(?Parent, ?Child).
    
    # متغيرات مع ثوابت
    query parent(?X, Omar).
}
```

### الاستخدام:
```bayan
hybrid {
    fact likes(Ali, "Coffee").
    fact likes(Ali, "Tea").
    fact likes(Fatima, "Coffee").
    
    # البحث عن كل ما يحبه علي
    query likes(Ali, ?Thing).
    
    # البحث عن كل من يحب القهوة
    query likes(?Person, "Coffee").
}
```

---

## 3. القواعد المعقدة (Complex Rules)

### التكرار (Recursion):
```bayan
hybrid {
    fact parent(Ali, Omar).
    fact parent(Omar, Lina).
    fact parent(Lina, Zaid).
    
    # قاعدة تكرارية للأسلاف
    rule ancestor(X, Y) :- parent(X, Y).
    rule ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
    
    # استعلام عن جميع الأسلاف
    query ancestor(Ali, ?Descendant).
}
```

### القواعد المتعددة:
```bayan
hybrid {
    fact parent(Ali, Omar).
    fact parent(Omar, Lina).
    fact gender(Ali, male).
    fact gender(Omar, male).
    fact gender(Lina, female).
    
    # قاعدة الأب
    rule father(X, Y) :- parent(X, Y), gender(X, male).
    
    # قاعدة الأم
    rule mother(X, Y) :- parent(X, Y), gender(X, female).
    
    # قاعدة الأخ
    rule brother(X, Y) :- parent(P, X), parent(P, Y), gender(X, male).
    
    query father(Ali, ?Child).
    query mother(?M, Lina).
    query brother(?B, Lina).
}
```

---

## 4. الدمج مع البرمجة التقليدية

### استخدام المتغيرات:
```bayan
hybrid {
    fact person(Ali, 25).
    fact person(Omar, 30).
    fact person(Lina, 22).
    
    # متغير تقليدي
    min_age = 25
    
    # استعلام مع متغير
    query person(?Name, Age), Age >= min_age.
}
```

### الطباعة والنتائج:
```bayan
hybrid {
    fact parent(Ali, Omar).
    fact parent(Omar, Lina).
    
    rule grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
    
    print("=== الأجداد ===")
    query grandparent(?GP, ?GC).
    print("انتهى")
}
```

---

## 5. الحقائق الديناميكية (Dynamic Facts)

### إضافة حقائق أثناء التنفيذ:
```bayan
hybrid {
    fact person(Ali).
    fact person(Omar).
    
    # إضافة حقيقة جديدة
    # (هذه الميزة قد تحتاج إلى تطوير)
    
    query person(?Name).
}
```

---

## 6. الاستعلامات المتقدمة

### البحث عن كل الحلول:
```bayan
hybrid {
    fact color(red).
    fact color(green).
    fact color(blue).
    
    fact likes(Ali, red).
    fact likes(Ali, blue).
    fact likes(Fatima, green).
    
    # البحث عن كل الألوان
    query color(?C).
    
    # البحث عن كل ما يحبه علي
    query likes(Ali, ?Thing).
}
```

### الاستعلامات المشروطة:
```bayan
hybrid {
    fact age(Ali, 25).
    fact age(Omar, 17).
    fact age(Lina, 30).
    
    # البحث عن البالغين
    query age(?Name, Age), Age >= 18.
}
```

---

## 7. أفضل الممارسات

### تنظيم الحقائق:
```bayan
hybrid {
    # حقائق الأشخاص
    fact person(Ali).
    fact person(Omar).
    fact person(Lina).
    
    # حقائق العلاقات
    fact parent(Ali, Omar).
    fact parent(Omar, Lina).
    
    # حقائق الخصائص
    fact age(Ali, 50).
    fact age(Omar, 25).
    
    # القواعس
    rule grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
    
    # الاستعلامات
    query grandparent(?GP, ?GC).
}
```

### تسمية واضحة:
```bayan
hybrid {
    # استخدم أسماء واضحة
    fact is_parent(Ali, Omar).
    fact is_child(Omar, Ali).
    
    # تجنب الأسماء الغامضة
    # fact p(Ali, Omar).
    # fact c(Omar, Ali).
}
```

---

## 8. الأخطاء الشائعة

### خطأ 1: نسيان النقطة:
```bayan
hybrid {
    # خطأ
    fact parent(Ali, Omar)
    
    # صحيح
    fact parent(Ali, Omar).
}
```

### خطأ 2: استخدام متغير بدون `?`:
```bayan
hybrid {
    fact parent(Ali, Omar).
    
    # خطأ
    query parent(Ali, Child).
    
    # صحيح
    query parent(Ali, ?Child).
}
```

### خطأ 3: عدم استخدام `:-` في القواعد:
```bayan
hybrid {
    fact parent(Ali, Omar).
    
    # خطأ
    rule grandparent(X, Z) parent(X, Y), parent(Y, Z).
    
    # صحيح
    rule grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
}
```

---

## 9. الميزات المخطط إضافتها

### 1. القيود (Constraints):
```bayan
# مخطط
hybrid {
    fact age(Ali, 25).
    
    # قيد: العمر يجب أن يكون موجباً
    constraint age(?Name, Age) :- Age > 0.
}
```

### 2. النفي (Negation):
```bayan
# مخطط
hybrid {
    fact parent(Ali, Omar).
    
    # قاعدة مع نفي
    rule orphan(X) :- person(X), not parent(?P, X).
}
```

### 3. القطع (Cut):
```bayan
# مخطط
hybrid {
    fact color(red).
    fact color(green).
    
    # قطع: توقف بعد أول حل
    query color(?C), !.
}
```

### 4. الدوال المنطقية:
```bayan
# مخطط
hybrid {
    fact number(1).
    fact number(2).
    
    # دالة منطقية
    rule is_even(X) :- X mod 2 == 0.
}
```

---

## 10. أمثلة عملية

### مثال 1: شجرة العائلة:
```bayan
hybrid {
    # الآباء
    fact parent(Ahmed, Ali).
    fact parent(Ahmed, Fatima).
    fact parent(Ali, Omar).
    fact parent(Ali, Lina).
    
    # الأجداد
    rule grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
    
    # الأعمام
    rule uncle(X, Y) :- parent(P, Y), parent(GP, P), parent(GP, X).
    
    print("=== الأجداد ===")
    query grandparent(?GP, ?GC).
    
    print("=== الأعمام ===")
    query uncle(?Uncle, ?Nephew).
}
```

### مثال 2: نظام التوصيات:
```bayan
hybrid {
    fact likes(Ali, "Coffee").
    fact likes(Ali, "Books").
    fact likes(Fatima, "Coffee").
    fact likes(Fatima, "Music").
    
    rule similar_taste(X, Y) :- likes(X, Z), likes(Y, Z), X != Y.
    
    print("=== من لديهم أذواق متشابهة ===")
    query similar_taste(?Person1, ?Person2).
}
```

---

**آخر تحديث:** 2024-10-23

