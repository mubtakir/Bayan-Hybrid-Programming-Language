# Bayan Language Architecture - معمارية لغة بيان

## Overview - نظرة عامة

Bayan is implemented as a complete interpreter with the following components:

1. **Lexer** - Tokenizes source code
2. **Parser** - Builds Abstract Syntax Tree (AST)
3. **Logical Engine** - Implements logical inference
4. **Traditional Interpreter** - Executes imperative code
5. **Hybrid Interpreter** - Combines both paradigms

## Component Details - تفاصيل المكونات

### Lexer (lexer.py)

The lexer tokenizes Bayan source code into tokens.

**Key Features:**
- Recognizes keywords (if, for, while, def, class, etc.)
- Handles logical operators (:-, ←)
- Supports logical variables (?X, ?Y)
- Recognizes Arabic identifiers
- Handles strings, numbers, and operators

**Token Types:**
- KEYWORD: if, for, while, def, class, etc.
- IDENTIFIER: variable and function names
- VARIABLE: logical variables (?X)
- NUMBER: integers and floats
- STRING: quoted strings
- OPERATOR: +, -, *, /, etc.
- LOGICAL: :-, ←, query, fact, rule

### Parser (parser.py)

The parser builds an Abstract Syntax Tree from tokens.

**Key Methods:**
- `parse()` - Main entry point
- `parse_statement()` - Parses individual statements
- `parse_expression()` - Parses expressions
- `parse_hybrid_block()` - Parses hybrid blocks
- `parse_logical_predicate()` - Parses logical predicates
- `parse_fact()` - Parses logical facts
- `parse_rule()` - Parses logical rules
- `parse_query()` - Parses logical queries

### Logical Engine (logical_engine.py)

Implements logical inference using unification and backtracking.

**Key Classes:**
- `Term` - Represents constants and variables
- `Predicate` - Represents logical predicates
- `Fact` - Represents logical facts
- `Rule` - Represents logical rules
- `Substitution` - Manages variable bindings
- `LogicalEngine` - Main inference engine

**Key Algorithms:**
- **Unification** - Pattern matching between terms
- **Backtracking** - Exploring multiple solutions
- **Variable Renaming** - Avoiding variable conflicts
- **Occurs Check** - Preventing infinite structures

### Traditional Interpreter (traditional_interpreter.py)

Executes imperative programming constructs.

**Supported Features:**
- Variable assignment
- Arithmetic operations
- Control flow (if/else, for, while)
- Function definitions and calls
- Class definitions
- List and dictionary operations
- Built-in functions

### Hybrid Interpreter (hybrid_interpreter.py)

Combines traditional and logical interpreters.

**Key Methods:**
- `visit_hybrid_block()` - Executes hybrid blocks
- `visit_logical_fact()` - Adds logical facts
- `visit_logical_rule()` - Adds logical rules
- `visit_logical_query()` - Executes logical queries

## Data Flow - تدفق البيانات

```
Source Code
    ↓
Lexer (tokenize)
    ↓
Tokens
    ↓
Parser (parse)
    ↓
AST (Abstract Syntax Tree)
    ↓
Hybrid Interpreter (interpret)
    ↓
Result
```

## AST Node Types - أنواع عقد AST

### Traditional Nodes
- `Program` - Root node
- `Assignment` - Variable assignment
- `BinaryOp` - Binary operations
- `UnaryOp` - Unary operations
- `IfStatement` - If/else statement
- `ForLoop` - For loop
- `WhileLoop` - While loop
- `FunctionDef` - Function definition
- `FunctionCall` - Function call
- `ClassDef` - Class definition
- `ReturnStatement` - Return statement

### Logical Nodes
- `LogicalFact` - Logical fact
- `LogicalRule` - Logical rule
- `LogicalQuery` - Logical query
- `LogicalPredicate` - Logical predicate

### Hybrid Nodes
- `HybridBlock` - Hybrid block
- `LogicalIfStatement` - If statement with logical condition
- `QueryExpression` - Query expression

## Execution Flow - تدفق التنفيذ

1. **Lexical Analysis** - Convert source code to tokens
2. **Syntax Analysis** - Build AST from tokens
3. **Semantic Analysis** - Validate AST (implicit)
4. **Interpretation** - Execute AST

## Key Algorithms - الخوارزميات الرئيسية

### Unification Algorithm

```
unify(term1, term2, substitution):
    term1 = deref(term1, substitution)
    term2 = deref(term2, substitution)
    
    if term1 == term2:
        return substitution
    
    if term1 is variable:
        if occurs_check(term1, term2):
            return None
        return bind(term1, term2, substitution)
    
    if term2 is variable:
        if occurs_check(term2, term1):
            return None
        return bind(term2, term1, substitution)
    
    if both are predicates:
        return unify_arguments(term1, term2, substitution)
    
    return None
```

### Backtracking Algorithm

```
solve_goal(goal, substitution):
    solutions = []
    
    for each fact/rule matching goal:
        if fact:
            new_sub = unify(goal, fact, substitution)
            if new_sub is not None:
                solutions.append(new_sub)
        
        if rule:
            head_sub = unify(goal, rule.head, substitution)
            if head_sub is not None:
                body_solutions = prove_body(rule.body, head_sub)
                solutions.extend(body_solutions)
    
    return solutions
```

## Performance Considerations - اعتبارات الأداء

1. **Variable Renaming** - Prevents variable conflicts but adds overhead
2. **Occurs Check** - Prevents infinite structures but adds overhead
3. **Backtracking** - Explores all solutions but can be slow
4. **Unification** - Core operation, optimized for performance

## Future Enhancements - التحسينات المستقبلية

1. Constraint solving
2. Tabling/memoization
3. Cut operator (!)
4. Assert/retract for dynamic predicates
5. Module system
6. Debugging support
7. Performance optimization


