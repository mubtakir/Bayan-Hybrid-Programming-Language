# دليل لغة البيان - الجزء الثاني: البرمجة الإجرائية والكائنية
# Bayan Language Guide - Part 2: Procedural & OOP Programming

<div dir="rtl">

## 📚 جدول المحتويات

### القسم الأول: الأساسيات (للمبتدئين)
1. [المتغيرات وأنواع البيانات](#1-المتغيرات-وأنواع-البيانات)
2. [العمليات الحسابية والمنطقية](#2-العمليات-الحسابية-والمنطقية)
3. [النصوص (Strings)](#3-النصوص-strings)
4. [القوائم (Lists)](#4-القوائم-lists)
5. [القواميس (Dictionaries)](#5-القواميس-dictionaries)
6. [المجموعات (Sets)](#6-المجموعات-sets)

### القسم الثاني: التحكم في التدفق (متوسط)
7. [الشروط (if/elif/else)](#7-الشروط-ifelifelse)
8. [الحلقات (for/while)](#8-الحلقات-forwhile)
9. [الدوال (Functions)](#9-الدوال-functions)
10. [معالجة الاستثناءات](#10-معالجة-الاستثناءات)

### القسم الثالث: البرمجة الكائنية (متقدم)
11. [الأصناف والكائنات](#11-الأصناف-والكائنات)
12. [الوراثة](#12-الوراثة)
13. [التغليف](#13-التغليف)
14. [تعدد الأشكال](#14-تعدد-الأشكال)

### القسم الرابع: ميزات متقدمة (محترف)
15. [Decorators](#15-decorators)
16. [Generators](#16-generators)
17. [Async/Await](#17-asyncawait)
18. [Context Managers](#18-context-managers)
19. [*args و **kwargs](#19-args-و-kwargs)

---

# القسم الأول: الأساسيات

## 1. المتغيرات وأنواع البيانات

### 1.1 تعريف المتغيرات

في لغة البيان، لا تحتاج لتحديد نوع المتغير (Dynamic Typing):

```bayan
hybrid {
    # أرقام صحيحة (Integers)
    age = 25
    year = 2024
    
    # أرقام عشرية (Floats)
    price = 99.99
    pi = 3.14159
    
    # نصوص (Strings)
    name = "أحمد"
    city = "الرياض"
    
    # قيم منطقية (Booleans)
    is_student = True
    is_married = False
    
    # قيمة فارغة (None)
    result = None
}
```

### 1.2 أنواع البيانات الأساسية

```bayan
hybrid {
    # Integer
    x = 10
    print(x)  # 10
    
    # Float
    y = 3.14
    print(y)  # 3.14
    
    # String
    text = "مرحباً"
    print(text)  # مرحباً
    
    # Boolean
    flag = True
    print(flag)  # True
    
    # None
    empty = None
    print(empty)  # None
}
```

### 1.3 تحويل الأنواع

```bayan
hybrid {
    # String to Integer
    text = "123"
    number = int(text)
    print(number)  # 123
    
    # Integer to String
    age = 25
    age_text = str(age)
    print(age_text)  # "25"
    
    # String to Float
    price_text = "99.99"
    price = float(price_text)
    print(price)  # 99.99
    
    # Integer to Float
    x = 10
    y = float(x)
    print(y)  # 10.0
}
```

---

## 2. العمليات الحسابية والمنطقية

### 2.1 العمليات الحسابية

```bayan
hybrid {
    a = 10
    b = 3
    
    # الجمع
    sum = a + b
    print(sum)  # 13
    
    # الطرح
    diff = a - b
    print(diff)  # 7
    
    # الضرب
    product = a * b
    print(product)  # 30
    
    # القسمة
    division = a / b
    print(division)  # 3.333...
    
    # القسمة الصحيحة
    floor_div = a // b
    print(floor_div)  # 3
    
    # الباقي
    remainder = a % b
    print(remainder)  # 1
    
    # الأس
    power = a ** b
    print(power)  # 1000
}
```

### 2.2 عمليات المقارنة

```bayan
hybrid {
    x = 10
    y = 20
    
    # يساوي
    result1 = (x == y)
    print(result1)  # False
    
    # لا يساوي
    result2 = (x != y)
    print(result2)  # True
    
    # أكبر من
    result3 = (x > y)
    print(result3)  # False
    
    # أصغر من
    result4 = (x < y)
    print(result4)  # True
    
    # أكبر من أو يساوي
    result5 = (x >= 10)
    print(result5)  # True
    
    # أصغر من أو يساوي
    result6 = (y <= 20)
    print(result6)  # True
}
```

### 2.3 العمليات المنطقية

```bayan
hybrid {
    a = True
    b = False
    
    # AND (و)
    result1 = a and b
    print(result1)  # False
    
    # OR (أو)
    result2 = a or b
    print(result2)  # True
    
    # NOT (ليس)
    result3 = not a
    print(result3)  # False
    
    # مثال مركب
    x = 10
    y = 20
    result4 = (x > 5) and (y < 30)
    print(result4)  # True
}
```

---

## 3. النصوص (Strings)

### 3.1 إنشاء النصوص

```bayan
hybrid {
    # نص بسيط
    text1 = "مرحباً"
    text2 = 'Hello'
    
    # نص متعدد الأسطر
    text3 = """
    هذا نص
    متعدد الأسطر
    """
    
    # نص فارغ
    empty = ""
}
```

### 3.2 عمليات النصوص

```bayan
hybrid {
    # دمج النصوص
    first = "محمد"
    last = "أحمد"
    full_name = first + " " + last
    print(full_name)  # "محمد أحمد"
    
    # تكرار النص
    text = "Ha" * 3
    print(text)  # "HaHaHa"
    
    # طول النص
    length = len(full_name)
    print(length)  # 9
    
    # الوصول إلى حرف
    first_char = full_name[0]
    print(first_char)  # "م"
    
    # قطع النص (Slicing)
    substring = full_name[0:4]
    print(substring)  # "محمد"
}
```

### 3.3 دوال النصوص المدمجة

```bayan
hybrid {
    text = "Hello World"
    
    # تحويل لأحرف كبيرة
    upper_text = upper(text)
    print(upper_text)  # "HELLO WORLD"
    
    # تحويل لأحرف صغيرة
    lower_text = lower(text)
    print(lower_text)  # "hello world"
    
    # استبدال
    new_text = replace(text, "World", "Python")
    print(new_text)  # "Hello Python"
    
    # تقسيم النص
    words = split(text, " ")
    print(words)  # ["Hello", "World"]
}
```

### 3.4 Escape Sequences

```bayan
hybrid {
    # سطر جديد
    text1 = "السطر الأول\nالسطر الثاني"
    print(text1)
    
    # Tab
    text2 = "العمود1\tالعمود2"
    print(text2)
    
    # علامة اقتباس
    text3 = "قال: \"مرحباً\""
    print(text3)
    
    # Backslash
    text4 = "المسار: C:\\Users\\Ahmad"
    print(text4)
}
```

---

## 4. القوائم (Lists)

### 4.1 إنشاء القوائم

```bayan
hybrid {
    # قائمة فارغة
    empty_list = []
    
    # قائمة أرقام
    numbers = [1, 2, 3, 4, 5]
    
    # قائمة نصوص
    names = ["أحمد", "فاطمة", "علي"]
    
    # قائمة مختلطة
    mixed = [1, "text", 3.14, True]
    
    # قائمة متداخلة
    nested = [[1, 2], [3, 4], [5, 6]]
}
```

### 4.2 الوصول إلى العناصر

```bayan
hybrid {
    fruits = ["تفاح", "موز", "برتقال", "عنب"]
    
    # الوصول بالفهرس
    first = fruits[0]
    print(first)  # "تفاح"
    
    # الفهرس السالب (من النهاية)
    last = fruits[-1]
    print(last)  # "عنب"
    
    # Slicing
    subset = fruits[1:3]
    print(subset)  # ["موز", "برتقال"]
    
    # طول القائمة
    length = len(fruits)
    print(length)  # 4
}
```

### 4.3 تعديل القوائم

```bayan
hybrid {
    numbers = [1, 2, 3, 4, 5]
    
    # تغيير عنصر
    numbers[0] = 10
    print(numbers)  # [10, 2, 3, 4, 5]
    
    # إضافة عنصر في النهاية
    numbers.append(6)
    print(numbers)  # [10, 2, 3, 4, 5, 6]
    
    # إضافة عنصر في موضع محدد
    numbers.insert(0, 0)
    print(numbers)  # [0, 10, 2, 3, 4, 5, 6]
    
    # حذف عنصر
    numbers.remove(10)
    print(numbers)  # [0, 2, 3, 4, 5, 6]
    
    # حذف بالفهرس
    del numbers[0]
    print(numbers)  # [2, 3, 4, 5, 6]
}
```

### 4.4 عمليات القوائم

```bayan
hybrid {
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    
    # دمج القوائم
    combined = list1 + list2
    print(combined)  # [1, 2, 3, 4, 5, 6]
    
    # تكرار القائمة
    repeated = list1 * 2
    print(repeated)  # [1, 2, 3, 1, 2, 3]
    
    # البحث عن عنصر
    exists = 2 in list1
    print(exists)  # True
    
    # فرز القائمة
    numbers = [5, 2, 8, 1, 9]
    sorted_numbers = sorted(numbers)
    print(sorted_numbers)  # [1, 2, 5, 8, 9]
    
    # عكس القائمة
    reversed_list = list(reversed(numbers))
    print(reversed_list)  # [9, 1, 8, 2, 5]
}
```

---

## 5. القواميس (Dictionaries)

### 5.1 إنشاء القواميس

```bayan
hybrid {
    # قاموس فارغ
    empty_dict = {}
    
    # قاموس بسيط
    person = {
        "name": "أحمد",
        "age": 25,
        "city": "الرياض"
    }
    
    # قاموس بمفاتيح عربية
    student = {
        "الاسم": "فاطمة",
        "العمر": 20,
        "التخصص": "علوم حاسب"
    }
}
```

### 5.2 الوصول إلى القيم

```bayan
hybrid {
    person = {
        "name": "أحمد",
        "age": 25,
        "city": "الرياض"
    }
    
    # الوصول بالمفتاح
    name = person["name"]
    print(name)  # "أحمد"
    
    # التحقق من وجود مفتاح
    has_age = "age" in person
    print(has_age)  # True
    
    # الحصول على جميع المفاتيح
    keys = list(person.keys())
    print(keys)  # ["name", "age", "city"]
    
    # الحصول على جميع القيم
    values = list(person.values())
    print(values)  # ["أحمد", 25, "الرياض"]
}
```

### 5.3 تعديل القواميس

```bayan
hybrid {
    person = {
        "name": "أحمد",
        "age": 25
    }
    
    # إضافة/تعديل قيمة
    person["city"] = "الرياض"
    person["age"] = 26
    print(person)
    
    # حذف مفتاح
    del person["age"]
    print(person)
    
    # مسح القاموس
    person.clear()
    print(person)  # {}
}
```

---

## 6. المجموعات (Sets)

### 6.1 إنشاء المجموعات

```bayan
hybrid {
    # مجموعة من الأرقام
    numbers = {1, 2, 3, 4, 5}
    
    # مجموعة من النصوص
    fruits = {"تفاح", "موز", "برتقال"}
    
    # ملاحظة: المجموعات لا تحتوي على عناصر مكررة
    unique_numbers = {1, 2, 2, 3, 3, 3}
    print(unique_numbers)  # {1, 2, 3}
}
```

### 6.2 عمليات المجموعات

```bayan
hybrid {
    set1 = {1, 2, 3, 4}
    set2 = {3, 4, 5, 6}
    
    # الاتحاد (Union)
    union = set1 | set2
    print(union)  # {1, 2, 3, 4, 5, 6}
    
    # التقاطع (Intersection)
    intersection = set1 & set2
    print(intersection)  # {3, 4}
    
    # الفرق (Difference)
    difference = set1 - set2
    print(difference)  # {1, 2}
    
    # إضافة عنصر
    set1.add(5)
    print(set1)  # {1, 2, 3, 4, 5}
    
    # حذف عنصر
    set1.remove(5)
    print(set1)  # {1, 2, 3, 4}
}
```

---

# القسم الثاني: التحكم في التدفق

## 7. الشروط (if/elif/else)

### 7.1 الشرط البسيط

```bayan
hybrid {
    age = 18
    
    if age >= 18: {
        print("بالغ")
    }
}
```

### 7.2 if-else

```bayan
hybrid {
    temperature = 30
    
    if temperature > 25: {
        print("الجو حار")
    }
    else: {
        print("الجو معتدل")
    }
}
```

### 7.3 if-elif-else

```bayan
hybrid {
    score = 85
    
    if score >= 90: {
        print("ممتاز")
    }
    elif score >= 80: {
        print("جيد جداً")
    }
    elif score >= 70: {
        print("جيد")
    }
    elif score >= 60: {
        print("مقبول")
    }
    else: {
        print("راسب")
    }
}
```

### 7.4 شروط متداخلة

```bayan
hybrid {
    age = 20
    has_license = True
    
    if age >= 18: {
        if has_license: {
            print("يمكنك القيادة")
        }
        else: {
            print("تحتاج رخصة قيادة")
        }
    }
    else: {
        print("أنت صغير السن")
    }
}
```

---

## 8. الحلقات (for/while)

### 8.1 حلقة for

```bayan
hybrid {
    # التكرار على قائمة
    fruits = ["تفاح", "موز", "برتقال"]
    
    for fruit in fruits: {
        print(fruit)
    }
    
    # التكرار على range
    for i in range(5): {
        print(i)  # 0, 1, 2, 3, 4
    }
    
    # range مع بداية ونهاية
    for i in range(1, 6): {
        print(i)  # 1, 2, 3, 4, 5
    }
    
    # range مع خطوة
    for i in range(0, 10, 2): {
        print(i)  # 0, 2, 4, 6, 8
    }
}
```

### 8.2 حلقة while

```bayan
hybrid {
    # حلقة while بسيطة
    count = 0
    
    while count < 5: {
        print(count)
        count = count + 1
    }
    
    # حلقة while مع شرط
    number = 1
    
    while number <= 10: {
        if number % 2 == 0: {
            print(number)
        }
        number = number + 1
    }
}
```

### 8.3 break و continue

```bayan
hybrid {
    # break - إيقاف الحلقة
    for i in range(10): {
        if i == 5: {
            break
        }
        print(i)  # 0, 1, 2, 3, 4
    }
    
    # continue - تخطي التكرار الحالي
    for i in range(5): {
        if i == 2: {
            continue
        }
        print(i)  # 0, 1, 3, 4
    }
}
```

### 8.4 enumerate و zip

```bayan
hybrid {
    # enumerate - الحصول على الفهرس والقيمة
    fruits = ["تفاح", "موز", "برتقال"]
    
    for index_value in enumerate(fruits): {
        index = index_value[0]
        value = index_value[1]
        print(index)
        print(value)
    }
    
    # zip - دمج قائمتين
    names = ["أحمد", "فاطمة", "علي"]
    ages = [25, 22, 30]
    
    for pair in zip(names, ages): {
        name = pair[0]
        age = pair[1]
        print(name)
        print(age)
    }
}
```

---

## 9. الدوال (Functions)

### 9.1 تعريف دالة بسيطة

```bayan
hybrid {
    def greet(): {
        print("مرحباً!")
    }
    
    greet()  # استدعاء الدالة
}
```

### 9.2 دالة بمعاملات

```bayan
hybrid {
    def greet_person(name): {
        print("مرحباً " + name)
    }
    
    greet_person("أحمد")  # "مرحباً أحمد"
    greet_person("فاطمة")  # "مرحباً فاطمة"
}
```

### 9.3 دالة بقيمة إرجاع

```bayan
hybrid {
    def add(a, b): {
        return a + b
    }
    
    result = add(10, 20)
    print(result)  # 30
}
```

### 9.4 معاملات افتراضية

```bayan
hybrid {
    def greet(name, greeting="مرحباً"): {
        return greeting + " " + name
    }

    msg1 = greet("أحمد")
    print(msg1)  # "مرحباً أحمد"

    msg2 = greet("فاطمة", "أهلاً")
    print(msg2)  # "أهلاً فاطمة"
}
```

### 9.5 دوال متعددة القيم

```bayan
hybrid {
    def get_min_max(numbers): {
        minimum = min(numbers)
        maximum = max(numbers)
        return [minimum, maximum]
    }

    result = get_min_max([5, 2, 8, 1, 9])
    print(result[0])  # 1 (minimum)
    print(result[1])  # 9 (maximum)
}
```

### 9.6 دوال متداخلة

```bayan
hybrid {
    def outer_function(x): {
        def inner_function(y): {
            return x + y
        }

        return inner_function(10)
    }

    result = outer_function(5)
    print(result)  # 15
}
```

---

## 10. معالجة الاستثناءات

### 10.1 try-except الأساسي

```bayan
hybrid {
    try: {
        x = 10 / 0
    }
    except ZeroDivisionError: {
        print("خطأ: القسمة على صفر!")
    }
}
```

### 10.2 معالجة استثناءات متعددة

```bayan
hybrid {
    try: {
        number = int("abc")
    }
    except ValueError: {
        print("خطأ: قيمة غير صحيحة")
    }
    except TypeError: {
        print("خطأ: نوع غير صحيح")
    }
}
```

### 10.3 try-except-finally

```bayan
hybrid {
    try: {
        file = open("data.txt", "r")
        content = file.read()
    }
    except FileNotFoundError: {
        print("الملف غير موجود")
    }
    finally: {
        print("تم الانتهاء من المحاولة")
    }
}
```

### 10.4 رفع استثناء

```bayan
hybrid {
    def check_age(age): {
        if age < 0: {
            raise ValueError("العمر لا يمكن أن يكون سالباً")
        }
        return age
    }

    try: {
        check_age(-5)
    }
    except ValueError: {
        print("خطأ في العمر")
    }
}
```

---

# القسم الثالث: البرمجة الكائنية

## 11. الأصناف والكائنات

### 11.1 تعريف صنف بسيط

```bayan
hybrid {
    class Person: {
        def __init__(self, name, age): {
            self.name = name
            self.age = age
        }

        def display(self): {
            print(self.name)
            print(self.age)
        }
    }

    # إنشاء كائن
    person1 = Person("أحمد", 25)
    person1.display()
}
```

### 11.2 الخصائص والطرق

```bayan
hybrid {
    class Student: {
        def __init__(self, name, grade): {
            self.name = name
            self.grade = grade
            self.courses = []
        }

        def add_course(self, course): {
            self.courses.append(course)
        }

        def get_info(self): {
            info = self.name + " - Grade: " + str(self.grade)
            return info
        }
    }

    student = Student("فاطمة", 95)
    student.add_course("رياضيات")
    student.add_course("فيزياء")

    print(student.get_info())
    print(student.courses)
}
```

### 11.3 صنف مع عدة طرق

```bayan
hybrid {
    class BankAccount: {
        def __init__(self, owner, balance): {
            self.owner = owner
            self.balance = balance
        }

        def deposit(self, amount): {
            self.balance = self.balance + amount
            return self.balance
        }

        def withdraw(self, amount): {
            if amount > self.balance: {
                print("رصيد غير كافٍ")
                return self.balance
            }
            self.balance = self.balance - amount
            return self.balance
        }

        def get_balance(self): {
            return self.balance
        }
    }

    account = BankAccount("أحمد", 1000)
    account.deposit(500)
    print(account.get_balance())  # 1500

    account.withdraw(200)
    print(account.get_balance())  # 1300
}
```

---

## 12. الوراثة

### 12.1 وراثة بسيطة

```bayan
hybrid {
    # الصنف الأب
    class Animal: {
        def __init__(self, name): {
            self.name = name
        }

        def speak(self): {
            print("الحيوان يصدر صوتاً")
        }
    }

    # الصنف الابن
    class Dog: {
        def __init__(self, name, breed): {
            self.name = name
            self.breed = breed
        }

        def speak(self): {
            print("الكلب ينبح")
        }
    }

    dog = Dog("ريكس", "جيرمن")
    dog.speak()  # "الكلب ينبح"
}
```

### 12.2 استخدام super()

```bayan
hybrid {
    class Vehicle: {
        def __init__(self, brand, model): {
            self.brand = brand
            self.model = model
        }

        def info(self): {
            return self.brand + " " + self.model
        }
    }

    class Car: {
        def __init__(self, brand, model, doors): {
            self.brand = brand
            self.model = model
            self.doors = doors
        }

        def info(self): {
            base_info = self.brand + " " + self.model
            return base_info + " - Doors: " + str(self.doors)
        }
    }

    car = Car("تويوتا", "كامري", 4)
    print(car.info())
}
```

### 12.3 الوراثة المتعددة

```bayan
hybrid {
    class Flyable: {
        def fly(self): {
            print("يطير")
        }
    }

    class Swimmable: {
        def swim(self): {
            print("يسبح")
        }
    }

    class Duck: {
        def __init__(self, name): {
            self.name = name
        }

        def fly(self): {
            print("البطة تطير")
        }

        def swim(self): {
            print("البطة تسبح")
        }
    }

    duck = Duck("دونالد")
    duck.fly()
    duck.swim()
}
```

---

## 13. التغليف

### 13.1 خصائص خاصة (Private)

```bayan
hybrid {
    class BankAccount: {
        def __init__(self, balance): {
            self.__balance = balance  # خاصية خاصة
        }

        def get_balance(self): {
            return self.__balance
        }

        def set_balance(self, amount): {
            if amount >= 0: {
                self.__balance = amount
            }
        }
    }

    account = BankAccount(1000)
    print(account.get_balance())  # 1000

    account.set_balance(2000)
    print(account.get_balance())  # 2000
}
```

---

## 14. تعدد الأشكال

### 14.1 Polymorphism الأساسي

```bayan
hybrid {
    class Shape: {
        def area(self): {
            return 0
        }
    }

    class Rectangle: {
        def __init__(self, width, height): {
            self.width = width
            self.height = height
        }

        def area(self): {
            return self.width * self.height
        }
    }

    class Circle: {
        def __init__(self, radius): {
            self.radius = radius
        }

        def area(self): {
            return 3.14 * self.radius * self.radius
        }
    }

    rect = Rectangle(5, 10)
    print(rect.area())  # 50

    circle = Circle(7)
    print(circle.area())  # 153.86
}
```

---

# القسم الرابع: ميزات متقدمة

## 15. Decorators

### 15.1 Decorator بسيط

```bayan
hybrid {
    def my_decorator(func): {
        def wrapper(): {
            print("قبل الدالة")
            func()
            print("بعد الدالة")
        }
        return wrapper
    }

    @my_decorator
    def say_hello(): {
        print("مرحباً!")
    }

    say_hello()
}
```

### 15.2 Decorator بمعاملات

```bayan
hybrid {
    def repeat(times): {
        def decorator(func): {
            def wrapper(): {
                for i in range(times): {
                    func()
                }
            }
            return wrapper
        }
        return decorator
    }

    @repeat(3)
    def greet(): {
        print("مرحباً")
    }

    greet()  # يطبع "مرحباً" 3 مرات
}
```

---

## 16. Generators

### 16.1 Generator بسيط

```bayan
hybrid {
    def count_up_to(n): {
        i = 1
        while i <= n: {
            yield i
            i = i + 1
        }
    }

    for num in count_up_to(5): {
        print(num)  # 1, 2, 3, 4, 5
    }
}
```

### 16.2 Generator للأعداد الزوجية

```bayan
hybrid {
    def even_numbers(max): {
        n = 0
        while n <= max: {
            yield n
            n = n + 2
        }
    }

    for num in even_numbers(10): {
        print(num)  # 0, 2, 4, 6, 8, 10
    }
}
```

---

## 17. Async/Await

### 17.1 دالة async بسيطة

```bayan
hybrid {
    async def fetch_data(): {
        print("جاري جلب البيانات...")
        return "البيانات"
    }

    async def main(): {
        result = await fetch_data()
        print(result)
    }
}
```

---

## 18. Context Managers

### 18.1 استخدام with

```bayan
hybrid {
    class FileManager: {
        def __init__(self, filename): {
            self.filename = filename
        }

        def __enter__(self): {
            print("فتح الملف")
            return self
        }

        def __exit__(self): {
            print("إغلاق الملف")
        }
    }

    with FileManager("data.txt"): {
        print("العمل مع الملف")
    }
}
```

---

## 19. *args و **kwargs

### 19.1 استخدام *args

```bayan
hybrid {
    def sum_all(*numbers): {
        total = 0
        for num in numbers: {
            total = total + num
        }
        return total
    }

    result1 = sum_all(1, 2, 3)
    print(result1)  # 6

    result2 = sum_all(1, 2, 3, 4, 5)
    print(result2)  # 15
}
```

### 19.2 استخدام **kwargs

```bayan
hybrid {
    def print_info(**info): {
        for key in info: {
            print(key)
            print(info[key])
        }
    }

    print_info(name="أحمد", age=25, city="الرياض")
}
```

### 19.3 استخدام كليهما

```bayan
hybrid {
    def create_profile(name, *hobbies, **details): {
        print(name)

        for hobby in hobbies: {
            print(hobby)
        }

        for key in details: {
            print(key)
            print(details[key])
        }
    }

    create_profile("أحمد", "قراءة", "برمجة", age=25, city="الرياض")
}
```

---

## 🎓 خاتمة

الآن أصبحت تعرف جميع أساسيات البرمجة الإجرائية والكائنية في لغة البيان!

### 📚 الخطوات التالية:
- **[الجزء الثالث: البرمجة المنطقية](03_LOGIC_PROGRAMMING_AR.md)** - تعلم البرمجة المنطقية من الصفر

### 💡 نصائح للممارسة:
1. اكتب أمثلة بنفسك
2. جرب تعديل الأمثلة الموجودة
3. ابدأ بمشاريع صغيرة
4. راجع الوثائق عند الحاجة

**بالتوفيق في رحلتك البرمجية! 🚀**

</div>

