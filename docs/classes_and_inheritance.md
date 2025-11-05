# الأصناف والوراثة المتقدمة (Classes & Inheritance)

دليل شامل للعمل مع الأصناف والوراثة في لغة بيان.

---

## 1. أساسيات الأصناف

### تعريف صنف بسيط:
```bayan
class Person:
{
    def __init__(name, age):
    {
        self.name = name
        self.age = age
    }
    
    def greet():
    {
        print("مرحبا، أنا " + self.name)
    }
    
    def get_age():
    {
        return self.age
    }
}

# إنشاء كائن
person = Person("أحمد", 25)
person.greet()          # مرحبا، أنا أحمد
print(person.get_age()) # 25
```

### الخصائص والطرق:
```bayan
class Car:
{
    def __init__(brand, model):
    {
        self.brand = brand
        self.model = model
        self.speed = 0
    }
    
    def accelerate():
    {
        self.speed = self.speed + 10
    }
    
    def brake():
    {
        self.speed = self.speed - 10
    }
    
    def get_info():
    {
        return self.brand + " " + self.model
    }
}

car = Car("Toyota", "Camry")
car.accelerate()
print(car.speed)        # 10
```

---

## 2. الوراثة البسيطة (Single Inheritance)

### تعريف صنف وارث:
```bayan
class Animal:
{
    def __init__(name):
    {
        self.name = name
    }
    
    def speak():
    {
        print(self.name + " يصدر صوتاً")
    }
}

class Dog(Animal):
{
    def speak():
    {
        print(self.name + " ينبح")
    }
}

class Cat(Animal):
{
    def speak():
    {
        print(self.name + " يموء")
    }
}

dog = Dog("ماكس")
dog.speak()             # ماكس ينبح

cat = Cat("ميشا")
cat.speak()             # ميشا يموء
```

---

## 3. الوراثة المتعددة (Multiple Inheritance)

### تعريف صنف بعدة آباء:
```bayan
class Swimmer:
{
    def swim():
    {
        print(self.name + " يسبح")
    }
}

class Flyer:
{
    def fly():
    {
        print(self.name + " يطير")
    }
}

class Duck(Swimmer, Flyer):
{
    def __init__(name):
    {
        self.name = name
    }
}

duck = Duck("دونالد")
duck.swim()             # دونالد يسبح
duck.fly()              # دونالد يطير
```

---

## 4. ترتيب حل الطرق (C3 MRO)

### فهم MRO:
```bayan
class A:
{
    def method():
    {
        print("A")
    }
}

class B(A):
{
    def method():
    {
        print("B")
    }
}

class C(A):
{
    def method():
    {
        print("C")
    }
}

class D(B, C):
{
    pass
}

d = D()
d.method()              # B (حسب ترتيب MRO: D -> B -> C -> A)
```

### ترتيب البحث:
```bayan
# ترتيب البحث عن الطرق:
# 1. الصنف نفسه (D)
# 2. الآباء بالترتيب (B، ثم C)
# 3. آباء الآباء (A)
```

---

## 5. استخدام super()

### الصيغة الأولى:
```bayan
class Parent:
{
    def greet():
    {
        print("مرحبا من الأب")
    }
}

class Child(Parent):
{
    def greet():
    {
        super().greet()
        print("مرحبا من الابن")
    }
}

child = Child()
child.greet()
# المخرجات:
# مرحبا من الأب
# مرحبا من الابن
```

### الصيغة الثانية:
```bayan
class Parent:
{
    def greet():
    {
        print("مرحبا من الأب")
    }
}

class Child(Parent):
{
    def greet():
    {
        super(greet)
        print("مرحبا من الابن")
    }
}
```

---

## 6. الدوال السحرية (Dunder Methods)

### __init__ و __repr__:
```bayan
class Person:
{
    def __init__(name, age):
    {
        self.name = name
        self.age = age
    }
    
    def __repr__():
    {
        return "Person(" + self.name + ", " + self.age + ")"
    }
}

p = Person("أحمد", 25)
print(repr(p))          # Person(أحمد, 25)
```

### __str__ و __len__:
```bayan
class List:
{
    def __init__(items):
    {
        self.items = items
    }
    
    def __len__():
    {
        return len(self.items)
    }
}

lst = List([1, 2, 3])
print(len(lst))         # 3
```

### __getitem__ و __setitem__:
```bayan
class Container:
{
    def __init__():
    {
        self.data = [10, 20, 30]
    }
    
    def __getitem__(index):
    {
        return self.data[index]
    }
    
    def __setitem__(index, value):
    {
        self.data[index] = value
    }
}

c = Container()
print(c[0])             # 10
c[0] = 100
print(c[0])             # 100
```

### __contains__:
```bayan
class Set:
{
    def __init__(items):
    {
        self.items = items
    }
    
    def __contains__(item):
    {
        return item in self.items
    }
}

s = Set([1, 2, 3])
print(2 in s)           # True
print(5 in s)           # False
```

### __iter__:
```bayan
class Range:
{
    def __init__(n):
    {
        self.n = n
        self.current = 0
    }
    
    def __iter__():
    {
        return self
    }
}

r = Range(3)
for i in r:
{
    print(i)
}
```

---

## 7. الخصائص الثابتة والطرق الثابتة

### الخصائص الثابتة:
```bayan
class Counter:
{
    count = 0
    
    def __init__():
    {
        Counter.count = Counter.count + 1
    }
}

c1 = Counter()
c2 = Counter()
print(Counter.count)    # 2
```

### الطرق الثابتة (مخطط):
```bayan
# مخطط
class Math:
{
    @staticmethod
    def add(a, b):
    {
        return a + b
    }
}

print(Math.add(2, 3))   # 5
```

---

## 8. الخصائص المحمية والخاصة

### الاتفاقية (Convention):
```bayan
class BankAccount:
{
    def __init__(balance):
    {
        self._balance = balance      # محمية (بـ _)
        self.__pin = 1234            # خاصة (بـ __)
    }
    
    def get_balance():
    {
        return self._balance
    }
}

account = BankAccount(1000)
print(account.get_balance())  # 1000
```

---

## 9. التركيب (Composition)

### استخدام الكائنات داخل كائنات:
```bayan
class Address:
{
    def __init__(city, country):
    {
        self.city = city
        self.country = country
    }
}

class Person:
{
    def __init__(name, address):
    {
        self.name = name
        self.address = address
    }
    
    def get_info():
    {
        return self.name + " من " + self.address.city
    }
}

addr = Address("القاهرة", "مصر")
person = Person("أحمد", addr)
print(person.get_info())  # أحمد من القاهرة
```

---

## 10. الأنماط الشائعة

### نمط Singleton:
```bayan
class Database:
{
    _instance = None
    
    def __init__():
    {
        if Database._instance == None:
        {
            Database._instance = self
        }
    }
}
```

### نمط Factory:
```bayan
class AnimalFactory:
{
    def create_animal(type):
    {
        if type == "dog":
        {
            return Dog("ماكس")
        }
        elif type == "cat":
        {
            return Cat("ميشا")
        }
    }
}
```

---

## 11. الميزات المخطط إضافتها

### 1. Decorators:
```bayan
# مخطط
@property
def age():
{
    return self._age
}
```

### 2. Abstract Classes:
```bayan
# مخطط
class AbstractAnimal:
{
    def speak():
    {
        raise NotImplementedError()
    }
}
```

### 3. Metaclasses:
```bayan
# مخطط
class Meta(type):
{
    def __new__(name, bases, attrs):
    {
        return super().__new__(name, bases, attrs)
    }
}
```

---

**آخر تحديث:** 2024-10-23

