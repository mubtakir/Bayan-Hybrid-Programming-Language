"""
Traditional Interpreter for Bayan Language
مفسر تقليدي للغة بيان
"""

from .ast_nodes import *
from .object_system import ClassSystem, BayanObject
from .import_system import ImportSystem

class ReturnValue(Exception):
    """Exception to handle return statements"""
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    """Exception to handle break statements"""
    pass

class ContinueException(Exception):
    """Exception to handle continue statements"""
    pass
class BayanRuntimeError(Exception):
    """Runtime error that carries a Bayan stack trace"""
    pass


class TraditionalInterpreter:
    """Interpreter for traditional programming constructs"""

    def __init__(self):
        self.global_env = {}
        self.local_env = None
        self.functions = {}
        self.classes = {}
        self.class_system = ClassSystem(self)
        self.import_system = ImportSystem()
        self.logical_engine = None
        # Track current owner class for super() resolution in MRO
        self._owner_stack = []
        # Bayan runtime call stack of (node_type, line, column, filename)
        self._call_stack = []
        # Optional source buffer for code-frame rendering
        self._source_lines = None
        self._source_filename = None

        # Error reporting configuration
        self._err_color = False
        self._err_context_lines = 1
        self._err_tabstop = 4

    def set_source(self, code: str, filename: str | None = None):
        """Set current source buffer for error code-frames."""
        # Normalize line endings and keep lines including spaces
        self._source_lines = code.splitlines()
        self._source_filename = filename

    def set_error_formatting(self, *, colors: bool | None = None, context_lines: int | None = None, tabstop: int | None = None):
        """Configure error display options.
        - colors: enable ANSI color output
        - context_lines: number of lines before/after the error line to show
        - tabstop: tab width for caret alignment
        """
        if colors is not None:
            self._err_color = bool(colors)
        if context_lines is not None and context_lines >= 0:
            self._err_context_lines = int(context_lines)
        if tabstop is not None and tabstop >= 1:
            self._err_tabstop = int(tabstop)

    def _truthy(self, value):
        """Bayan truthiness: use __bool__ or __len__ on BayanObject if available."""
        if isinstance(value, BayanObject):
            if value.has_method('__bool__'):
                try:
                    res = value.call_method('__bool__', [])
                    return bool(res)
                except Exception:
                    return True
            if value.has_method('__len__'):
                try:
                    res = value.call_method('__len__', [])
                    return bool(res)
                except Exception:
                    return True
            return True
        return bool(value)

    def _to_iterable(self, obj):
        """Convert BayanObject with __iter__ into a Python iterable if possible."""
        if isinstance(obj, BayanObject):
            if obj.has_method('__iter__'):
                it = obj.call_method('__iter__', [])
                return self._to_iterable(it)
            else:
                raise TypeError("Object is not iterable")
        return obj

    def interpret(self, node):
        """Interpret an AST node with Bayan stack tracking"""
        # Push current frame (node type + optional position)
        self._call_stack.append((type(node).__name__, getattr(node, 'line', None), getattr(node, 'column', None), getattr(node, 'filename', None)))
        try:
            return self._interpret_core(node)
        except Exception as e:
            # Control-flow exceptions should not be wrapped
            if isinstance(e, (ReturnValue, BreakException, ContinueException, BayanRuntimeError)):
                raise
            frames = list(self._call_stack)
            trace = " -> ".join(
                (f"{name}@{fn}:{ln}:{col}" if fn else f"{name}@{ln}:{col}") if ln is not None else name
                for (name, ln, col, fn) in frames
            )
            # Try to add a code-frame for the most recent frame with position
            code_frame = ""
            try:
                for (name, ln, col, fn) in reversed(frames):
                    if ln is not None and col is not None:
                        # Only render frame if we have a matching source buffer
                        if self._source_lines is not None and (self._source_filename == fn or self._source_filename is None):
                            code_frame = self._build_code_frame(fn, int(ln), int(col))
                        break
            except Exception:
                # Never fail error reporting
                code_frame = ""
            raise BayanRuntimeError(f"{e.__class__.__name__}: {e}\nBayan stack: {trace}{code_frame}")
        finally:
            self._call_stack.pop()


    def _style(self, text: str, *kinds: str) -> str:
        if not self._err_color:
            return text
        code_map = {
            'dim': '2',
            'bold': '1',
            'red': '31',
            'cyan': '36',
        }
        codes = [code_map.get(k) for k in kinds if code_map.get(k)]
        if not codes:
            return text
        start = "\x1b[" + ";".join(codes) + "m"
        end = "\x1b[0m"
        return f"{start}{text}{end}"

    def _display_width(self, s: str, tabstop: int = 4) -> int:
        import unicodedata
        w = 0
        for ch in s:
            if ch == '\t':
                w += tabstop - (w % tabstop)
            elif unicodedata.combining(ch):
                continue
            else:
                ea = unicodedata.east_asian_width(ch)
                w += 2 if ea in ('W', 'F') else 1
        return w

    def _caret_indent_for(self, s: str, col_char_index_1based: int) -> str:
        # Compute display width up to character index col-1 (1-based char index)
        prefix = s[:max(0, col_char_index_1based - 1)]
        spaces = self._display_width(prefix, tabstop=self._err_tabstop)
        return ' ' * max(0, spaces)

    def _build_code_frame(self, filename: str | None, line: int, col: int) -> str:
        """Return a numbered code frame with caret.
        - Shows ±context_lines around the error
        - Highlights current line with '>' and optional ANSI colors
        """
        if self._source_lines is None:
            return ''
        file_label = filename if filename is not None else (self._source_filename if self._source_filename else '<memory>')
        start = max(1, line - self._err_context_lines)
        end = min(len(self._source_lines), line + self._err_context_lines)
        pad = len(str(end))
        header = f"\n\nFile {file_label}:{line}:{col}"
        if self._err_color:
            header = self._style(header, 'dim')
        lines_out = [header]
        for i in range(start, end + 1):
            text = self._source_lines[i - 1]
            prefix = '>' if i == line else ' '
            numbered = f"{prefix}{str(i).rjust(pad)} | {text}"
            if self._err_color:
                if i == line:
                    numbered = self._style(numbered, 'bold')
                else:
                    numbered = self._style(numbered, 'dim')
            lines_out.append(numbered)
            if i == line:
                caret_indent = self._caret_indent_for(text, col)
                caret = '^'
                if self._err_color:
                    caret = self._style(caret, 'red', 'bold')
                lines_out.append(' ' * (1 + pad + 3) + caret_indent + caret)
        return '\n'.join(lines_out)

    def _interpret_core(self, node):
        """Core interpret dispatch without stack handling"""
        if isinstance(node, Program):
            return self.visit_program(node)
        elif isinstance(node, Block):
            return self.visit_block(node)
        elif isinstance(node, Assignment):
            return self.visit_assignment(node)
        elif isinstance(node, BinaryOp):
            return self.visit_binary_op(node)
        elif isinstance(node, UnaryOp):
            return self.visit_unary_op(node)
        elif isinstance(node, Number):
            return node.value
        elif isinstance(node, String):
            return node.value
        elif isinstance(node, Boolean):
            return node.value
        elif isinstance(node, Variable):
            return self.visit_variable(node)
        elif isinstance(node, List):
            return self.visit_list(node)
        elif isinstance(node, Dict):
            return self.visit_dict(node)
        elif isinstance(node, FunctionCall):
            return self.visit_function_call(node)
        elif isinstance(node, FunctionDef):
            return self.visit_function_def(node)
        elif isinstance(node, ClassDef):
            return self.visit_class_def(node)
        elif isinstance(node, IfStatement):
            return self.visit_if_statement(node)
        elif isinstance(node, ForLoop):
            return self.visit_for_loop(node)
        elif isinstance(node, WhileLoop):
            return self.visit_while_loop(node)
        elif isinstance(node, ReturnStatement):
            return self.visit_return_statement(node)
        elif isinstance(node, BreakStatement):
            raise BreakException()
        elif isinstance(node, ContinueStatement):
            raise ContinueException()
        elif isinstance(node, PrintStatement):
            return self.visit_print_statement(node)
        elif isinstance(node, AttributeAccess):
            return self.visit_attribute_access(node)
        elif isinstance(node, SubscriptAccess):
            return self.visit_subscript_access(node)
        elif isinstance(node, AttributeAssignment):
            return self.visit_attribute_assignment(node)
        elif isinstance(node, SubscriptAssignment):
            return self.visit_subscript_assignment(node)
        elif isinstance(node, MethodCall):
            return self.visit_method_call(node)
        elif isinstance(node, SelfReference):
            return self.visit_self_reference(node)
        elif isinstance(node, SuperCall):
            return self.visit_super_call(node)
        elif isinstance(node, ImportStatement):
            return self.visit_import_statement(node)
        elif isinstance(node, FromImportStatement):
            return self.visit_from_import_statement(node)
        else:
            raise RuntimeError(f"Unknown node type: {type(node)}")

    def visit_program(self, node):
        """Visit a program node"""
        result = None
        for statement in node.statements:
            result = self.interpret(statement)
        return result

    def visit_block(self, node):
        """Visit a block node"""
        result = None
        for statement in node.statements:
            result = self.interpret(statement)
        return result

    def visit_assignment(self, node):
        """Visit an assignment node"""
        value = self.interpret(node.value)

        # Check if this is an attribute assignment (obj.attr = value)
        if '.' in node.name:
            parts = node.name.split('.')
            obj_name = parts[0]
            attr_name = parts[1]

            env = self.local_env if self.local_env is not None else self.global_env
            if obj_name in env:
                obj = env[obj_name]
                if isinstance(obj, BayanObject):
                    obj.set_attribute(attr_name, value)
                    return value
            elif obj_name in self.global_env:
                obj = self.global_env[obj_name]
                if isinstance(obj, BayanObject):
                    obj.set_attribute(attr_name, value)
                    return value

        env = self.local_env if self.local_env is not None else self.global_env
        env[node.name] = value
        return value

    def visit_binary_op(self, node):
        """Visit a binary operation node"""
        left = self.interpret(node.left)
        right = self.interpret(node.right)

        # Helper to try dunder methods on BayanObject
        def _try_dunder(l, r, name, rname=None):
            if isinstance(l, BayanObject) and l.has_method(name):
                return l.call_method(name, [r])
            if rname and isinstance(r, BayanObject) and r.has_method(rname):
                return r.call_method(rname, [l])
            return None

        if node.operator == '+':
            res = _try_dunder(left, right, '__add__', '__radd__')
            return res if res is not None else (left + right)
        elif node.operator == '-':
            res = _try_dunder(left, right, '__sub__', '__rsub__')
            return res if res is not None else (left - right)
        elif node.operator == '*':
            res = _try_dunder(left, right, '__mul__', '__rmul__')
            return res if res is not None else (left * right)
        elif node.operator == '/':
            res = _try_dunder(left, right, '__truediv__', '__rtruediv__')
            return res if res is not None else (left / right)
        elif node.operator == '%':
            res = _try_dunder(left, right, '__mod__', '__rmod__')
            return res if res is not None else (left % right)
        elif node.operator == '==':
            res = _try_dunder(left, right, '__eq__')
            return res if res is not None else (left == right)
        elif node.operator == '!=':
            res = _try_dunder(left, right, '__ne__')
            if res is not None:
                return res
            # Fallback: negate __eq__ if provided
            eq_res = _try_dunder(left, right, '__eq__')
            return (not eq_res) if eq_res is not None else (left != right)
        elif node.operator == '<':
            res = _try_dunder(left, right, '__lt__')
            return res if res is not None else (left < right)
        elif node.operator == '>':
            res = _try_dunder(left, right, '__gt__')
            return res if res is not None else (left > right)
        elif node.operator == '<=':
            res = _try_dunder(left, right, '__le__')
            return res if res is not None else (left <= right)
        elif node.operator == '>=':
            res = _try_dunder(left, right, '__ge__')
            return res if res is not None else (left >= right)
        elif node.operator == 'in':
            # membership: left in right
            if isinstance(right, BayanObject) and right.has_method('__contains__'):
                return right.call_method('__contains__', [left])
            return left in right
        elif node.operator == 'and':
            # Preserve Python-like value return while using Bayan truthiness
            return right if self._truthy(left) else left
        elif node.operator == 'or':
            return left if self._truthy(left) else right
        else:
            raise RuntimeError(f"Unknown operator: {node.operator}")

    def visit_unary_op(self, node):
        """Visit a unary operation node"""
        operand = self.interpret(node.operand)

        if node.operator == '-':
            if isinstance(operand, BayanObject) and operand.has_method('__neg__'):
                return operand.call_method('__neg__', [])
            return -operand
        elif node.operator == 'not':
            return not self._truthy(operand)
        else:
            raise RuntimeError(f"Unknown unary operator: {node.operator}")

    def visit_variable(self, node):
        """Visit a variable node"""
        # Check if this is an attribute access (obj.attr)
        if '.' in node.name:
            parts = node.name.split('.')
            obj_name = parts[0]
            attr_name = parts[1]

            env = self.local_env if self.local_env is not None else self.global_env
            if obj_name in env:
                obj = env[obj_name]
                if isinstance(obj, BayanObject):
                    return obj.get_attribute(attr_name)
            elif obj_name in self.global_env:
                obj = self.global_env[obj_name]
                if isinstance(obj, BayanObject):
                    return obj.get_attribute(attr_name)

        env = self.local_env if self.local_env is not None else self.global_env

        if node.name in env:
            return env[node.name]
        elif node.name in self.global_env:
            return self.global_env[node.name]
        else:
            raise NameError(self._undefined_name_message(node.name))

    def _undefined_name_message(self, name: str) -> str:
        """Build a helpful undefined-name error message with suggestions."""
        # Collect candidate symbols from current scope
        candidates = set()
        if self.local_env:
            candidates.update(self.local_env.keys())
        candidates.update(self.global_env.keys())
        candidates.update(self.functions.keys())
        candidates.update(self.classes.keys())
        # Compute distances and keep best few
        scored = []
        for cand in candidates:
            try:
                d = self._levenshtein(name, str(cand), max_dist=3)
            except Exception:
                d = None
            if d is not None and d <= 3:
                scored.append((d, str(cand)))
        scored.sort(key=lambda x: (x[0], x[1]))
        suggestions = ", ".join(s for _, s in scored[:3])
        if suggestions:
            return f"Undefined variable: {name}. Did you mean: {suggestions}?"
        return f"Undefined variable: {name}"

    def _levenshtein(self, a: str, b: str, max_dist: int = 3) -> int | None:
        """Levenshtein distance with early exit; returns None if > max_dist."""
        if a == b:
            return 0
        # Ensure a is shorter
        if len(a) > len(b):
            a, b = b, a
        # If length diff already exceeds max_dist, skip
        if len(b) - len(a) > max_dist:
            return None
        previous = list(range(len(b) + 1))
        for i, ca in enumerate(a, start=1):
            current = [i]
            row_min = current[0]
            for j, cb in enumerate(b, start=1):
                ins = current[j-1] + 1
                dele = previous[j] + 1
                sub = previous[j-1] + (0 if ca == cb else 1)
                val = min(ins, dele, sub)
                current.append(val)
                if val < row_min:
                    row_min = val
            if row_min > max_dist:
                return None
            previous = current
        return previous[-1] if previous[-1] <= max_dist else None


    def visit_list(self, node):
        """Visit a list node"""
        return [self.interpret(elem) for elem in node.elements]

    def visit_dict(self, node):
        """Visit a dict node"""
        result = {}
        for key_node, value_node in node.pairs:
            key = self.interpret(key_node)
            value = self.interpret(value_node)
            result[key] = value
        return result

    def visit_function_call(self, node):
        """Visit a function call node"""
        # Check if this is a logical predicate call (contains logical variables)
        has_logical_vars = any(isinstance(arg, Variable) and arg.name.startswith('?') for arg in node.arguments)

        if has_logical_vars and hasattr(self, 'logical_engine'):
            # This is a logical query
            from .logical_engine import Predicate, Term

            # Convert arguments to logical terms
            logical_args = []
            for arg in node.arguments:
                if isinstance(arg, Variable):
                    if arg.name.startswith('?'):
                        # Logical variable
                        logical_args.append(Term(arg.name[1:], is_variable=True))
                    else:
                        # Regular variable - evaluate it
                        value = self.interpret(arg)
                        logical_args.append(Term(str(value), is_variable=False))
                else:
                    # Evaluate the argument
                    value = self.interpret(arg)
                    logical_args.append(Term(str(value), is_variable=False))

            # Create a logical predicate and query it
            predicate = Predicate(node.name, logical_args)
            solutions = self.logical_engine.query(predicate)

            # Return True if there are solutions, False otherwise
            return len(solutions) > 0

        # Check for built-in functions
        if node.name == 'len':
            arg = self.interpret(node.arguments[0])
            if isinstance(arg, BayanObject) and arg.has_method('__len__'):
                return arg.call_method('__len__', [])
            return len(arg)
        elif node.name == 'range':
            args = [self.interpret(arg) for arg in node.arguments]
            return list(range(*args))
        elif node.name == 'str':
            arg = self.interpret(node.arguments[0])
            if isinstance(arg, BayanObject) and arg.has_method('__str__'):
                return arg.call_method('__str__', [])
            return str(arg)
        elif node.name == 'repr':
            arg = self.interpret(node.arguments[0])
            if isinstance(arg, BayanObject) and arg.has_method('__repr__'):
                return arg.call_method('__repr__', [])
            return repr(arg)
        elif node.name == 'bool':
            arg = self.interpret(node.arguments[0])
            return bool(self._truthy(arg))
        elif node.name == 'int':
            arg = self.interpret(node.arguments[0])
            return int(arg)
        elif node.name == 'float':
            arg = self.interpret(node.arguments[0])
            return float(arg)
        elif node.name == 'list':
            arg = self.interpret(node.arguments[0])
            return list(arg)
        elif node.name == 'dict':
            return {}

        # Check if this is a class (object instantiation)
        if node.name in self.classes:
            args = [self.interpret(arg) for arg in node.arguments]
            return self.class_system.create_object(node.name, args)

        # User-defined functions
        if node.name in self.functions:
            func_def = self.functions[node.name]
            args = [self.interpret(arg) for arg in node.arguments]

            # Create new local environment
            old_local_env = self.local_env
            self.local_env = {}

            # Bind parameters
            for param, arg in zip(func_def.parameters, args):
                self.local_env[param] = arg

            try:
                result = self.interpret(func_def.body)
            except ReturnValue as ret:
                result = ret.value
            finally:
                self.local_env = old_local_env

            return result

        # Python/global environment callable or BayanObject __call__
        env = self.local_env if self.local_env is not None else self.global_env
        if node.name in env:
            target = env[node.name]
            args = [self.interpret(arg) for arg in node.arguments]
            if isinstance(target, BayanObject) and target.has_method('__call__'):
                return target.call_method('__call__', args)
            if callable(target):
                return target(*args)

        raise NameError(f"Undefined function or class: {node.name}")

    def visit_function_def(self, node):
        """Visit a function definition node"""
        self.functions[node.name] = node
        return None

    def visit_if_statement(self, node):
        """Visit an if statement node"""
        condition = self.interpret(node.condition)

        if self._truthy(condition):
            return self.interpret(node.then_branch)
        elif node.else_branch:
            return self.interpret(node.else_branch)

        return None

    def visit_for_loop(self, node):
        """Visit a for loop node"""
        iterable = self._to_iterable(self.interpret(node.iterable))
        result = None

        env = self.local_env if self.local_env is not None else self.global_env

        for value in iterable:
            env[node.variable] = value
            try:
                result = self.interpret(node.body)
            except BreakException:
                break
            except ContinueException:
                continue

        return result

    def visit_while_loop(self, node):
        """Visit a while loop node"""
        result = None

        while self._truthy(self.interpret(node.condition)):
            try:
                result = self.interpret(node.body)
            except BreakException:
                break
            except ContinueException:
                continue

        return result

    def visit_return_statement(self, node):
        """Visit a return statement node"""
        value = None
        if node.value:
            value = self.interpret(node.value)
        raise ReturnValue(value)

    def visit_print_statement(self, node):
        """Visit a print statement node"""
        value = self.interpret(node.value)
        print(value)
        return None

    def visit_class_def(self, node):
        """Visit a class definition node"""
        self.classes[node.name] = node
        self.class_system.register_class(node)
        return None

    def visit_super_call(self, node):
        """Visit a super(...) call inside a method using MRO"""
        # Ensure we are inside a method with self bound
        if not self.local_env or 'self' not in self.local_env:
            raise RuntimeError("'super' used outside of a method")
        self_obj = self.local_env['self']
        if not isinstance(self_obj, BayanObject):
            raise RuntimeError("'super' requires a BayanObject context")

        # Determine current owner class context for super
        if not self._owner_stack:
            raise RuntimeError("super() requires a current method context")
        current_owner = self._owner_stack[-1]

        # Resolve next method in MRO after current_owner
        start_after = current_owner
        owner, method = self.class_system.resolve_method(self_obj.class_def.name, node.method_name, start_after=start_after)
        if not method:
            raise AttributeError(f"No super method '{node.method_name}' found after {current_owner}")

        args = [self.interpret(arg) for arg in node.arguments]

        # Execute method body with self bound to the current instance; push new owner
        old_env = self.local_env
        self.local_env = {'self': self_obj}
        self._owner_stack.append(owner)
        try:
            for i, param in enumerate(method.parameters):
                if i < len(args):
                    self.local_env[param] = args[i]
            result = self.interpret(method.body)
            return result
        except ReturnValue as ret:
            return ret.value
        finally:
            self._owner_stack.pop()
            self.local_env = old_env

    def visit_attribute_access(self, node):
        """Visit an attribute access node (obj.attr)"""
        obj = self.interpret(node.object_expr)

        if isinstance(obj, BayanObject):
            return obj.get_attribute(node.attribute_name)
        elif isinstance(obj, dict):
            return obj.get(node.attribute_name)
        else:
            # Try Python attribute access
            if hasattr(obj, node.attribute_name):
                return getattr(obj, node.attribute_name)
            raise AttributeError(f"Object has no attribute '{node.attribute_name}'")

    def visit_subscript_access(self, node):
        """Visit a subscript access node (obj[index])"""
        obj = self.interpret(node.object_expr)
        index = self.interpret(node.index_expr)
        if isinstance(obj, BayanObject):
            if obj.has_method('__getitem__'):
                return obj.call_method('__getitem__', [index])
            raise TypeError("Object does not support __getitem__")
        try:
            return obj[index]
        except Exception as e:
            raise TypeError(f"Indexing not supported: {e}")

    def visit_attribute_assignment(self, node):
        """Visit attribute assignment (obj.attr = value)"""
        obj = self.interpret(node.object_expr)
        value = self.interpret(node.value)
        if isinstance(obj, BayanObject):
            obj.set_attribute(node.attribute_name, value)
            return value
        # Fallback to Python setattr
        try:
            setattr(obj, node.attribute_name, value)
            return value
        except Exception as e:
            raise AttributeError(f"Cannot set attribute '{node.attribute_name}': {e}")

    def visit_subscript_assignment(self, node):
        """Visit subscript assignment (obj[index] = value)"""
        obj = self.interpret(node.object_expr)
        index = self.interpret(node.index_expr)
        value = self.interpret(node.value)
        if isinstance(obj, BayanObject):
            if obj.has_method('__setitem__'):
                obj.call_method('__setitem__', [index, value])
                return value
            raise TypeError("Object does not support __setitem__")
        # Python container assignment
        try:
            obj[index] = value
            return value
        except Exception as e:
            raise TypeError(f"Index assignment not supported: {e}")

    def visit_method_call(self, node):
        """Visit a method call node (obj.method())"""
        obj = self.interpret(node.object_expr)
        arguments = [self.interpret(arg) for arg in node.arguments]

        if isinstance(obj, BayanObject):
            return obj.call_method(node.method_name, arguments)
        else:
            # Python object or module function call
            if hasattr(obj, node.method_name):
                func = getattr(obj, node.method_name)
                if callable(func):
                    return func(*arguments)
            raise AttributeError(f"Object has no method '{node.method_name}'")

    def visit_self_reference(self, node):
        """Visit a self reference node"""
        if self.local_env and 'self' in self.local_env:
            return self.local_env['self']
        raise NameError("'self' is not defined")

    def visit_import_statement(self, node):
        """Visit an import statement"""
        module = self.import_system.import_module(node.module_name, node.alias)

        # Add to environment
        name = node.alias if node.alias else node.module_name
        env = self.local_env if self.local_env is not None else self.global_env
        env[name] = module

        return None

    def visit_from_import_statement(self, node):
        """Visit a from...import statement"""
        imported = self.import_system.import_from_module(
            node.module_name,
            node.names,
            node.aliases
        )

        # Add to environment
        env = self.local_env if self.local_env is not None else self.global_env
        for name, value in imported.items():
            env[name] = value

        return None

