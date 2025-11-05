# العوامل والعمليات في لغة بيان (Operators & Operations)

دليل شامل لجميع العوامل والعمليات المدعومة في لغة بيان.

---

## 1. العوامل الحسابية (Arithmetic Operators)

| العامل | الوصف | المثال | النتيجة |
|--------|-------|--------|---------|
| `+` | الجمع | `5 + 3` | `8` |
| `-` | الطرح | `5 - 3` | `2` |
| `*` | الضرب | `5 * 3` | `15` |
| `/` | القسمة | `6 / 2` | `3` |
| `%` | الباقي | `7 % 3` | `1` |
| `-` (أحادي) | السالب | `-5` | `-5` |

### أمثلة:
```bayan
x = 10
y = 3

print(x + y)    # 13
print(x - y)    # 7
print(x * y)    # 30
print(x / y)    # 3.333...
print(x % y)    # 1
print(-x)       # -10
```

---

## 2. عوامل المقارنة (Comparison Operators)

| العامل | الوصف | المثال | النتيجة |
|--------|-------|--------|---------|
| `==` | يساوي | `5 == 5` | `True` |
| `!=` | لا يساوي | `5 != 3` | `True` |
| `<` | أقل من | `3 < 5` | `True` |
| `<=` | أقل من أو يساوي | `5 <= 5` | `True` |
| `>` | أكبر من | `5 > 3` | `True` |
| `>=` | أكبر من أو يساوي | `5 >= 5` | `True` |

### أمثلة:
```bayan
a = 10
b = 5

print(a == b)   # False
print(a != b)   # True
print(a < b)    # False
print(a <= b)   # False
print(a > b)    # True
print(a >= b)   # True
```

---

## 3. العوامل المنطقية (Logical Operators)

| العامل | الوصف | المثال | النتيجة |
|--------|-------|--------|---------|
| `and` | و | `True and False` | `False` |
| `or` | أو | `True or False` | `True` |
| `not` | ليس | `not True` | `False` |

### أمثلة:
```bayan
x = True
y = False

print(x and y)      # False
print(x or y)       # True
print(not x)        # False
print(x and not y)  # True
```

### قصر الدارة (Short-circuit):
```bayan
# and: إذا كان الأول False، لا يُقيّم الثاني
result = False and expensive_function()  # لا يستدعي الدالة

# or: إذا كان الأول True، لا يُقيّم الثاني
result = True or expensive_function()    # لا يستدعي الدالة
```

---

## 4. عامل العضوية (Membership Operator)

| العامل | الوصف | المثال | النتيجة |
|--------|-------|--------|---------|
| `in` | موجود في | `2 in [1,2,3]` | `True` |

### أمثلة:
```bayan
lst = [1, 2, 3, 4, 5]
print(3 in lst)     # True
print(6 in lst)     # False

text = "مرحبا"
print("ح" in text)  # True

d = {"a": 1, "b": 2}
print("a" in d)     # True
```

---

## 5. أسبقية العوامل (Operator Precedence)

من الأعلى إلى الأدنى:

| المستوى | العوامل | الربط |
|--------|---------|------|
| 1 | أحادي: `not`, `-` | يمين ← يسار |
| 2 | `*`, `/`, `%` | يسار → يمين |
| 3 | `+`, `-` | يسار → يمين |
| 4 | `==`, `!=`, `<`, `<=`, `>`, `>=`, `in` | يسار → يمين |
| 5 | `and` | يسار → يمين |
| 6 | `or` | يسار → يمين |

### أمثلة:
```bayan
# بدون أقواس
result = 2 + 3 * 4      # 14 (ليس 20)

# مع أقواس
result = (2 + 3) * 4    # 20

# مع عوامل منطقية
result = True or False and False  # True (and له أولوية أعلى)
result = (True or False) and False  # False
```

---

## 6. العوامل المركبة (Compound Assignment)

**ملاحظة:** العوامل المركبة غير مدعومة حالياً، لكن يمكن محاكاتها:

```bayan
# بدلاً من: x += 5
x = x + 5

# بدلاً من: x *= 2
x = x * 2

# بدلاً من: x -= 3
x = x - 3
```

---

## 7. عمليات على السلاسل النصية (String Operations)

### الجمع (Concatenation):
```bayan
s1 = "مرحبا"
s2 = "عالم"
result = s1 + " " + s2  # "مرحبا عالم"
```

### الضرب (Repetition):
```bayan
s = "أ"
result = s * 3          # "ااا"
```

### الفهرسة (Indexing):
```bayan
s = "مرحبا"
print(s[0])             # "م"
print(s[1])             # "ر"
```

### العضوية (Membership):
```bayan
s = "مرحبا"
print("ح" in s)         # True
print("ع" in s)         # False
```

---

## 8. عمليات على القوائم (List Operations)

### الجمع:
```bayan
lst1 = [1, 2, 3]
lst2 = [4, 5, 6]
result = lst1 + lst2    # [1, 2, 3, 4, 5, 6]
```

### الضرب:
```bayan
lst = [1, 2]
result = lst * 3        # [1, 2, 1, 2, 1, 2]
```

### الفهرسة:
```bayan
lst = [10, 20, 30, 40]
print(lst[0])           # 10
print(lst[-1])          # 40 (آخر عنصر)
```

### التعديل:
```bayan
lst = [1, 2, 3]
lst[1] = 20             # [1, 20, 3]
```

### العضوية:
```bayan
lst = [1, 2, 3]
print(2 in lst)         # True
```

---

## 9. عمليات على القواميس (Dictionary Operations)

### الوصول:
```bayan
d = {"name": "أحمد", "age": 25}
print(d["name"])        # "أحمد"
```

### التعديل:
```bayan
d = {"name": "أحمد"}
d["age"] = 25           # {"name": "أحمد", "age": 25}
```

### العضوية:
```bayan
d = {"name": "أحمد", "age": 25}
print("name" in d)      # True
print("email" in d)     # False
```

---

## 10. الدوال السحرية للعوامل (Dunder Methods)

### حسابية:
```bayan
class Number:
{
    def __init__(val):
    {
        self.val = val
    }
    
    def __add__(other):
    {
        return Number(self.val + other.val)
    }
    
    def __sub__(other):
    {
        return Number(self.val - other.val)
    }
    
    def __mul__(other):
    {
        return Number(self.val * other.val)
    }
}

n1 = Number(5)
n2 = Number(3)
n3 = n1 + n2    # Number(8)
```

### مقارنات:
```bayan
class Number:
{
    def __eq__(other):
    {
        return self.val == other.val
    }
    
    def __lt__(other):
    {
        return self.val < other.val
    }
}
```

---

## 11. تحويل الأنواع (Type Conversion)

```bayan
# إلى نص
num = 42
text = str(num)         # "42"

# إلى عدد
text = "42"
num = int(text)         # 42

# إلى عشري
text = "3.14"
num = float(text)       # 3.14

# إلى منطقي
print(bool(1))          # True
print(bool(0))          # False
print(bool(""))         # False
print(bool("text"))     # True
```

---

## 12. الحقيقة والكذب (Truthiness)

```bayan
# قيم صادقة (Truthy)
if 1:           { print("صادق") }
if "text":      { print("صادق") }
if [1, 2]:      { print("صادق") }

# قيم كاذبة (Falsy)
if 0:           { print("كاذب") }
if "":          { print("كاذب") }
if []:          { print("كاذب") }
if None:        { print("كاذب") }
if False:       { print("كاذب") }
```

---

**آخر تحديث:** 2024-10-23

