# 🌟 Bayan - Hybrid Programming Language | لغة البيان

<div align="center">

![Bayan Language](https://img.shields.io/badge/Bayan-Hybrid%20Language-blue?style=for-the-badge)
![Tests](https://img.shields.io/badge/tests-267%20passing-green?style=for-the-badge)
![Arabic Support](https://img.shields.io/badge/Arabic-Fully%20Supported-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**The World's First True Hybrid Programming Language**  
**أول لغة برمجة هجينة حقيقية في العالم**

[English](#english) | [العربية](#arabic)

</div>

---

<a name="english"></a>

## 🎯 What is Bayan?

**Bayan** (البيان) is a revolutionary hybrid programming language that seamlessly combines **three programming paradigms** in one unified syntax:

1. **Imperative Programming** - Traditional procedural code
2. **Object-Oriented Programming (OOP)** - Classes, inheritance, polymorphism
3. **Logic Programming** - Prolog-style facts, rules, and queries

### 🌟 Key Features

- ✅ **Three Paradigms in One** - Switch between imperative, OOP, and logic programming seamlessly
- ✅ **Bilingual Keywords** - Full support for both Arabic and English keywords
- ✅ **Arabic Text Support** - Perfect handling of Arabic text without external libraries
- ✅ **Modern Features** - Async/await, generators, decorators, context managers
- ✅ **AI/ML Ready** - Built-in functions for data science and machine learning
- ✅ **Dynamic Knowledge Base** - Assert and retract facts at runtime
- ✅ **100% Test Coverage** - 267 passing tests
- ✅ **Comprehensive Documentation** - 5,594+ lines of tutorials and guides
- ✅ **LLM Integration** - Ready-to-use prompts for ChatGPT, Claude, and other AI models

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/mubtakir/Bayan-Hybrid-Programming-Language.git
cd Bayan-Hybrid-Programming-Language
```

### Hello World

```bayan
hybrid {
    print("Hello, World!")
    print("مرحباً بالعالم!")
}
```

### Run it

```bash
python -m bayan examples/hello.by
```

---

## 💡 Examples

### 1. Imperative Programming

```bayan
hybrid {
    # Variables and operations
    x = 10
    y = 20
    sum = x + y
    print("Sum: " + str(sum))
    
    # Control flow
    if sum > 25: {
        print("Large sum")
    }
    
    # Loops
    for i in range(5): {
        print("Number: " + str(i))
    }
}
```

### 2. Object-Oriented Programming

```bayan
hybrid {
    class Person: {
        def __init__(self, name, age): {
            self.name = name
            self.age = age
        }
        
        def greet(self): {
            return "Hello, I am " + self.name
        }
    }
    
    person = Person("أحمد", 25)
    print(person.greet())
}
```

### 3. Logic Programming

```bayan
hybrid {
    # Facts
    parent("أحمد", "محمد").
    parent("أحمد", "فاطمة").
    parent("علي", "سارة").
    
    # Rules
    sibling(?X, ?Y) :- parent(?P, ?X), parent(?P, ?Y), ?X != ?Y.
    
    # Query
    results = query sibling("محمد", ?S)?
    
    for result in results: {
        print("Sibling: " + result["?S"])
    }
}
```

### 4. Hybrid Programming (All Three!)

```bayan
hybrid {
    # OOP: Define a Student class
    class Student: {
        def __init__(self, name, grade): {
            self.name = name
            self.grade = grade
            
            # Logic: Add to knowledge base
            assertz(student(name, grade))
        }
    }
    
    # Imperative: Create students
    students = [
        Student("أحمد", 85),
        Student("فاطمة", 95),
        Student("علي", 92)
    ]
    
    # Logic: Query excellent students
    results = query student(?N, ?G), ?G >= 90?
    
    # Imperative: Print results
    print("Excellent students:")
    for result in results: {
        print("  - " + result["?N"] + ": " + str(result["?G"]))
    }
}
```

---

## 📚 Documentation

### Tutorials (Arabic)
- [Part 1: Introduction](docs/01_INTRODUCTION_AR.md) - What is Bayan, features, installation
- [Part 2: Procedural & OOP](docs/02_PROCEDURAL_OOP_AR.md) - From beginner to expert
- [Part 3: Logic Programming](docs/03_LOGIC_PROGRAMMING_AR.md) - Prolog-style programming

### LLM Integration
- [LLM System Prompt](docs/LLM_SYSTEM_PROMPT.txt) - Ready-to-use prompt for AI models
- [LLM Quick Reference](docs/LLM_QUICK_REFERENCE.md) - Quick syntax reference
- [LLM Complete Guide](docs/LLM_REFERENCE_GUIDE.md) - Comprehensive guide with 10 examples
- [How to Use with LLMs](docs/HOW_TO_USE_WITH_LLMS.md) - Complete usage guide

### Technical Documentation
- [Language Guide](docs/LANGUAGE_GUIDE.md) - Complete language reference
- [Architecture](docs/ARCHITECTURE.md) - Internal architecture
- [Examples](docs/EXAMPLES.md) - Advanced examples
- [Arabic Text Support](docs/ARABIC_TEXT_SUPPORT.md) - How Arabic text works

---

## 🧪 Testing

Run all tests:

```bash
python -m pytest tests/ -v
```

**Result**: 267 tests passing (100% success rate) ✅

---

## 🌍 Use Cases

- **Education** - Teach multiple programming paradigms in one language
- **AI/ML** - Logic programming + imperative for expert systems
- **Arabic Software** - Build software with Arabic keywords and perfect text handling
- **Research** - Explore hybrid programming paradigms
- **Rapid Prototyping** - Use the best paradigm for each part of your code

---

## 📊 Statistics

- **154 files** in the repository
- **41,889 lines** of code and documentation
- **267 tests** (100% passing)
- **5,594+ lines** of tutorials and guides
- **10+ complete examples**
- **3 programming paradigms** in one language

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Developed by: Basel Yahya Abdullah (باسل يحيى عبدالله)**  
**With assistance from: AI Language Models**

---

## 🙏 Acknowledgments

- Thanks to the open-source community
- Inspired by Python, Prolog, and modern programming languages
- Built for the global programming competition

---

## 📞 Contact

- GitHub: [@mubtakir](https://github.com/mubtakir)
- Repository: [Bayan-Hybrid-Programming-Language](https://github.com/mubtakir/Bayan-Hybrid-Programming-Language)

---

<a name="arabic"></a>

<div dir="rtl">

## 🎯 ما هي لغة البيان؟

**البيان** هي لغة برمجة هجينة ثورية تجمع بسلاسة بين **ثلاثة أنماط برمجية** في صيغة موحدة:

1. **البرمجة الإجرائية** - الكود الإجرائي التقليدي
2. **البرمجة الكائنية (OOP)** - الأصناف، الوراثة، تعدد الأشكال
3. **البرمجة المنطقية** - الحقائق والقواعد والاستعلامات بأسلوب Prolog

### 🌟 المزايا الرئيسية

- ✅ **ثلاثة أنماط في واحد** - التبديل بين الإجرائية والكائنية والمنطقية بسلاسة
- ✅ **كلمات مفتاحية ثنائية اللغة** - دعم كامل للكلمات المفتاحية العربية والإنجليزية
- ✅ **دعم النصوص العربية** - معالجة مثالية للنصوص العربية بدون مكتبات خارجية
- ✅ **ميزات حديثة** - Async/await، Generators، Decorators، Context Managers
- ✅ **جاهزة للذكاء الاصطناعي** - دوال مدمجة لعلوم البيانات والتعلم الآلي
- ✅ **قاعدة معرفة ديناميكية** - إضافة وحذف الحقائق أثناء التشغيل
- ✅ **تغطية اختبارات 100%** - 267 اختبار ناجح
- ✅ **وثائق شاملة** - 5,594+ سطر من الدروس والأدلة
- ✅ **تكامل مع النماذج اللغوية** - Prompts جاهزة لـ ChatGPT وClaude وغيرها

---

## 🚀 البدء السريع

### التثبيت

```bash
git clone https://github.com/mubtakir/Bayan-Hybrid-Programming-Language.git
cd Bayan-Hybrid-Programming-Language
```

### مرحباً بالعالم

```bayan
hybrid {
    print("مرحباً بالعالم!")
    print("Hello, World!")
}
```

### التشغيل

```bash
python -m bayan examples/hello.by
```

---

## 📚 الوثائق

### الدروس التعليمية
- [الجزء الأول: مقدمة](docs/01_INTRODUCTION_AR.md) - ما هي البيان، المزايا، التثبيت
- [الجزء الثاني: الإجرائية والكائنية](docs/02_PROCEDURAL_OOP_AR.md) - من المبتدئ إلى الخبير
- [الجزء الثالث: البرمجة المنطقية](docs/03_LOGIC_PROGRAMMING_AR.md) - البرمجة بأسلوب Prolog

### التكامل مع النماذج اللغوية
- [System Prompt للنماذج](docs/LLM_SYSTEM_PROMPT.txt) - Prompt جاهز للاستخدام
- [مرجع سريع](docs/LLM_QUICK_REFERENCE.md) - مرجع سريع للصيغة
- [دليل شامل](docs/LLM_REFERENCE_GUIDE.md) - دليل شامل مع 10 أمثلة
- [كيفية الاستخدام مع النماذج](docs/HOW_TO_USE_WITH_LLMS.md) - دليل الاستخدام الكامل

---

## 🧪 الاختبارات

تشغيل جميع الاختبارات:

```bash
python -m pytest tests/ -v
```

**النتيجة**: 267 اختبار ناجح (100% نجاح) ✅

---

## 👨‍💻 المطور

**تم التطوير بواسطة: باسل يحيى عبدالله**  
**بمساعدة: نماذج الذكاء الاصطناعي اللغوية**

---

## 📞 التواصل

- GitHub: [@mubtakir](https://github.com/mubtakir)
- المستودع: [Bayan-Hybrid-Programming-Language](https://github.com/mubtakir/Bayan-Hybrid-Programming-Language)

---

**🌟 لغة البيان - اللغة الوحيدة التي تجمع ثلاثة أنماط برمجية! 🌟**

</div>

