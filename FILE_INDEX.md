# فهرس الملفات - File Index
## لغة البيان - Bayan Programming Language

---

## نظرة عامة | Overview

هذا المجلد يحتوي على **نسخة كاملة ومستقلة** من لغة البيان البرمجية، جاهزة للتقديم والتقييم.

This folder contains a **complete and standalone copy** of the Bayan programming language, ready for submission and evaluation.

---

## الإحصائيات | Statistics

- **ملفات Python**: 28 ملف
- **ملفات Bayan**: 30 ملف (.by, .bayan)
- **ملفات التوثيق**: 15+ ملف
- **إجمالي الاختبارات**: 79 اختبار
- **معدل النجاح**: 100% ✅

---

## البنية الهيكلية | Directory Structure

```
bayan_python/
│
├── 📄 README.md                    # الدليل الرئيسي | Main Guide
├── 📄 EVALUATION_GUIDE.md          # دليل التقييم | Evaluation Guide
├── 📄 FILE_INDEX.md                # هذا الملف | This File
│
├── 📁 bayan/                       # المفسر الرئيسي | Main Interpreter
│   ├── main.py                    # نقطة الدخول | Entry Point
│   ├── myutils.py                 # أدوات مساعدة | Utilities
│   │
│   └── 📁 bayan/                   # الكود المصدري | Source Code
│       ├── __init__.py
│       ├── lexer.py               # المحلل اللغوي | Lexer (~500 lines)
│       ├── parser.py              # محلل الجملة | Parser (~600 lines)
│       ├── ast_nodes.py           # عقد الشجرة | AST Nodes (~300 lines)
│       ├── traditional_interpreter.py  # المفسر التقليدي (~400 lines)
│       ├── hybrid_interpreter.py       # المفسر الهجين (~120 lines)
│       ├── logical_engine.py           # المحرك المنطقي (~400 lines)
│       ├── object_system.py            # النظام الكائني (~200 lines)
│       ├── import_system.py            # نظام الاستيراد (~150 lines)
│       └── builtins.py                 # الدوال المدمجة (~100 lines)
│
├── 📁 tests/                       # الاختبارات | Tests (79 tests)
│   ├── __init__.py
│   ├── test_lexer.py              # اختبارات المحلل اللغوي (9 tests)
│   ├── test_traditional_interpreter.py  # (13 tests)
│   ├── test_hybrid_interpreter.py       # (11 tests)
│   ├── test_logical_engine.py           # (9 tests)
│   ├── test_oop.py                      # (5 tests)
│   ├── test_inheritance.py              # (3 tests)
│   ├── test_multiple_inheritance.py     # (3 tests)
│   ├── test_imports.py                  # (9 tests)
│   ├── test_bayan_modules.py            # (9 tests)
│   ├── test_error_reporting.py          # (6 tests)
│   ├── test_dunder_extras.py            # (5 tests)
│   ├── test_indexing.py                 # (2 tests)
│   ├── test_super_syntax.py
│   │
│   └── 📁 bayan_modules/          # وحدات اختبارية | Test Modules
│       ├── math_utils.by
│       ├── string_utils.by
│       └── logic_utils.by
│
├── 📁 examples/                    # أمثلة تطبيقية | Examples
│   ├── family.by                  # مثال العائلة والعلاقات المنطقية
│   ├── calculator.by              # آلة حاسبة كائنية
│   ├── showcase.bayan             # عرض شامل للميزات
│   ├── python_integration.bayan   # التكامل مع Python
│   └── myutils.py                 # أدوات مساعدة للأمثلة
│
├── 📁 bayan_solutions/            # حلول متقدمة | Advanced Solutions
│   ├── linguistic_equations.by    # معادلات لغوية
│   ├── shape_equations.by         # معادلات الأشكال
│   ├── information_equations.by   # معادلات المعلومات
│   ├── logical_inference.by       # الاستدلال المنطقي
│   ├── event_processing.by        # معالجة الأحداث
│   ├── knowledge_management.by    # إدارة المعرفة
│   ├── semantic_networks.by       # الشبكات الدلالية
│   ├── morphosyntactic_rules.by   # قواعد صرفية نحوية
│   ├── arabic_letters_database.by # قاعدة بيانات الحروف العربية
│   ├── english_letters_database.by
│   ├── expert_knowledge_base.by   # قاعدة معرفة الخبراء
│   ├── object_definitions.by      # تعريفات الكائنات
│   ├── operator_definitions.by    # تعريفات المعاملات
│   ├── specialized_databases.by   # قواعد بيانات متخصصة
│   ├── test_simple.by
│   ├── test_linguistic.by
│   ├── test_multiline_strings.by
│   ├── test_string_escapes.by
│   ├── test_list_comprehensions.by
│   ├── test_exceptions.by
│   └── test_default_and_named_parameters.by
│
├── 📁 docs/                       # التوثيق الكامل | Documentation
│   ├── basics.md                 # الأساسيات
│   ├── reference.md              # المرجع الكامل
│   ├── architecture.md           # البنية المعمارية
│   ├── developer_guide.md        # دليل المطورين
│   ├── classes_and_inheritance.md
│   ├── operators_and_operations.md
│   ├── hybrid_logic_advanced.md
│   ├── default_and_named_parameters.md
│   ├── advanced_features.md
│   ├── cookbook.md
│   ├── executable.md
│   ├── incomplete_features.md
│   └── implementation_guide_parameters.md
│
└── 📁 scripts/                    # سكريبتات مساعدة | Helper Scripts
    └── bayan_run.py              # سكريبت تشغيل

```

---

## الملفات الرئيسية | Main Files

### 1. الكود المصدري | Source Code

#### المحلل اللغوي | Lexer
- **`bayan/bayan/lexer.py`** (~500 سطر)
  - تحليل الكود إلى رموز (Tokens)
  - دعم Unicode للعربية
  - معالجة السلاسل النصية والتعليقات
  - المتغيرات المنطقية (?X)

#### المحلل النحوي | Parser
- **`bayan/bayan/parser.py`** (~600 سطر)
  - بناء شجرة AST
  - معلومات الموقع (line, column)
  - معالجة الأخطاء النحوية
  - دعم جميع التراكيب البرمجية

#### عقد الشجرة | AST Nodes
- **`bayan/bayan/ast_nodes.py`** (~300 سطر)
  - تعريفات جميع عقد AST
  - Program, Statement, Expression
  - Class, Function, Variable
  - LogicalFact, LogicalRule, Query

#### المفسر التقليدي | Traditional Interpreter
- **`bayan/bayan/traditional_interpreter.py`** (~400 سطر)
  - تنفيذ البرمجة الإجرائية
  - البرمجة الكائنية
  - معالجة الاستثناءات
  - Stack traces

#### المفسر الهجين | Hybrid Interpreter
- **`bayan/bayan/hybrid_interpreter.py`** (~120 سطر)
  - دمج البرمجة التقليدية والمنطقية
  - تنسيق التنفيذ
  - مشاركة البيئات

#### المحرك المنطقي | Logical Engine
- **`bayan/bayan/logical_engine.py`** (~400 سطر)
  - خوارزمية التوحيد (Unification)
  - التراجع (Backtracking)
  - معالجة الحقائق والقواعد
  - الاستعلامات

#### النظام الكائني | Object System
- **`bayan/bayan/object_system.py`** (~200 سطر)
  - إدارة الفئات والكائنات
  - خوارزمية C3 MRO
  - الوراثة المتعددة
  - Dunder methods

#### نظام الاستيراد | Import System
- **`bayan/bayan/import_system.py`** (~150 سطر)
  - استيراد وحدات Python (قائمة آمنة)
  - استيراد وحدات Bayan
  - التخزين المؤقت

#### الدوال المدمجة | Built-in Functions
- **`bayan/bayan/builtins.py`** (~100 سطر)
  - print, len, range, type
  - str, int, float, bool
  - list, dict
  - وغيرها...

---

### 2. الاختبارات | Tests (79 tests total)

- **test_lexer.py** - 9 اختبارات للمحلل اللغوي
- **test_traditional_interpreter.py** - 13 اختبار للمفسر التقليدي
- **test_hybrid_interpreter.py** - 11 اختبار للمفسر الهجين
- **test_logical_engine.py** - 9 اختبارات للمحرك المنطقي
- **test_oop.py** - 5 اختبارات للبرمجة الكائنية
- **test_inheritance.py** - 3 اختبارات للوراثة
- **test_multiple_inheritance.py** - 3 اختبارات للوراثة المتعددة
- **test_imports.py** - 9 اختبارات لنظام الاستيراد
- **test_bayan_modules.py** - 9 اختبارات لوحدات Bayan
- **test_error_reporting.py** - 6 اختبارات لمعالجة الأخطاء
- **test_dunder_extras.py** - 5 اختبارات لـ Dunder methods
- **test_indexing.py** - 2 اختبار للفهرسة
- **test_super_syntax.py** - اختبارات super()

---

### 3. الأمثلة | Examples

#### أمثلة أساسية | Basic Examples
- **family.by** - مثال العائلة (برمجة منطقية)
- **calculator.by** - آلة حاسبة (برمجة كائنية)
- **showcase.bayan** - عرض شامل للميزات
- **python_integration.bayan** - التكامل مع Python

#### حلول متقدمة | Advanced Solutions
- **linguistic_equations.by** - معادلات لغوية
- **shape_equations.by** - معادلات الأشكال
- **logical_inference.by** - استدلال منطقي
- **semantic_networks.by** - شبكات دلالية
- **morphosyntactic_rules.by** - قواعد صرفية نحوية
- وغيرها... (30 ملف)

---

### 4. التوثيق | Documentation

- **basics.md** - دليل الأساسيات للمبتدئين
- **reference.md** - المرجع الكامل للغة
- **architecture.md** - البنية المعمارية للنظام
- **developer_guide.md** - دليل المطورين
- **classes_and_inheritance.md** - الفئات والوراثة
- **operators_and_operations.md** - المعاملات والعمليات
- **hybrid_logic_advanced.md** - البرمجة الهجينة المتقدمة
- وغيرها...

---

## كيفية الاستخدام | How to Use

### 1. تشغيل برنامج | Run a Program
```bash
cd bayan
python main.py examples/family.by
```

### 2. الوضع التفاعلي | Interactive Mode
```bash
cd bayan
python main.py
```

### 3. تشغيل الاختبارات | Run Tests
```bash
cd bayan
python -m pytest tests/ -v
```

### 4. تشغيل اختبار محدد | Run Specific Test
```bash
cd bayan
python -m pytest tests/test_oop.py -v
```

---

## ملاحظات مهمة | Important Notes

1. ✅ **جميع الملفات منسوخة** من المشروع الأصلي
2. ✅ **المجلد مستقل تماماً** ويمكن نقله أو أرشفته
3. ✅ **جميع الاختبارات تعمل** بنسبة نجاح 100%
4. ✅ **التوثيق كامل** بالعربية والإنجليزية
5. ✅ **جاهز للتقديم** للجنة التقييم

---

## للمزيد من المعلومات | For More Information

- اقرأ **README.md** للنظرة العامة
- اقرأ **EVALUATION_GUIDE.md** لدليل التقييم
- راجع **docs/** للتوثيق الكامل
- جرب **examples/** للأمثلة التطبيقية
- ادرس **tests/** لفهم الاختبارات

---

**تم إعداد هذا المجلد خصيصاً لتقديم لغة البيان للجنة التقييم المختصة بلغات البرمجة**

**This folder has been specially prepared to present the Bayan language to the programming languages evaluation committee**

