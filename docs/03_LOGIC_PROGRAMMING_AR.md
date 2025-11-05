# دليل لغة البيان - الجزء الثالث: البرمجة المنطقية
# Bayan Language Guide - Part 3: Logic Programming

<div dir="rtl">

## 📚 جدول المحتويات

### القسم الأول: الأساسيات (للمبتدئين)
1. [مقدمة في البرمجة المنطقية](#1-مقدمة-في-البرمجة-المنطقية)
2. [الحقائق (Facts)](#2-الحقائق-facts)
3. [الاستعلامات (Queries)](#3-الاستعلامات-queries)
4. [المتغيرات المنطقية](#4-المتغيرات-المنطقية)
5. [القواعد البسيطة (Rules)](#5-القواعد-البسيطة-rules)

### القسم الثاني: المستوى المتوسط
6. [القواعد المركبة](#6-القواعد-المركبة)
7. [العودية (Recursion)](#7-العودية-recursion)
8. [القوائم في البرمجة المنطقية](#8-القوائم-في-البرمجة-المنطقية)
9. [العمليات المنطقية](#9-العمليات-المنطقية)

### القسم الثالث: المستوى المتقدم
10. [Meta-predicates](#10-meta-predicates)
11. [قاعدة المعرفة الديناميكية](#11-قاعدة-المعرفة-الديناميكية)
12. [البرمجة الهجينة](#12-البرمجة-الهجينة)
13. [أمثلة متقدمة](#13-أمثلة-متقدمة)

---

# القسم الأول: الأساسيات

## 1. مقدمة في البرمجة المنطقية

### 1.1 ما هي البرمجة المنطقية؟

البرمجة المنطقية هي نمط برمجي يعتمد على:
- **الحقائق** (Facts): معلومات صحيحة
- **القواعد** (Rules): علاقات منطقية
- **الاستعلامات** (Queries): أسئلة نطرحها

### 1.2 الفرق بين البرمجة الإجرائية والمنطقية

**البرمجة الإجرائية:**
```bayan
hybrid {
    # نخبر الحاسوب "كيف" يفعل الشيء
    def is_parent(person1, person2): {
        if person1 == "أحمد" and person2 == "محمد": {
            return True
        }
        return False
    }
}
```

**البرمجة المنطقية:**
```bayan
hybrid {
    # نخبر الحاسوب "ماذا" نريد
    parent("أحمد", "محمد").
    
    # الحاسوب يستنتج الإجابة
    results = query parent("أحمد", ?X)?
}
```

---

## 2. الحقائق (Facts)

### 2.1 حقيقة بسيطة

```bayan
hybrid {
    # حقيقة: أحمد هو أب محمد
    parent("أحمد", "محمد").
    
    # حقيقة: محمد هو أب علي
    parent("محمد", "علي").
}
```

### 2.2 حقائق متعددة

```bayan
hybrid {
    # علاقات الأبوة
    parent("أحمد", "محمد").
    parent("أحمد", "فاطمة").
    parent("محمد", "علي").
    parent("محمد", "سارة").
    
    # الأعمار
    age("أحمد", 50).
    age("محمد", 25).
    age("علي", 5).
}
```

### 2.3 حقائق بأنواع مختلفة

```bayan
hybrid {
    # نصوص
    city("الرياض").
    city("جدة").
    
    # أرقام
    temperature("الرياض", 35).
    temperature("جدة", 32).
    
    # قيم منطقية
    is_capital("الرياض", True).
    is_capital("جدة", False).
}
```

---

## 3. الاستعلامات (Queries)

### 3.1 استعلام بسيط

```bayan
hybrid {
    # حقائق
    parent("أحمد", "محمد").
    parent("محمد", "علي").
    
    # استعلام: هل أحمد أب محمد؟
    results = query parent("أحمد", "محمد")?
    
    if len(results) > 0: {
        print("نعم، أحمد أب محمد")
    }
}
```

### 3.2 استعلام مع متغير

```bayan
hybrid {
    # حقائق
    parent("أحمد", "محمد").
    parent("أحمد", "فاطمة").
    
    # استعلام: من هم أبناء أحمد؟
    results = query parent("أحمد", ?Child)?
    
    for result in results: {
        child = result["?Child"]
        print(child)  # محمد، فاطمة
    }
}
```

### 3.3 استعلام مع متغيرات متعددة

```bayan
hybrid {
    # حقائق
    parent("أحمد", "محمد").
    parent("فاطمة", "سارة").
    
    # استعلام: من هم جميع الآباء والأبناء؟
    results = query parent(?Parent, ?Child)?
    
    for result in results: {
        parent_name = result["?Parent"]
        child_name = result["?Child"]
        print(parent_name)
        print(child_name)
    }
}
```

---

## 4. المتغيرات المنطقية

### 4.1 تعريف المتغيرات

في البرمجة المنطقية، المتغيرات تبدأ بـ `?`:

```bayan
hybrid {
    # ?X متغير
    # "أحمد" ثابت
    
    parent("أحمد", "محمد").
    
    results = query parent(?X, "محمد")?
    # ?X سيكون "أحمد"
}
```

### 4.2 متغيرات متعددة

```bayan
hybrid {
    likes("أحمد", "برمجة").
    likes("فاطمة", "رياضيات").
    likes("علي", "برمجة").
    
    # من يحب ماذا؟
    results = query likes(?Person, ?Thing)?
    
    for result in results: {
        person = result["?Person"]
        thing = result["?Thing"]
        print(person + " يحب " + thing)
    }
}
```

### 4.3 نفس المتغير في أماكن متعددة

```bayan
hybrid {
    likes("أحمد", "برمجة").
    likes("أحمد", "رياضيات").
    likes("فاطمة", "برمجة").
    
    # من يحب البرمجة؟
    results = query likes(?Person, "برمجة")?
    
    for result in results: {
        print(result["?Person"])  # أحمد، فاطمة
    }
}
```

---

## 5. القواعد البسيطة (Rules)

### 5.1 قاعدة بسيطة

```bayan
hybrid {
    # حقائق
    parent("أحمد", "محمد").
    parent("محمد", "علي").
    
    # قاعدة: X جد Z إذا كان X أب Y و Y أب Z
    grandparent(?X, ?Z) :- parent(?X, ?Y), parent(?Y, ?Z).
    
    # استعلام
    results = query grandparent(?GP, "علي")?
    
    for result in results: {
        print(result["?GP"])  # أحمد
    }
}
```

### 5.2 قاعدة مع شرط واحد

```bayan
hybrid {
    # حقائق
    male("أحمد").
    male("محمد").
    female("فاطمة").
    
    parent("أحمد", "محمد").
    parent("أحمد", "فاطمة").
    
    # قاعدة: X أب Y إذا كان X ذكر و X والد Y
    father(?X, ?Y) :- male(?X), parent(?X, ?Y).
    
    # استعلام
    results = query father(?F, "محمد")?
    
    for result in results: {
        print(result["?F"])  # أحمد
    }
}
```

### 5.3 قواعد متعددة

```bayan
hybrid {
    # حقائق
    male("أحمد").
    male("محمد").
    female("فاطمة").
    female("سارة").
    
    parent("أحمد", "محمد").
    parent("أحمد", "فاطمة").
    
    # قواعد
    father(?X, ?Y) :- male(?X), parent(?X, ?Y).
    mother(?X, ?Y) :- female(?X), parent(?X, ?Y).
    
    # استعلامات
    fathers = query father(?F, ?C)?
    mothers = query mother(?M, ?C)?
    
    print("الآباء:")
    for result in fathers: {
        print(result["?F"])
    }
    
    print("الأمهات:")
    for result in mothers: {
        print(result["?M"])
    }
}
```

---

# القسم الثاني: المستوى المتوسط

## 6. القواعد المركبة

### 6.1 قاعدة بشروط متعددة

```bayan
hybrid {
    # حقائق
    parent("أحمد", "محمد").
    parent("فاطمة", "محمد").
    parent("محمد", "علي").
    
    male("أحمد").
    male("محمد").
    female("فاطمة").
    
    # قاعدة: X جد Y إذا كان X ذكر و X جد Y
    grandfather(?X, ?Z) :- male(?X), parent(?X, ?Y), parent(?Y, ?Z).
    
    results = query grandfather(?GF, "علي")?
    
    for result in results: {
        print(result["?GF"])  # أحمد
    }
}
```

### 6.2 قواعد متداخلة

```bayan
hybrid {
    # حقائق
    parent("أحمد", "محمد").
    parent("محمد", "علي").
    parent("علي", "حسن").
    
    # قواعد
    grandparent(?X, ?Z) :- parent(?X, ?Y), parent(?Y, ?Z).
    great_grandparent(?X, ?W) :- parent(?X, ?Y), grandparent(?Y, ?W).
    
    # استعلام
    results = query great_grandparent(?GGP, "حسن")?
    
    for result in results: {
        print(result["?GGP"])  # أحمد
    }
}
```

### 6.3 قواعد مع OR

```bayan
hybrid {
    # حقائق
    parent("أحمد", "محمد").
    parent("فاطمة", "سارة").
    
    # قاعدة: X قريب Y إذا كان X والد Y أو Y والد X
    related(?X, ?Y) :- parent(?X, ?Y).
    related(?X, ?Y) :- parent(?Y, ?X).
    
    results = query related("أحمد", ?R)?
    
    for result in results: {
        print(result["?R"])
    }
}
```

---

## 7. العودية (Recursion)

### 7.1 عودية بسيطة - الأسلاف

```bayan
hybrid {
    # حقائق
    parent("أحمد", "محمد").
    parent("محمد", "علي").
    parent("علي", "حسن").
    
    # قاعدة عودية: X سلف Y
    ancestor(?X, ?Y) :- parent(?X, ?Y).
    ancestor(?X, ?Z) :- parent(?X, ?Y), ancestor(?Y, ?Z).
    
    # استعلام: من هم أسلاف حسن؟
    results = query ancestor(?A, "حسن")?
    
    for result in results: {
        print(result["?A"])  # علي، محمد، أحمد
    }
}
```

### 7.2 عودية - حساب العدد

```bayan
hybrid {
    # حقيقة: 0 عدد
    number(0).
    
    # قاعدة عودية: إذا كان N عدد، فإن N+1 عدد
    number(?N1) :- number(?N), ?N1 = ?N + 1, ?N < 10.
    
    # استعلام
    results = query number(?N)?
    
    for result in results: {
        print(result["?N"])  # 0, 1, 2, ..., 10
    }
}
```

---

## 8. القوائم في البرمجة المنطقية

### 8.1 قوائم بسيطة

```bayan
hybrid {
    # حقيقة بقائمة
    scores("أحمد", [85, 90, 88]).
    scores("فاطمة", [92, 95, 89]).
    
    # استعلام
    results = query scores("أحمد", ?Scores)?
    
    for result in results: {
        scores_list = result["?Scores"]
        print(scores_list)  # [85, 90, 88]
    }
}
```

### 8.2 عضو في قائمة

```bayan
hybrid {
    # قاعدة: X عضو في قائمة
    member(?X, [?X | ?Tail]).
    member(?X, [?Head | ?Tail]) :- member(?X, ?Tail).
    
    # استعلام
    results = query member(2, [1, 2, 3])?
    
    if len(results) > 0: {
        print("2 موجود في القائمة")
    }
}
```

### 8.3 طول القائمة

```bayan
hybrid {
    # قاعدة: طول قائمة فارغة = 0
    list_length([], 0).
    
    # قاعدة عودية: طول قائمة = 1 + طول الباقي
    list_length([?H | ?T], ?N) :- list_length(?T, ?N1), ?N = ?N1 + 1.
    
    # استعلام
    results = query list_length([1, 2, 3, 4], ?Len)?
    
    for result in results: {
        print(result["?Len"])  # 4
    }
}
```

---

## 9. العمليات المنطقية

### 9.1 AND (,)

```bayan
hybrid {
    # حقائق
    student("أحمد").
    student("فاطمة").
    
    grade("أحمد", 85).
    grade("فاطمة", 92).
    
    # استعلام: طلاب بدرجة أكبر من 80
    results = query student(?S), grade(?S, ?G), ?G > 80?
    
    for result in results: {
        print(result["?S"])
    }
}
```

### 9.2 OR (;)

```bayan
hybrid {
    # حقائق
    likes("أحمد", "برمجة").
    likes("فاطمة", "رياضيات").
    
    # قاعدة: X يحب علوم إذا كان يحب برمجة أو رياضيات
    likes_science(?X) :- likes(?X, "برمجة"); likes(?X, "رياضيات").
    
    results = query likes_science(?Person)?
    
    for result in results: {
        print(result["?Person"])
    }
}
```

### 9.3 NOT

```bayan
hybrid {
    # حقائق
    student("أحمد").
    student("فاطمة").
    student("علي").
    
    passed("أحمد").
    passed("فاطمة").
    
    # قاعدة: X راسب إذا كان طالب ولم ينجح
    failed(?X) :- student(?X), not(passed(?X)).
    
    results = query failed(?S)?
    
    for result in results: {
        print(result["?S"])  # علي
    }
}
```

---

# القسم الثالث: المستوى المتقدم

## 10. Meta-predicates

### 10.1 findall/3

`findall/3` يجمع جميع الحلول في قائمة:

```bayan
hybrid {
    # حقائق
    score("أحمد", 85).
    score("فاطمة", 92).
    score("علي", 78).
    score("سارة", 95).
    
    # جمع جميع الدرجات
    results = query findall(?Score, score(?Name, ?Score), ?AllScores)?
    
    for result in results: {
        all_scores = result["?AllScores"]
        print(all_scores)  # [85, 92, 78, 95]
    }
}
```

### 10.2 findall مع شرط

```bayan
hybrid {
    # حقائق
    score("أحمد", 85).
    score("فاطمة", 92).
    score("علي", 78).
    score("سارة", 95).
    
    # جمع الدرجات الأكبر من 80
    goal = score(?Name, ?Score), ?Score > 80
    results = query findall(?Score, goal, ?HighScores)?
    
    for result in results: {
        high_scores = result["?HighScores"]
        print(high_scores)  # [85, 92, 95]
    }
}
```

### 10.3 bagof/3

`bagof/3` مثل `findall` لكنه يفشل إذا لم توجد حلول:

```bayan
hybrid {
    # حقائق
    class_member("أحمد", "class_a").
    class_member("فاطمة", "class_a").
    class_member("علي", "class_b").
    
    score("أحمد", 85).
    score("فاطمة", 92).
    score("علي", 78).
    
    # جمع درجات class_a
    goal = class_member(?Name, "class_a"), score(?Name, ?Score)
    results = query bagof(?Score, goal, ?Scores)?
    
    for result in results: {
        scores = result["?Scores"]
        print(scores)  # [85, 92]
    }
}
```

### 10.4 setof/3

`setof/3` يجمع حلول فريدة ومرتبة:

```bayan
hybrid {
    # حقائق
    likes("أحمد", "برمجة").
    likes("فاطمة", "برمجة").
    likes("علي", "رياضيات").
    likes("سارة", "برمجة").
    
    # جمع المواد المحبوبة (بدون تكرار)
    results = query setof(?Subject, likes(?Person, ?Subject), ?Subjects)?
    
    for result in results: {
        subjects = result["?Subjects"]
        print(subjects)  # ["برمجة", "رياضيات"]
    }
}
```

---

## 11. قاعدة المعرفة الديناميكية

### 11.1 assertz - إضافة حقيقة في النهاية

```bayan
hybrid {
    # حقائق أولية
    student("أحمد").
    student("فاطمة").
    
    # إضافة طالب جديد
    assertz(student("علي"))
    
    # استعلام
    results = query student(?S)?
    
    for result in results: {
        print(result["?S"])  # أحمد، فاطمة، علي
    }
}
```

### 11.2 asserta - إضافة حقيقة في البداية

```bayan
hybrid {
    # حقائق أولية
    priority("task2", 2).
    priority("task3", 3).
    
    # إضافة مهمة ذات أولوية عالية
    asserta(priority("task1", 1))
    
    # استعلام
    results = query priority(?Task, ?P)?
    
    for result in results: {
        print(result["?Task"])  # task1، task2، task3
    }
}
```

### 11.3 retract - حذف حقيقة

```bayan
hybrid {
    # حقائق
    student("أحمد").
    student("فاطمة").
    student("علي").
    
    # حذف طالب
    retract(student("فاطمة"))
    
    # استعلام
    results = query student(?S)?
    
    for result in results: {
        print(result["?S"])  # أحمد، علي
    }
}
```

### 11.4 retractall - حذف جميع الحقائق المطابقة

```bayan
hybrid {
    # حقائق
    temp_data("item1", 100).
    temp_data("item2", 200).
    temp_data("item3", 300).

    # حذف جميع البيانات المؤقتة
    retractall(temp_data(?X, ?Y))

    # استعلام
    results = query temp_data(?Item, ?Value)?

    print(len(results))  # 0
}
```

---

## 12. البرمجة الهجينة

### 12.1 دمج البرمجة الإجرائية والمنطقية

```bayan
hybrid {
    # الجزء المنطقي: قاعدة المعرفة
    parent("أحمد", "محمد").
    parent("محمد", "علي").

    grandparent(?X, ?Z) :- parent(?X, ?Y), parent(?Y, ?Z).

    # الجزء الإجرائي: معالجة النتائج
    results = query grandparent(?GP, "علي")?

    for result in results: {
        gp_name = result["?GP"]
        message = "الجد هو: " + gp_name
        print(message)
    }
}
```

### 12.2 استخدام OOP مع البرمجة المنطقية

```bayan
hybrid {
    # صنف لتمثيل شخص
    class Person: {
        def __init__(self, name, age): {
            self.name = name
            self.age = age
        }

        def display(self): {
            print(self.name + " - " + str(self.age))
        }
    }

    # إنشاء كائنات
    ahmad = Person("أحمد", 50)
    mohamed = Person("محمد", 25)

    # حقائق منطقية
    parent("أحمد", "محمد").

    # استعلام ودمج النتائج
    results = query parent(?P, "محمد")?

    for result in results: {
        parent_name = result["?P"]
        if parent_name == "أحمد": {
            ahmad.display()
        }
    }
}
```

### 12.3 قاعدة معرفة ديناميكية مع دوال

```bayan
hybrid {
    # دالة لإضافة طالب
    def add_student(name, grade): {
        assertz(student(name, grade))
    }

    # دالة للبحث عن الطلاب المتفوقين
    def find_excellent_students(): {
        results = query student(?Name, ?Grade), ?Grade >= 90?

        excellent = []
        for result in results: {
            excellent.append(result["?Name"])
        }

        return excellent
    }

    # استخدام الدوال
    add_student("أحمد", 85)
    add_student("فاطمة", 95)
    add_student("علي", 92)

    top_students = find_excellent_students()

    for student in top_students: {
        print(student)  # فاطمة، علي
    }
}
```

---

## 13. أمثلة متقدمة

### 13.1 نظام خبير طبي بسيط

```bayan
hybrid {
    # الأعراض
    symptom("patient1", "fever").
    symptom("patient1", "cough").
    symptom("patient2", "headache").
    symptom("patient2", "fever").

    # قواعد التشخيص
    diagnosis(?Patient, "flu") :-
        symptom(?Patient, "fever"),
        symptom(?Patient, "cough").

    diagnosis(?Patient, "migraine") :-
        symptom(?Patient, "headache").

    # دالة للتشخيص
    def diagnose_patient(patient_name): {
        results = query diagnosis(patient_name, ?Disease)?

        if len(results) > 0: {
            disease = results[0]["?Disease"]
            return disease
        }

        return "غير معروف"
    }

    # استخدام النظام
    diagnosis1 = diagnose_patient("patient1")
    print("Patient 1: " + diagnosis1)  # flu

    diagnosis2 = diagnose_patient("patient2")
    print("Patient 2: " + diagnosis2)  # migraine
}
```

### 13.2 نظام توصيات

```bayan
hybrid {
    # تفضيلات المستخدمين
    likes("أحمد", "برمجة").
    likes("أحمد", "رياضيات").
    likes("فاطمة", "برمجة").
    likes("فاطمة", "فيزياء").
    likes("علي", "رياضيات").

    # قاعدة: مستخدمان متشابهان إذا أحبا نفس الشيء
    similar(?User1, ?User2) :-
        likes(?User1, ?Thing),
        likes(?User2, ?Thing),
        ?User1 != ?User2.

    # دالة للحصول على توصيات
    def get_recommendations(user): {
        # البحث عن مستخدمين متشابهين
        similar_users = query similar(user, ?Other)?

        recommendations = []

        for result in similar_users: {
            other_user = result["?Other"]

            # البحث عن ما يحبه المستخدم المشابه
            likes_results = query likes(other_user, ?Thing)?

            for like_result in likes_results: {
                thing = like_result["?Thing"]

                # التحقق من أن المستخدم الحالي لا يحبه بالفعل
                already_likes = query likes(user, thing)?

                if len(already_likes) == 0: {
                    if thing not in recommendations: {
                        recommendations.append(thing)
                    }
                }
            }
        }

        return recommendations
    }

    # الحصول على توصيات لأحمد
    recs = get_recommendations("أحمد")

    print("توصيات لأحمد:")
    for rec in recs: {
        print(rec)  # فيزياء
    }
}
```

### 13.3 معالجة بيانات ML

```bayan
hybrid {
    # بيانات تدريب
    training_sample("sample1", "class_a", 0.8).
    training_sample("sample2", "class_a", 0.9).
    training_sample("sample3", "class_b", 0.3).
    training_sample("sample4", "class_b", 0.2).

    # دالة لحساب متوسط درجات صنف
    def calculate_class_average(class_name): {
        # جمع جميع الدرجات للصنف
        goal = training_sample(?ID, class_name, ?Score)
        results = query findall(?Score, goal, ?Scores)?

        if len(results) > 0: {
            scores = results[0]["?Scores"]

            # حساب المتوسط
            total = sum(scores)
            average = total / len(scores)

            return average
        }

        return 0
    }

    # حساب المتوسطات
    avg_a = calculate_class_average("class_a")
    avg_b = calculate_class_average("class_b")

    print("Class A average: " + str(avg_a))  # 0.85
    print("Class B average: " + str(avg_b))  # 0.25
}
```

### 13.4 رسم بياني للمعرفة (Knowledge Graph)

```bayan
hybrid {
    # علاقات في رسم بياني
    connected("الرياض", "جدة").
    connected("جدة", "مكة").
    connected("مكة", "المدينة").
    connected("الرياض", "الدمام").

    distance("الرياض", "جدة", 950).
    distance("جدة", "مكة", 80).
    distance("مكة", "المدينة", 400).
    distance("الرياض", "الدمام", 400).

    # قاعدة: يمكن الوصول من A إلى B
    reachable(?A, ?B) :- connected(?A, ?B).
    reachable(?A, ?C) :- connected(?A, ?B), reachable(?B, ?C).

    # دالة للبحث عن مسار
    def find_path(start, end): {
        results = query reachable(start, end)?

        if len(results) > 0: {
            return True
        }

        return False
    }

    # دالة لحساب المسافة الكلية
    def calculate_distance(city1, city2): {
        results = query distance(city1, city2, ?Dist)?

        if len(results) > 0: {
            return results[0]["?Dist"]
        }

        return 0
    }

    # استخدام النظام
    can_reach = find_path("الرياض", "المدينة")
    print("Can reach: " + str(can_reach))  # True

    dist = calculate_distance("الرياض", "جدة")
    print("Distance: " + str(dist))  # 950
}
```

### 13.5 نظام قواعد الأعمال

```bayan
hybrid {
    # حقائق عن الموظفين
    employee("أحمد", "مهندس", 5).
    employee("فاطمة", "مدير", 10).
    employee("علي", "مبرمج", 2).

    salary("مهندس", 8000).
    salary("مدير", 15000).
    salary("مبرمج", 6000).

    # قواعد الترقية
    eligible_for_promotion(?Name) :-
        employee(?Name, ?Position, ?Years),
        ?Years >= 5.

    # قواعد المكافأة
    bonus_percentage(?Name, 20) :-
        employee(?Name, ?Position, ?Years),
        ?Years >= 10.

    bonus_percentage(?Name, 10) :-
        employee(?Name, ?Position, ?Years),
        ?Years >= 5,
        ?Years < 10.

    bonus_percentage(?Name, 5) :-
        employee(?Name, ?Position, ?Years),
        ?Years < 5.

    # دالة لحساب الراتب الكلي
    def calculate_total_salary(name): {
        # الحصول على الراتب الأساسي
        emp_results = query employee(name, ?Position, ?Years)?

        if len(emp_results) == 0: {
            return 0
        }

        position = emp_results[0]["?Position"]

        salary_results = query salary(position, ?BaseSalary)?
        base_salary = salary_results[0]["?BaseSalary"]

        # الحصول على نسبة المكافأة
        bonus_results = query bonus_percentage(name, ?Bonus)?
        bonus_percent = bonus_results[0]["?Bonus"]

        # حساب الراتب الكلي
        bonus_amount = base_salary * bonus_percent / 100
        total = base_salary + bonus_amount

        return total
    }

    # حساب الرواتب
    ahmad_salary = calculate_total_salary("أحمد")
    print("أحمد: " + str(ahmad_salary))  # 8800

    fatima_salary = calculate_total_salary("فاطمة")
    print("فاطمة: " + str(fatima_salary))  # 18000

    # البحث عن المؤهلين للترقية
    promotion_results = query eligible_for_promotion(?Name)?

    print("مؤهلون للترقية:")
    for result in promotion_results: {
        print(result["?Name"])  # أحمد، فاطمة
    }
}
```

---

## 🎓 خاتمة

الآن أصبحت تعرف البرمجة المنطقية في لغة البيان من المبتدئ إلى المحترف!

### 📚 ما تعلمته:

#### المستوى الأساسي:
- ✅ الحقائق والاستعلامات
- ✅ المتغيرات المنطقية
- ✅ القواعد البسيطة

#### المستوى المتوسط:
- ✅ القواعد المركبة
- ✅ العودية (Recursion)
- ✅ القوائم في البرمجة المنطقية
- ✅ العمليات المنطقية (AND, OR, NOT)

#### المستوى المتقدم:
- ✅ Meta-predicates (findall, bagof, setof)
- ✅ قاعدة المعرفة الديناميكية (assert, retract)
- ✅ البرمجة الهجينة (دمج الأنماط الثلاثة)
- ✅ أمثلة متقدمة (أنظمة خبيرة، توصيات، ML، Knowledge Graphs)

### 💡 نصائح للإتقان:

1. **ابدأ بسيطاً**: ابدأ بحقائق واستعلامات بسيطة
2. **فكر منطقياً**: البرمجة المنطقية تعتمد على "ماذا" وليس "كيف"
3. **استخدم العودية**: العودية قوية جداً في البرمجة المنطقية
4. **جرب الهجين**: دمج الأنماط الثلاثة يعطيك قوة هائلة
5. **اكتب أمثلة**: الممارسة هي المفتاح

### 🚀 التطبيقات العملية:

البرمجة المنطقية مثالية لـ:
- 🧠 **الأنظمة الخبيرة** (Expert Systems)
- 🤖 **الذكاء الاصطناعي** (AI Reasoning)
- 📊 **تحليل البيانات** (Data Analysis)
- 🔍 **محركات البحث** (Search Engines)
- 💼 **قواعد الأعمال** (Business Rules)
- 🌐 **رسوم المعرفة** (Knowledge Graphs)

### 📖 المراجع:

- **[الجزء الأول: مقدمة](01_INTRODUCTION_AR.md)** - تعريف بلغة البيان
- **[الجزء الثاني: البرمجة الإجرائية والكائنية](02_PROCEDURAL_OOP_AR.md)** - دليل شامل للـ OOP

---

## 🌟 الخلاصة النهائية

**لغة البيان** هي اللغة الوحيدة في العالم التي تجمع:
- ✅ البرمجة الإجرائية
- ✅ البرمجة الكائنية
- ✅ البرمجة المنطقية

في لغة واحدة مع دعم كامل للعربية والإنجليزية!

**بالتوفيق في رحلتك البرمجية مع لغة البيان! 🎉🚀**

</div>

