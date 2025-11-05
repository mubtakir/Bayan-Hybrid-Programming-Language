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

class YieldValue(Exception):
    """Exception to handle yield expressions in generators"""
    def __init__(self, value):
        self.value = value

class BayanRuntimeError(Exception):
    """Runtime error that carries a Bayan stack trace"""
    pass

class BayanException(Exception):
    """Exception used for Bayan raise/try/except"""
    def __init__(self, value=None):
        self.value = value



class TraditionalInterpreter:
    """Interpreter for traditional programming constructs"""

    class BayanCoroutine:
        """Simple coroutine object for async function calls."""
        def __init__(self, interpreter, func_def, args, named_args):
            self.interpreter = interpreter
            self.func_def = func_def
            self.args = args
            self.named_args = named_args or {}

        def run(self):
            """Execute the coroutine synchronously"""
            interp = self.interpreter
            # Save and switch local environment
            old_local_env = interp.local_env
            interp.local_env = {}
            try:
                # Resolve parameters (support Parameter objects or raw names)
                parameters = getattr(self.func_def, 'parameters', getattr(self.func_def, 'params', []))
                param_names = []
                for p in parameters:
                    if isinstance(p, Parameter):
                        param_names.append(p.name)
                    else:
                        param_names.append(p)

                # Bind positional arguments
                for i, arg in enumerate(self.args):
                    if i < len(param_names):
                        interp.local_env[param_names[i]] = arg

                # Bind named arguments
                for name, value in self.named_args.items():
                    if name in param_names:
                        interp.local_env[name] = value

                # Bind defaults
                for p in parameters:
                    if isinstance(p, Parameter):
                        if p.name not in interp.local_env and p.has_default():
                            interp.local_env[p.name] = interp.interpret(p.default_value)
                        elif p.name not in interp.local_env and not p.has_default():
                            raise RuntimeError(f"Missing required parameter: {p.name}")

                # Execute body
                try:
                    result = interp.interpret(self.func_def.body)
                except ReturnValue as ret:
                    result = ret.value
                return result
            finally:
                interp.local_env = old_local_env

        def __await__(self):
            """Make this a proper awaitable"""
            result = self.run()
            if False:
                yield None
            return result

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
        # Track async functions
        self._async_functions = set()

        # Error reporting configuration
        self._err_color = False
        self._err_context_lines = 1
        self._err_tabstop = 4

        # Register built-in types in global environment
        self.global_env['str'] = str
        self.global_env['int'] = int
        self.global_env['float'] = float
        self.global_env['bool'] = bool
        self.global_env['list'] = list
        self.global_env['dict'] = dict
        self.global_env['tuple'] = tuple
        self.global_env['set'] = set
        self.global_env['type'] = type
        self.global_env['object'] = object

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
            if isinstance(e, (ReturnValue, BreakException, ContinueException, YieldValue, BayanException, BayanRuntimeError)):
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
        elif isinstance(node, ListComprehension):
            return self.visit_list_comprehension(node)
        elif isinstance(node, Dict):
            return self.visit_dict(node)
        elif isinstance(node, Tuple):
            return self.visit_tuple(node)
        elif isinstance(node, Set):
            return self.visit_set(node)
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
        elif isinstance(node, RaiseStatement):
            return self.visit_raise_statement(node)
        elif isinstance(node, TryExceptFinally):
            return self.visit_try_except_finally(node)
        elif isinstance(node, AsyncFunctionDef):
            return self.visit_async_function_def(node)
        elif isinstance(node, AwaitExpr):
            return self.visit_await_expr(node)
        elif isinstance(node, YieldExpr):
            return self.visit_yield_expr(node)
        elif isinstance(node, WithStatement):
            return self.visit_with_statement(node)
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

    def _contains_yield(self, node):
        """Check if node contains yield expression"""
        from .ast_nodes import YieldExpr, Block, ForLoop, WhileLoop, IfStatement

        if isinstance(node, YieldExpr):
            return True
        if isinstance(node, Block):
            return any(self._contains_yield(stmt) for stmt in node.statements)
        if isinstance(node, ForLoop):
            return self._contains_yield(node.body)
        if isinstance(node, WhileLoop):
            return self._contains_yield(node.body)
        if isinstance(node, IfStatement):
            has_yield = self._contains_yield(node.then_block)
            if node.else_block:
                has_yield = has_yield or self._contains_yield(node.else_block)
            return has_yield
        if isinstance(node, list):
            return any(self._contains_yield(n) for n in node if hasattr(n, '__class__'))
        return False


    def visit_list(self, node):
        """Visit a list node"""
        return [self.interpret(elem) for elem in node.elements]

    def visit_tuple(self, node):
        """Visit a tuple node"""
        return tuple(self.interpret(elem) for elem in node.elements)

    def visit_set(self, node):
        """Visit a set node"""
        return set(self.interpret(elem) for elem in node.elements)

    def visit_list_pattern(self, node):
        """Visit a list pattern node [H|T]"""
        # Convert ListPattern to internal representation for logical engine
        head_elements = [self.interpret(elem) for elem in node.head_elements]
        tail = self.interpret(node.tail)

        # Return a special dict representation
        return {
            'list_pattern': True,
            'head': head_elements,
            'tail': tail
        }

    def visit_list_comprehension(self, node):
        """Evaluate a list comprehension."""
        iterable = self._to_iterable(self.interpret(node.iterable))
        result = []
        env = self.local_env if self.local_env is not None else self.global_env
        for value in iterable:
            env[node.var_name] = value
            if node.condition is not None:
                cond = self.interpret(node.condition)
                if not cond:
                    continue
            result.append(self.interpret(node.expr))
        return result

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
        elif node.name == 'isinstance':
            args = [self.interpret(arg) for arg in node.arguments]
            return isinstance(*args)
        elif node.name == 'type':
            arg = self.interpret(node.arguments[0])
            return type(arg)
        elif node.name == 'callable':
            arg = self.interpret(node.arguments[0])
            return callable(arg)
        elif node.name == 'hasattr':
            args = [self.interpret(arg) for arg in node.arguments]
            return hasattr(*args)
        elif node.name == 'getattr':
            args = [self.interpret(arg) for arg in node.arguments]
            return getattr(*args)
        elif node.name == 'setattr':
            args = [self.interpret(arg) for arg in node.arguments]
            setattr(*args)
            return None
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
            # Check if it's a generator
            if hasattr(arg, '__iter__') and hasattr(arg, '__next__'):
                result = []
                try:
                    while True:
                        result.append(next(arg))
                except StopIteration:
                    pass
                return result
            return list(arg)
        elif node.name == 'dict':
            return {}
        elif node.name == 'sum':
            args = [self.interpret(arg) for arg in node.arguments]
            if len(args) == 1:
                return sum(args[0])
            elif len(args) == 2:
                return sum(args[0], args[1])  # sum(iterable, start)
            else:
                raise RuntimeError("sum() takes 1 or 2 arguments")
        elif node.name == 'min':
            args = [self.interpret(arg) for arg in node.arguments]
            if len(args) == 1 and hasattr(args[0], '__iter__'):
                return min(args[0])
            else:
                return min(*args)
        elif node.name == 'max':
            args = [self.interpret(arg) for arg in node.arguments]
            if len(args) == 1 and hasattr(args[0], '__iter__'):
                return max(args[0])
            else:
                return max(*args)
        elif node.name == 'sorted':
            args = [self.interpret(arg) for arg in node.arguments]
            if len(args) == 1:
                return sorted(args[0])
            elif len(args) == 2:
                # sorted(iterable, reverse=True/False)
                return sorted(args[0], reverse=args[1])
            else:
                raise RuntimeError("sorted() takes 1 or 2 arguments")
        elif node.name == 'enumerate':
            args = [self.interpret(arg) for arg in node.arguments]
            if len(args) == 1:
                return list(enumerate(args[0]))
            elif len(args) == 2:
                return list(enumerate(args[0], args[1]))  # enumerate(iterable, start)
            else:
                raise RuntimeError("enumerate() takes 1 or 2 arguments")
        elif node.name == 'zip':
            args = [self.interpret(arg) for arg in node.arguments]
            return list(zip(*args))
        elif node.name == 'map':
            # Special handling: first argument might be a function name (Variable node)
            if len(node.arguments) < 2:
                raise RuntimeError("map() requires at least 2 arguments")

            # Check if first argument is a Variable (function name)
            first_arg = node.arguments[0]
            if isinstance(first_arg, Variable) and first_arg.name in self.functions:
                func_name = first_arg.name
                func_def = self.functions[func_name]
                iterables = [self.interpret(arg) for arg in node.arguments[1:]]

                def wrapper(*items):
                    old_local = self.local_env
                    self.local_env = {}
                    try:
                        for i, param in enumerate(func_def.parameters):
                            param_name = param.name if isinstance(param, Parameter) else param
                            if i < len(items):
                                self.local_env[param_name] = items[i]
                        try:
                            result = self.interpret(func_def.body)
                        except ReturnValue as ret:
                            result = ret.value
                        return result
                    finally:
                        self.local_env = old_local
                return list(map(wrapper, *iterables))
            else:
                # Evaluate all arguments normally
                args = [self.interpret(arg) for arg in node.arguments]
                func = args[0]
                iterables = args[1:]
                return list(map(func, *iterables))
        elif node.name == 'filter':
            # Special handling: first argument might be a function name (Variable node)
            if len(node.arguments) != 2:
                raise RuntimeError("filter() requires exactly 2 arguments")

            # Check if first argument is a Variable (function name)
            first_arg = node.arguments[0]
            if isinstance(first_arg, Variable) and first_arg.name in self.functions:
                func_name = first_arg.name
                func_def = self.functions[func_name]
                iterable = self.interpret(node.arguments[1])

                def wrapper(item):
                    old_local = self.local_env
                    self.local_env = {}
                    try:
                        param_name = func_def.parameters[0].name if isinstance(func_def.parameters[0], Parameter) else func_def.parameters[0]
                        self.local_env[param_name] = item
                        try:
                            result = self.interpret(func_def.body)
                        except ReturnValue as ret:
                            result = ret.value
                        return self._truthy(result)
                    finally:
                        self.local_env = old_local
                return list(filter(wrapper, iterable))
            else:
                # Evaluate all arguments normally
                args = [self.interpret(arg) for arg in node.arguments]
                func = args[0]
                iterable = args[1]
                return list(filter(func, iterable))
        elif node.name == 'all':
            arg = self.interpret(node.arguments[0])
            return all(self._truthy(x) for x in arg)
        elif node.name == 'any':
            arg = self.interpret(node.arguments[0])
            return any(self._truthy(x) for x in arg)
        elif node.name == 'abs':
            arg = self.interpret(node.arguments[0])
            return abs(arg)
        elif node.name == 'round':
            args = [self.interpret(arg) for arg in node.arguments]
            if len(args) == 1:
                return round(args[0])
            elif len(args) == 2:
                return round(args[0], args[1])
            else:
                raise RuntimeError("round() takes 1 or 2 arguments")
        elif node.name == 'pow':
            args = [self.interpret(arg) for arg in node.arguments]
            if len(args) == 2:
                return pow(args[0], args[1])
            elif len(args) == 3:
                return pow(args[0], args[1], args[2])
            else:
                raise RuntimeError("pow() takes 2 or 3 arguments")
        elif node.name == 'reversed':
            arg = self.interpret(node.arguments[0])
            return list(reversed(arg))

        # Logical programming: assert/retract
        elif node.name == 'assertz' or node.name == 'asserta' or node.name == 'retract' or node.name == 'retractall':
            if self.logical_engine is None:
                raise RuntimeError(f"{node.name}() requires a logical engine")

            # These functions work with predicates/facts
            # For now, we'll support passing predicate objects
            arg = self.interpret(node.arguments[0])

            if node.name == 'assertz':
                self.logical_engine.assertz(arg)
                return True
            elif node.name == 'asserta':
                self.logical_engine.asserta(arg)
                return True
            elif node.name == 'retract':
                return self.logical_engine.retract(arg)
            elif node.name == 'retractall':
                return self.logical_engine.retractall(arg)

        # Check if this is a class (object instantiation)
        if node.name in self.classes:
            args = [self.interpret(arg) for arg in node.arguments]
            # Handle named arguments
            named_args = {}
            if hasattr(node, 'named_arguments') and node.named_arguments:
                for name, value in node.named_arguments.items():
                    named_args[name] = self.interpret(value)
            return self.class_system.create_object(node.name, args, named_args)

        # Check if function is decorated (stored in environment)
        env = self.local_env if self.local_env is not None else self.global_env
        if node.name in env:
            target = env[node.name]
            # Check if it's a decorated function (callable)
            if callable(target) and not isinstance(target, type):
                args = [self.interpret(arg) for arg in node.arguments]
                if isinstance(target, BayanObject) and target.has_method('__call__'):
                    return target.call_method('__call__', args)
                return target(*args)

        # User-defined functions
        if node.name in self.functions:
            func_def = self.functions[node.name]
            args = [self.interpret(arg) for arg in node.arguments]

            # Check if function is async - return a coroutine
            if node.name in self._async_functions:
                named_args = {}
                if hasattr(node, 'named_arguments'):
                    for name, value in node.named_arguments.items():
                        named_args[name] = self.interpret(value)
                return self.BayanCoroutine(self, func_def, args, named_args)

            # Check if function contains yield (is a generator)
            if self._contains_yield(func_def.body):
                # Return a generator
                return self._create_generator(func_def, args, node.named_arguments if hasattr(node, 'named_arguments') else {})

            # Evaluate named arguments
            named_args = {}
            if hasattr(node, 'named_arguments'):
                for name, value in node.named_arguments.items():
                    named_args[name] = self.interpret(value)

            # Create new local environment
            old_local_env = self.local_env
            self.local_env = {}

            # Bind parameters with support for defaults, named arguments, *args, and **kwargs
            param_names = []
            varargs_param = None
            kwargs_param = None

            for param in func_def.parameters:
                if isinstance(param, Parameter):
                    if param.is_kwargs:
                        kwargs_param = param.name
                    elif param.is_varargs:
                        varargs_param = param.name
                    else:
                        param_names.append(param.name)
                else:
                    # Legacy format: parameter is just a string
                    param_names.append(param)

            # Bind positional arguments
            positional_count = 0
            for i, arg in enumerate(args):
                if i < len(param_names):
                    self.local_env[param_names[i]] = arg
                    positional_count += 1
                elif varargs_param:
                    # Extra positional arguments go to *args
                    if varargs_param not in self.local_env:
                        self.local_env[varargs_param] = []
                    self.local_env[varargs_param].append(arg)
                else:
                    raise RuntimeError(f"Too many positional arguments for function {node.name}")

            # Initialize *args if it exists and wasn't populated
            if varargs_param and varargs_param not in self.local_env:
                self.local_env[varargs_param] = []

            # Bind named arguments
            for name, value in named_args.items():
                if name in param_names:
                    self.local_env[name] = value
                elif kwargs_param:
                    # Extra named arguments go to **kwargs
                    if kwargs_param not in self.local_env:
                        self.local_env[kwargs_param] = {}
                    self.local_env[kwargs_param][name] = value
                else:
                    raise RuntimeError(f"Unexpected keyword argument: {name}")

            # Initialize **kwargs if it exists and wasn't populated
            if kwargs_param and kwargs_param not in self.local_env:
                self.local_env[kwargs_param] = {}

            # Bind default values for missing parameters
            for param in func_def.parameters:
                if isinstance(param, Parameter):
                    if not param.is_varargs and not param.is_kwargs:
                        if param.name not in self.local_env and param.has_default():
                            self.local_env[param.name] = self.interpret(param.default_value)
                        elif param.name not in self.local_env:
                            raise RuntimeError(f"Missing required parameter: {param.name}")

            try:
                result = self.interpret(func_def.body)
            except ReturnValue as ret:
                result = ret.value
            finally:
                self.local_env = old_local_env

            return result

        # Python/global environment callable or BayanObject __call__
        if node.name in env:
            target = env[node.name]
            args = [self.interpret(arg) for arg in node.arguments]
            if isinstance(target, BayanObject) and target.has_method('__call__'):
                return target.call_method('__call__', args)
            if callable(target):
                return target(*args)

        raise NameError(f"Undefined function or class: {node.name}")

    def visit_function_def(self, node):
        """Visit a function definition node with decorator support"""
        # Store the function
        self.functions[node.name] = node

        # Also store in local environment if we're inside a function
        if self.local_env is not None:
            # Create a callable for nested functions WITH CLOSURE SUPPORT
            # Capture the current local_env as closure
            closure_env = dict(self.local_env)  # Copy current local environment

            def make_nested_callable(fn_node, interp, closure):
                def nested_callable(*args):
                    return interp._execute_function(fn_node, list(args), closure)
                return nested_callable

            self.local_env[node.name] = make_nested_callable(node, self, closure_env)

        # Apply decorators if present (in reverse order, bottom to top)
        if node.decorators:
            # For Bayan decorators, we need to call the decorator function
            # with the original function as an argument

            env = self.local_env if self.local_env is not None else self.global_env

            # Start with the original function
            func_name = node.name
            func_node = self.functions[func_name]
            current_closure = dict(self.local_env) if self.local_env is not None else None

            def make_func_callable(fn_node, interp, closure):
                def func_callable(*args):
                    return interp._execute_function(fn_node, list(args), closure)
                return func_callable

            # Start with the base function
            current_func = make_func_callable(func_node, self, current_closure)

            # Apply decorators in reverse order (bottom decorator first)
            for decorator in reversed(node.decorators):
                # Check if decorator has arguments
                if hasattr(decorator, 'args') and decorator.args:
                    # Decorator with arguments: @decorator(arg1, arg2)
                    # First call the decorator with its arguments to get the actual decorator
                    decorator_args = [self.interpret(arg) for arg in decorator.args]

                    if decorator.name in self.functions:
                        # Call the decorator factory function
                        from .ast_nodes import FunctionCall, Number, String

                        # Create argument nodes for the decorator factory
                        arg_nodes = []
                        for arg in decorator_args:
                            if isinstance(arg, (int, float)):
                                arg_nodes.append(Number(arg))
                            elif isinstance(arg, str):
                                arg_nodes.append(String(arg))
                            else:
                                # For other types, we'll need to handle them differently
                                arg_nodes.append(Number(arg))  # Fallback
                        factory_call = FunctionCall(decorator.name, arg_nodes, {})

                        # This should return a decorator function
                        actual_decorator = self.interpret(factory_call)

                        # Call the decorator with the current function
                        if callable(actual_decorator):
                            current_func = actual_decorator(current_func)
                else:
                    # Simple decorator: @decorator
                    if decorator.name in self.functions:
                        # Call the decorator with the current function
                        decorator_result = self._execute_function(self.functions[decorator.name], [current_func])
                        current_func = decorator_result

            # Store the final decorated function
            env[node.name] = current_func

        return None

    def _execute_function(self, func_def, args, closure=None):
        """Helper method to execute a Bayan function with given arguments

        Args:
            func_def: The function definition AST node
            args: List of arguments to pass to the function
            closure: Optional dict containing closure variables from parent scope
        """
        # Create new local environment
        old_local_env = self.local_env

        # Start with closure if provided, otherwise empty dict
        if closure is not None:
            self.local_env = dict(closure)  # Copy closure to avoid mutation
        else:
            self.local_env = {}

        # Bind parameters
        param_names = []
        for param in func_def.parameters:
            if isinstance(param, Parameter):
                param_names.append(param.name)
            else:
                param_names.append(param)

        for i, arg in enumerate(args):
            if i < len(param_names):
                self.local_env[param_names[i]] = arg

                # If the argument is a callable (e.g., a decorated function),
                # also make it available for function calls
                if callable(arg) and not isinstance(arg, (int, float, str, bool, list, dict, type)):
                    # This allows calling the function from within Bayan code
                    pass  # Already stored in local_env

        try:
            result = self.interpret(func_def.body)
        except ReturnValue as ret:
            result = ret.value
        finally:
            self.local_env = old_local_env

        return result

    def visit_async_function_def(self, node):
        """Visit an async function definition node"""
        # Store async function with marker
        self.functions[node.name] = node
        # Mark as async in a separate registry
        self._async_functions.add(node.name)
        return None

    def visit_await_expr(self, node):
        """Visit an await expression node"""
        # Evaluate the expression being awaited
        result = self.interpret(node.expression)

        # If result is a BayanCoroutine, execute it synchronously
        if isinstance(result, self.BayanCoroutine):
            return result.run()

        # If result has __await__, call it
        if hasattr(result, '__await__'):
            return result.__await__()

        # Otherwise return the result as-is
        return result

    def visit_yield_expr(self, node):
        """Visit a yield expression node"""
        # Evaluate the value to yield
        value = None
        if node.value:
            value = self.interpret(node.value)

        # Raise YieldValue exception to signal yielding
        raise YieldValue(value)

    def visit_with_statement(self, node):
        """Visit a with statement node (context manager)"""
        # Evaluate the context expression
        context_obj = self.interpret(node.context_expr)

        # Call __enter__ method
        if isinstance(context_obj, BayanObject) and context_obj.has_method('__enter__'):
            enter_result = context_obj.call_method('__enter__', [])
        elif hasattr(context_obj, '__enter__'):
            enter_result = context_obj.__enter__()
        else:
            raise TypeError(f"Object does not support context manager protocol")

        # Bind the result to the target variable if specified
        env = self.local_env if self.local_env is not None else self.global_env
        if node.target_var:
            env[node.target_var] = enter_result

        # Execute the body
        result = None
        exception_occurred = None
        try:
            result = self.interpret(node.body)
        except Exception as e:
            exception_occurred = e

        # Call __exit__ method
        try:
            if isinstance(context_obj, BayanObject) and context_obj.has_method('__exit__'):
                context_obj.call_method('__exit__', [None, None, None])
            elif hasattr(context_obj, '__exit__'):
                context_obj.__exit__(None, None, None)
        except Exception:
            pass

        # Re-raise the exception if one occurred
        if exception_occurred:
            raise exception_occurred

        return result

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

    def visit_raise_statement(self, node):
        """Visit a raise statement node"""
        value = self.interpret(node.value) if node.value is not None else None
        raise BayanException(value)

    def visit_try_except_finally(self, node):
        """Visit a try/except/finally node"""
        result = None
        try:
            result = self.interpret(node.try_block)
        except (BayanException, BayanRuntimeError, Exception) as e:
            # Don't catch control flow exceptions
            if isinstance(e, (ReturnValue, BreakException, ContinueException, YieldValue)):
                raise

            handled = False
            env = self.local_env if self.local_env is not None else self.global_env

            # Extract the actual exception value
            if isinstance(e, BayanException):
                exc_value = e.value
            elif isinstance(e, BayanRuntimeError):
                exc_value = str(e)
            else:
                exc_value = str(e)

            for handler in node.handlers:
                match = False
                if handler.type_name is None:
                    # Bare except: catches everything
                    match = True
                else:
                    # Determine exception class name if BayanObject
                    if isinstance(e, BayanException) and isinstance(e.value, BayanObject):
                        exc_class = e.value.class_def.name
                        if exc_class == handler.type_name or self.class_system.is_subclass(exc_class, handler.type_name):
                            match = True
                    else:
                        # Python exceptions or non-object Bayan exceptions match generic handlers
                        if handler.type_name in ('Exception', 'BaseException'):
                            match = True
                        # Also match specific Python exception types
                        elif handler.type_name == e.__class__.__name__:
                            match = True
                if match:
                    handled = True
                    if handler.alias:
                        env[handler.alias] = exc_value
                    result = self.interpret(handler.body)
                    break
            if not handled:
                # Propagate if not matched
                raise
        finally:
            if node.finally_block:
                self.interpret(node.finally_block)
        return result

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
            # Bind parameters with support for Parameter objects and defaults
            from .ast_nodes import Parameter

            param_names = []
            for param in method.parameters:
                if isinstance(param, Parameter):
                    if param.name != 'self':
                        param_names.append(param.name)
                else:
                    # Legacy format: parameter is just a string
                    if param != 'self':
                        param_names.append(param)

            # Bind positional arguments
            for i, arg in enumerate(args):
                if i < len(param_names):
                    self.local_env[param_names[i]] = arg

            # Bind default values for missing parameters
            for param in method.parameters:
                if isinstance(param, Parameter):
                    if param.name != 'self' and param.name not in self.local_env and param.has_default():
                        self.local_env[param.name] = self.interpret(param.default_value)

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
        """Visit a subscript access node (obj[index] or obj[start:end:step])"""
        from .ast_nodes import Slice

        obj = self.interpret(node.object_expr)
        index_expr = node.index_expr

        # Check if this is a slice operation
        if isinstance(index_expr, Slice):
            start = self.interpret(index_expr.start) if index_expr.start is not None else None
            end = self.interpret(index_expr.end) if index_expr.end is not None else None
            step = self.interpret(index_expr.step) if index_expr.step is not None else None

            # Create Python slice object
            slice_obj = slice(start, end, step)

            if isinstance(obj, BayanObject):
                if obj.has_method('__getitem__'):
                    return obj.call_method('__getitem__', [slice_obj])
                raise TypeError("Object does not support __getitem__")
            try:
                return obj[slice_obj]
            except Exception as e:
                raise TypeError(f"Slicing not supported: {e}")
        else:
            # Regular indexing
            index = self.interpret(index_expr)
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
        """Visit a method call node (obj.method()) with support for named arguments"""
        obj = self.interpret(node.object_expr)
        arguments = [self.interpret(arg) for arg in node.arguments]

        # Evaluate named arguments
        named_args = {}
        if hasattr(node, 'named_arguments'):
            for name, value in node.named_arguments.items():
                named_args[name] = self.interpret(value)

        if isinstance(obj, BayanObject):
            return obj.call_method(node.method_name, arguments, named_args)
        else:
            # Python object or module function call
            if hasattr(obj, node.method_name):
                func = getattr(obj, node.method_name)
                if callable(func):
                    return func(*arguments, **named_args)
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

    def _contains_yield(self, node):
        """Check if a node or its children contain a yield expression"""
        if isinstance(node, YieldExpr):
            return True

        # Check all attributes that might contain child nodes
        if isinstance(node, Block):
            for statement in node.statements:
                if self._contains_yield(statement):
                    return True
        elif isinstance(node, IfStatement):
            if self._contains_yield(node.then_branch):
                return True
            if node.else_branch and self._contains_yield(node.else_branch):
                return True
        elif isinstance(node, WhileLoop):
            if self._contains_yield(node.body):
                return True
        elif isinstance(node, ForLoop):
            if self._contains_yield(node.body):
                return True
        elif isinstance(node, TryExceptFinally):
            if self._contains_yield(node.try_block):
                return True
            for handler in node.handlers:
                if self._contains_yield(handler.body):
                    return True
            if node.finally_block and self._contains_yield(node.finally_block):
                return True

        return False

    def _interpret_in_env(self, node, env):
        """Interpret a node with a specific local environment, restoring afterward."""
        old_env = self.local_env
        self.local_env = env
        try:
            return self.interpret(node)
        finally:
            self.local_env = old_env

    def _gen_run_block(self, block, env):
        """Execute a block as a Python generator, yielding values on YieldExpr."""
        for stmt in block.statements:
            # Yield statement
            if isinstance(stmt, YieldExpr):
                value = self._interpret_in_env(stmt.value, env) if stmt.value is not None else None
                yield value
                continue

            # Return ends the generator
            if isinstance(stmt, ReturnStatement):
                return

            # Simple assignment
            if isinstance(stmt, Assignment):
                value = self._interpret_in_env(stmt.value, env)
                env[stmt.name] = value
                continue

            # If statement (bodies may yield)
            if isinstance(stmt, IfStatement):
                cond = self._interpret_in_env(stmt.condition, env)
                if self._truthy(cond):
                    if isinstance(stmt.then_branch, Block):
                        yield from self._gen_run_block(stmt.then_branch, env)
                    else:
                        self._interpret_in_env(stmt.then_branch, env)
                elif stmt.else_branch:
                    if isinstance(stmt.else_branch, Block):
                        yield from self._gen_run_block(stmt.else_branch, env)
                    else:
                        self._interpret_in_env(stmt.else_branch, env)
                continue

            # For loop (body may yield)
            if isinstance(stmt, ForLoop):
                iterable = self._to_iterable(self._interpret_in_env(stmt.iterable, env))
                for value in iterable:
                    env[stmt.variable] = value
                    try:
                        yield from self._gen_run_block(stmt.body, env)
                    except BreakException:
                        break
                    except ContinueException:
                        continue
                continue

            # While loop (body may yield)
            if isinstance(stmt, WhileLoop):
                while self._truthy(self._interpret_in_env(stmt.condition, env)):
                    try:
                        yield from self._gen_run_block(stmt.body, env)
                    except BreakException:
                        break
                    except ContinueException:
                        continue
                continue

            # Try/except/finally (blocks may yield)
            if isinstance(stmt, TryExceptFinally):
                try:
                    # Execute try block as generator
                    yield from self._gen_run_block(stmt.try_block, env)
                except (BayanException, BayanRuntimeError, Exception) as e:
                    # Don't catch control flow exceptions
                    if isinstance(e, (ReturnValue, BreakException, ContinueException, YieldValue)):
                        raise

                    handled = False

                    # Extract the actual exception value
                    if isinstance(e, BayanException):
                        exc_value = e.value
                    elif isinstance(e, BayanRuntimeError):
                        exc_value = str(e)
                    else:
                        exc_value = str(e)

                    for handler in stmt.handlers:
                        match = False
                        if handler.type_name is None:
                            # Bare except: catches everything
                            match = True
                        else:
                            # Determine exception class name if BayanObject
                            if isinstance(e, BayanException) and isinstance(e.value, BayanObject):
                                exc_class = e.value.class_def.name
                                if exc_class == handler.type_name or self.class_system.is_subclass(exc_class, handler.type_name):
                                    match = True
                            else:
                                # Python exceptions or non-object Bayan exceptions match generic handlers
                                if handler.type_name in ('Exception', 'BaseException'):
                                    match = True
                                # Also match specific Python exception types
                                elif handler.type_name == e.__class__.__name__:
                                    match = True
                        if match:
                            handled = True
                            if handler.alias:
                                env[handler.alias] = exc_value
                            # Execute handler body as generator
                            yield from self._gen_run_block(handler.body, env)
                            break
                    if not handled:
                        # Propagate if not matched
                        raise
                finally:
                    if stmt.finally_block:
                        # Execute finally block as generator
                        yield from self._gen_run_block(stmt.finally_block, env)
                continue

            # With statement (body may yield)
            if isinstance(stmt, WithStatement):
                # Evaluate context manager
                context_manager = self._interpret_in_env(stmt.expression, env)

                # Call __enter__
                if isinstance(context_manager, BayanObject) and context_manager.has_method('__enter__'):
                    enter_result = context_manager.call_method('__enter__', [])
                elif hasattr(context_manager, '__enter__'):
                    enter_result = context_manager.__enter__()
                else:
                    raise RuntimeError(f"Context manager does not have __enter__ method")

                # Bind to alias if provided
                if stmt.alias:
                    env[stmt.alias] = enter_result

                # Execute body with proper cleanup
                try:
                    yield from self._gen_run_block(stmt.body, env)
                finally:
                    # Call __exit__
                    if isinstance(context_manager, BayanObject) and context_manager.has_method('__exit__'):
                        context_manager.call_method('__exit__', [None, None, None])
                    elif hasattr(context_manager, '__exit__'):
                        context_manager.__exit__(None, None, None)
                continue

            # Fallback: execute statement synchronously
            self._interpret_in_env(stmt, env)

    def _create_generator(self, func_def, args, named_args):
        """Return a native Python generator for a function containing yield."""
        # Prepare a fresh local environment for this generator invocation
        gen_env = {}

        # Parameter names (support Parameter objects or raw names)
        parameters = getattr(func_def, 'parameters', getattr(func_def, 'params', []))
        param_names = []
        for p in parameters:
            if isinstance(p, Parameter):
                param_names.append(p.name)
            else:
                param_names.append(p)

        # Bind positional arguments
        for i, arg in enumerate(args):
            if i < len(param_names):
                gen_env[param_names[i]] = arg

        # Bind named arguments (values are AST nodes; evaluate in caller env)
        if isinstance(named_args, dict):
            for name, value_node in named_args.items():
                if name in param_names:
                    gen_env[name] = self.interpret(value_node)

        # Apply default values for missing parameters
        for p in parameters:
            if isinstance(p, Parameter) and p.default_value is not None and p.name not in gen_env:
                gen_env[p.name] = self.interpret(p.default_value)

        def generator():
            # Drive the function body as a generator
            yield from self._gen_run_block(func_def.body, gen_env)

        return generator()
