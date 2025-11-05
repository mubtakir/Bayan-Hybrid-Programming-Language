# Bayan Architecture — التصميم والمعمارية

هذه وثيقة تصميم عالية المستوى تبين تدفّق التنفيذ والمكوّنات الأساسية، مع رسومات Mermaid لتوضيح العلاقات.

## نظرة عامة
- طبقة Lexing: تحويل النص إلى Tokens مع line/column.
- طبقة Parsing: بناء AST مع metadata (line, column, filename).
- طبقة Interpreting: تنفيذ تقليدي + تنفيذ منطقي + طبقة هجينة تجمعهما.
- نظام الاستيراد: تحميل وحدات بيان ثم محاولة بايثون، مع تخزين مؤقت.
- طبقة الأخطاء: Bayan stack + code frame (ألوان اختيارية، عرض-واعي للمحارف).

## مخطط تدفّق التنفيذ
```mermaid
flowchart LR
    S[Source Code] --> L[Lexer]
    L --> T[Tokens]
    T --> P[Parser]
    P --> AST[AST]
    AST --> H[HybridInterpreter]
    H --> TI[Traditional]
    H --> LI[Logical]
    TI --> OUT[(Result/Side-effects)]
    LI --> OUT
```

## طبقة المفسّر الهجين
- HybridInterpreter ينسّق بين المفسّر التقليدي والمنطقي.
- traditional_interpreter:
  - بيئات (global_env/local_env) ودوال وأصناف ونظام استيراد.
  - تتبّع call stack وإطارات أخطاء ملوّنة اختيارياً.
- logical_engine:
  - Term/Predicate/Fact/Rule + تنفيذ قواعد واستعلامات.

## علاقات فئات أساسية
```mermaid
classDiagram
    class HybridInterpreter {
        +interpret(ast)
        -traditional: TraditionalInterpreter
        -logical_engine: LogicalEngine
    }
    class TraditionalInterpreter {
        +interpret(node)
        +set_source(code, filename)
        +set_error_formatting(colors, context_lines, tabstop)
        -class_system: ClassSystem
        -import_system: ImportSystem
    }
    class ClassSystem {
        +instantiate(classdef)
        +mro(c)
    }
    class ImportSystem {
        +import(module)
        +from_import(module, names)
        -cache
    }
    class LogicalEngine {
        +assert_fact(f)
        +assert_rule(r)
        +query(q)
    }
    HybridInterpreter --> TraditionalInterpreter
    HybridInterpreter --> LogicalEngine
    TraditionalInterpreter --> ClassSystem
    TraditionalInterpreter --> ImportSystem
```

## تسلسل خطأ وتشخيص
```mermaid
sequenceDiagram
    participant User
    participant TI as TraditionalInterpreter
    participant CF as CodeFrame
    User->>TI: interpret(ast)
    TI->>TI: push (NodeType, line, col, file)
    TI-->>User: throws Exception
    TI->>TI: wrap into BayanRuntimeError (with Bayan stack)
    TI->>CF: build code frame (if source available)
    CF-->>TI: formatted frame
    TI-->>User: BayanRuntimeError + frame
```

## نقاط تصميم أساسية
- إرفاق (line, column, filename) بعُقد AST مبكراً من parser.
- بناء code frame حساس لعرض المحارف/tabstop مع تلوين ANSI اختيارياً.
- super() بدعم صيغتين مع تتبّع owner stack لسلامة MRO.
- بروتوكولات dunder لتكامل العوامل/الحاويات/التكرار/الاستدعاء.

## أفكار مستقبلية
- API تشغيل من سطر الأوامر (CLI) لملفات .bayan.
- Type checker اختياري.
- REPL تفاعلي مع إبراز نحوي.

انتهى.

