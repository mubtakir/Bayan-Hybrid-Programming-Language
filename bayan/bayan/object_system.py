"""
Object System for Bayan Language
نظام الكائنات للغة بيان
"""

class BayanObject:
    """Represents a Bayan object instance"""

    def __init__(self, class_def, interpreter, arguments=None):
        """Initialize a Bayan object"""
        self.class_def = class_def
        self.interpreter = interpreter
        self.attributes = {}
        # Local methods for this class only
        self.methods = {}

        # Extract methods from class definition
        self._extract_methods()

        # Call constructor if exists
        if arguments is not None:
            self._call_constructor(arguments)

    def _extract_methods(self):
        """Extract methods from class definition"""
        if self.class_def.body:
            for stmt in self.class_def.body.statements:
                from .ast_nodes import FunctionDef
                if isinstance(stmt, FunctionDef):
                    self.methods[stmt.name] = stmt

    def _call_constructor(self, arguments):
        """Call the constructor (__init__)"""
        # Resolve via MRO (so parent's __init__ can be called via super)
        owner, constructor = self.interpreter.class_system.resolve_method(self.class_def.name, '__init__')
        if constructor:
            # Create new environment with self, and push owner on stack
            old_env = self.interpreter.local_env
            self.interpreter.local_env = {'self': self}
            if not hasattr(self.interpreter, '_owner_stack'):
                self.interpreter._owner_stack = []
            self.interpreter._owner_stack.append(owner)
            try:
                # Bind arguments to parameters
                for i, param in enumerate(constructor.parameters):
                    if i < len(arguments):
                        self.interpreter.local_env[param] = arguments[i]
                # Execute constructor body
                self.interpreter.interpret(constructor.body)
            finally:
                self.interpreter._owner_stack.pop()
                self.interpreter.local_env = old_env

    def get_attribute(self, name):
        """Get an attribute value"""
        if name in self.attributes:
            return self.attributes[name]
        return None

    def set_attribute(self, name, value):
        """Set an attribute value"""
        self.attributes[name] = value

    def call_method(self, method_name, arguments):
        """Call a method on this object using class MRO"""
        # Find method via class system MRO
        owner, method = self.interpreter.class_system.resolve_method(self.class_def.name, method_name)
        if not method:
            raise AttributeError(f"Method '{method_name}' not found")

        # Create new environment with self and push owner
        old_env = self.interpreter.local_env
        self.interpreter.local_env = {'self': self}
        if not hasattr(self.interpreter, '_owner_stack'):
            self.interpreter._owner_stack = []
        self.interpreter._owner_stack.append(owner)

        try:
            # Bind arguments to parameters
            for i, param in enumerate(method.parameters):
                if i < len(arguments):
                    self.interpreter.local_env[param] = arguments[i]

            # Execute method body
            result = self.interpreter.interpret(method.body)
            return result
        except Exception as e:
            # Handle ReturnValue exception
            if e.__class__.__name__ == 'ReturnValue':
                return e.value
            raise
        finally:
            self.interpreter._owner_stack.pop()
            self.interpreter.local_env = old_env

    def has_method(self, method_name):
        """Check if object has a method via MRO"""
        owner, method = self.interpreter.class_system.resolve_method(self.class_def.name, method_name)
        return method is not None

    def __repr__(self):
        return f"<{self.class_def.name} object>"


class ClassSystem:
    """Manages class definitions and object creation"""

    def __init__(self, interpreter):
        """Initialize class system"""
        self.interpreter = interpreter
        self.classes = {}
        # child -> list of parent names (order matters)
        self.inheritance_map = {}
        # class_name -> {method_name: FunctionDef}
        self.methods_map = {}

    def _extract_methods_from_class(self, class_def):
        methods = {}
        if class_def.body:
            from .ast_nodes import FunctionDef
            for stmt in class_def.body.statements:
                if isinstance(stmt, FunctionDef):
                    methods[stmt.name] = stmt
        return methods

    def register_class(self, class_def):
        """Register a class definition"""
        self.classes[class_def.name] = class_def
        # Methods cache
        self.methods_map[class_def.name] = self._extract_methods_from_class(class_def)

        # Register inheritance (support multiple bases)
        bases = []
        if hasattr(class_def, 'base_classes') and class_def.base_classes:
            bases = list(class_def.base_classes)
        elif class_def.base_class:
            bases = [class_def.base_class]
        self.inheritance_map[class_def.name] = bases

    def create_object(self, class_name, arguments=None):
        """Create an object instance"""
        if class_name not in self.classes:
            raise NameError(f"Class '{class_name}' not defined")

        class_def = self.classes[class_name]
        # Create object without calling constructor yet
        obj = BayanObject(class_def, self.interpreter, arguments=None)

        # Note: For multiple inheritance, we now rely on methods_map and MRO
        # rather than constructing parent objects.

        # Now call constructor after any metadata is available
        if arguments is not None:
            obj._call_constructor(arguments)

        return obj

    def get_class(self, class_name):
        """Get a class definition"""
        return self.classes.get(class_name)

    def is_subclass(self, child_name, parent_name):
        """Check if child is subclass of parent (supports multiple bases)"""
        if child_name == parent_name:
            return True

        for base in self.inheritance_map.get(child_name, []):
            if self.is_subclass(base, parent_name):
                return True
        return False

    def get_mro(self, class_name):
        """Compute C3 linearization (MRO) for a class by name."""
        # Cache simple MRO if needed (omitted for brevity); compute on demand
        bases = self.inheritance_map.get(class_name, [])
        if not bases:
            return [class_name]

        def merge(seqs):
            result = []
            seqs = [list(s) for s in seqs if s]
            while seqs:
                for seq in seqs:
                    candidate = seq[0]
                    if all(candidate not in s[1:] for s in seqs):
                        break
                else:
                    raise RuntimeError("Inconsistent hierarchy for C3 MRO")
                result.append(candidate)
                for s in list(seqs):
                    if s and s[0] == candidate:
                        s.pop(0)
                    if not s:
                        seqs.remove(s)
            return result

        parent_mros = [self.get_mro(b) for b in bases]
        return [class_name] + merge(parent_mros + [bases])

    def resolve_method(self, class_name, method_name, start_after=None):
        """Find method definition and its owner class via MRO.
        If start_after is provided, search strictly after that class in MRO.
        Returns (owner_class_name, FunctionDef) or (None, None).
        """
        mro = self.get_mro(class_name)
        start_index = 0
        if start_after is not None and start_after in mro:
            start_index = mro.index(start_after) + 1
        for cname in mro[start_index:]:
            methods = self.methods_map.get(cname, {})
            if method_name in methods:
                return cname, methods[method_name]
        return None, None
