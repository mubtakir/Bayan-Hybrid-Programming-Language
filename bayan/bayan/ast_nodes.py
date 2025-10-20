"""
Abstract Syntax Tree (AST) nodes for Bayan Language
عقد شجرة التجريد للغة بيان
"""

class ASTNode:
    """Base class for all AST nodes with optional source position"""
    line = None
    column = None
    filename = None

    def with_pos(self, line=None, column=None, filename=None):
        self.line = line
        self.column = column
        self.filename = filename
        return self

# ============ Traditional Programming Nodes ============

class Program(ASTNode):
    """Root node of the program"""
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program({len(self.statements)} statements)"

class Block(ASTNode):
    """A block of statements"""
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({len(self.statements)} statements)"

class Assignment(ASTNode):
    """Variable assignment: x = 5"""
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Assignment({self.name}, {self.value})"

class BinaryOp(ASTNode):
    """Binary operation: a + b"""
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.operator}, {self.left}, {self.right})"

class UnaryOp(ASTNode):
    """Unary operation: -x, not x"""
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"UnaryOp({self.operator}, {self.operand})"

class Number(ASTNode):
    """Numeric literal"""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"

class String(ASTNode):
    """String literal"""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"String({repr(self.value)})"

class Boolean(ASTNode):
    """Boolean literal"""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Boolean({self.value})"

class Variable(ASTNode):
    """Variable reference"""
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Variable({self.name})"

class List(ASTNode):
    """List literal: [1, 2, 3]"""
    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return f"List({len(self.elements)} elements)"

class Dict(ASTNode):
    """Dictionary literal: {key: value}"""
    def __init__(self, pairs):
        self.pairs = pairs  # List of (key, value) tuples

    def __repr__(self):
        return f"Dict({len(self.pairs)} pairs)"

class FunctionCall(ASTNode):
    """Function call: func(arg1, arg2)"""
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f"FunctionCall({self.name}, {len(self.arguments)} args)"

class FunctionDef(ASTNode):
    """Function definition"""
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"FunctionDef({self.name}, {len(self.parameters)} params)"

class ClassDef(ASTNode):
    """Class definition"""
    def __init__(self, name, base_class, body, base_classes=None):
        self.name = name
        # Backward-compat single base
        self.base_class = base_class
        # New: support multiple bases
        self.base_classes = base_classes
        self.body = body

    def __repr__(self):
        return f"ClassDef({self.name})"

class ObjectInstance(ASTNode):
    """Object instance"""
    def __init__(self, class_name, arguments):
        self.class_name = class_name
        self.arguments = arguments

    def __repr__(self):
        return f"ObjectInstance({self.class_name})"

class AttributeAccess(ASTNode):
    """Attribute access (obj.attr)"""
    def __init__(self, object_expr, attribute_name):
        self.object_expr = object_expr
        self.attribute_name = attribute_name

    def __repr__(self):
        return f"AttributeAccess({self.attribute_name})"

class MethodCall(ASTNode):
    """Method call (obj.method())"""
    def __init__(self, object_expr, method_name, arguments):
        self.object_expr = object_expr
        self.method_name = method_name
        self.arguments = arguments

    def __repr__(self):
        return f"MethodCall({self.method_name})"

class SubscriptAccess(ASTNode):
    """Indexing access (obj[index])"""
    def __init__(self, object_expr, index_expr):
        self.object_expr = object_expr
        self.index_expr = index_expr

    def __repr__(self):
        return "SubscriptAccess([])"

class AttributeAssignment(ASTNode):
    """Attribute assignment: obj.attr = value"""
    def __init__(self, object_expr, attribute_name, value):
        self.object_expr = object_expr
        self.attribute_name = attribute_name
        self.value = value

    def __repr__(self):
        return f"AttributeAssignment({self.attribute_name})"

class SubscriptAssignment(ASTNode):
    """Subscript assignment: obj[index] = value"""
    def __init__(self, object_expr, index_expr, value):
        self.object_expr = object_expr
        self.index_expr = index_expr
        self.value = value

    def __repr__(self):
        return "SubscriptAssignment([])"

class SelfReference(ASTNode):
    """Self reference"""
    def __init__(self):
        pass

    def __repr__(self):
        return "SelfReference()"

class SuperCall(ASTNode):
    """Super call for parent class"""
    def __init__(self, method_name, arguments):
        self.method_name = method_name
        self.arguments = arguments

    def __repr__(self):
        return f"SuperCall({self.method_name})"

class ImportStatement(ASTNode):
    """Import statement"""
    def __init__(self, module_name, alias=None):
        self.module_name = module_name
        self.alias = alias

    def __repr__(self):
        return f"ImportStatement({self.module_name})"

class FromImportStatement(ASTNode):
    """From ... import statement"""
    def __init__(self, module_name, names, aliases=None):
        self.module_name = module_name
        self.names = names
        self.aliases = aliases or []

    def __repr__(self):
        return f"FromImportStatement({self.module_name})"

class IfStatement(ASTNode):
    """If statement"""
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"IfStatement(condition, then, else={self.else_branch is not None})"

class ForLoop(ASTNode):
    """For loop"""
    def __init__(self, variable, iterable, body):
        self.variable = variable
        self.iterable = iterable
        self.body = body

    def __repr__(self):
        return f"ForLoop({self.variable}, iterable, body)"

class WhileLoop(ASTNode):
    """While loop"""
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileLoop(condition, body)"

class ReturnStatement(ASTNode):
    """Return statement"""
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return f"ReturnStatement({self.value})"

class BreakStatement(ASTNode):
    """Break statement"""
    def __repr__(self):
        return "BreakStatement()"

class ContinueStatement(ASTNode):
    """Continue statement"""
    def __repr__(self):
        return "ContinueStatement()"

class PrintStatement(ASTNode):
    """Print statement"""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"PrintStatement({self.value})"

# ============ Logical Programming Nodes ============

class LogicalFact(ASTNode):
    """Logical fact: parent(john, mary)."""
    def __init__(self, predicate):
        self.predicate = predicate

    def __repr__(self):
        return f"LogicalFact({self.predicate})"

class LogicalRule(ASTNode):
    """Logical rule: grandparent(X, Z) :- parent(X, Y), parent(Y, Z)."""
    def __init__(self, head, body):
        self.head = head
        self.body = body  # List of predicates

    def __repr__(self):
        return f"LogicalRule({self.head} :- ...)"

class LogicalQuery(ASTNode):
    """Logical query: ?- parent(X, john)."""
    def __init__(self, goal):
        self.goal = goal

    def __repr__(self):
        return f"LogicalQuery({self.goal})"

class LogicalPredicate(ASTNode):
    """Logical predicate: parent(X, Y)"""
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f"LogicalPredicate({self.name}/{len(self.arguments)})"

class LogicalVariable(ASTNode):
    """Logical variable: ?X, ?Y"""
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"LogicalVariable(?{self.name})"

class LogicalConstant(ASTNode):
    """Logical constant: atom, number, string"""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"LogicalConstant({self.value})"

class LogicalConjunction(ASTNode):
    """Logical AND: goal1, goal2"""
    def __init__(self, goals):
        self.goals = goals

    def __repr__(self):
        return f"LogicalConjunction({len(self.goals)} goals)"

class LogicalDisjunction(ASTNode):
    """Logical OR: goal1; goal2"""
    def __init__(self, goals):
        self.goals = goals

    def __repr__(self):
        return f"LogicalDisjunction({len(self.goals)} goals)"

class LogicalNegation(ASTNode):
    """Logical NOT: \\+ goal"""
    def __init__(self, goal):
        self.goal = goal

    def __repr__(self):
        return f"LogicalNegation({self.goal})"

# ============ Hybrid Nodes ============

class HybridBlock(ASTNode):
    """Hybrid block combining traditional and logical code"""
    def __init__(self, traditional_stmts, logical_stmts):
        self.traditional_stmts = traditional_stmts
        self.logical_stmts = logical_stmts

    def __repr__(self):
        return f"HybridBlock({len(self.traditional_stmts)} trad, {len(self.logical_stmts)} logical)"

class LogicalIfStatement(ASTNode):
    """If statement with logical condition"""
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition  # Can be a logical query
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"LogicalIfStatement(condition, then, else={self.else_branch is not None})"

class QueryExpression(ASTNode):
    """Query expression in traditional code: query parent(?X, john)"""
    def __init__(self, goal):
        self.goal = goal

    def __repr__(self):
        return f"QueryExpression({self.goal})"

