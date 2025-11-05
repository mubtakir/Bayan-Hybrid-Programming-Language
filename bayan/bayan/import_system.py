"""
Import System for Bayan Language
نظام الاستيراد للغة بيان

Enhanced import system with:
- Dynamic whitelist management
- Conditional imports
- Package imports
- Local module imports
- Advanced error handling
"""

import importlib
import importlib.util
import sys
import os
from pathlib import Path

class ImportSystem:
    """Manages importing Python modules and libraries with enhanced features"""

    # Default whitelist of safe modules
    DEFAULT_SAFE_MODULES = {
        # Standard library - Math & Numbers
        'math', 'random', 'datetime', 'time', 'statistics',
        'decimal', 'fractions', 'numbers', 'cmath',

        # Standard library - Data structures
        'collections', 'itertools', 'array', 'heapq', 'bisect', 'queue',

        # Standard library - Functional
        'functools', 'operator',

        # Standard library - String & Text
        'string', 're', 'codecs', 'unicodedata', 'stringprep',

        # Standard library - File & IO
        'io', 'pathlib', 'glob', 'fnmatch', 'linecache',
        'shutil', 'tempfile', 'zipfile', 'tarfile',
        'gzip', 'bz2', 'lzma', 'zlib',

        # Standard library - Data formats
        'json', 'csv', 'pickle', 'shelve', 'dbm',

        # Standard library - Cryptography & Security
        'hashlib', 'hmac', 'secrets', 'base64',

        # Standard library - Internet & Networking
        'urllib', 'urllib.request', 'urllib.parse',
        'http', 'http.client', 'email', 'socket', 'ssl',
        'select', 'selectors',

        # Standard library - Concurrency
        'threading', 'multiprocessing', 'asyncio', 'signal',

        # Standard library - System & Platform
        'os', 'sys', 'platform', 'errno', 'ctypes', 'mmap',

        # Standard library - Development
        'logging', 'getpass', 'curses', 'pprint', 'reprlib',
        'pydoc', 'doctest', 'unittest', 'inspect', 'traceback',

        # Standard library - Utilities
        'types', 'copy', 'weakref', 'enum', 'graphlib',
        'sched', 'atexit', 'gc', 'site', 'builtins',
        'abc', 'contextvars', 'readline', 'rlcompleter',

        # Popular third-party libraries
        'numpy', 'pandas', 'matplotlib', 'scipy',
        'sklearn', 'tensorflow', 'torch', 'requests',
        'flask', 'django', 'sqlalchemy', 'pytest',
        'pytest-cov', 'coverage',

        # Project-local safe modules
        'myutils'
    }

    def __init__(self, safe_modules=None, allow_custom=False, custom_paths=None):
        """
        Initialize import system

        Args:
            safe_modules: Set of safe module names (uses defaults if None)
            allow_custom: Whether to allow custom modules to be added dynamically
            custom_paths: List of custom paths to search for modules
        """
        self.safe_modules = safe_modules or self.DEFAULT_SAFE_MODULES.copy()
        self.allow_custom = allow_custom
        self.custom_modules = set()
        self.custom_paths = custom_paths or []

        self.imported_modules = {}
        self.module_aliases = {}
        self.import_history = []  # Track import history for debugging
    
    def add_safe_module(self, module_name):
        """Add a module to the safe list dynamically"""
        if not self.allow_custom:
            raise PermissionError(f"Custom modules not allowed. Enable allow_custom=True")
        self.custom_modules.add(module_name)
        self.import_history.append(f"Added safe module: {module_name}")

    def add_custom_path(self, path):
        """Add a custom path to search for modules"""
        if not os.path.exists(path):
            raise ValueError(f"Path does not exist: {path}")
        self.custom_paths.append(path)
        self.import_history.append(f"Added custom path: {path}")

    def import_module(self, module_name, alias=None, default=None):
        """
        Import a Python module

        Args:
            module_name: Name of the module to import
            alias: Optional alias for the module
            default: Default value if import fails (for conditional imports)

        Returns:
            The imported module

        Raises:
            ImportError: If module is not safe or cannot be imported
        """
        # Check if module is safe
        if not self._is_safe_module(module_name):
            raise ImportError(
                f"Module '{module_name}' is not in the safe list. "
                f"Available modules: {', '.join(sorted(self.safe_modules)[:5])}..."
            )

        # Check if already imported
        if module_name in self.imported_modules:
            module = self.imported_modules[module_name]
            self.import_history.append(f"Cached import: {module_name}")
        else:
            try:
                module = importlib.import_module(module_name)
                self.imported_modules[module_name] = module
                self.import_history.append(f"Imported: {module_name}")
            except ImportError as e:
                if default is not None:
                    self.import_history.append(f"Import failed (using default): {module_name}")
                    return default
                raise ImportError(
                    f"Cannot import module '{module_name}': {str(e)}. "
                    f"Make sure the module is installed."
                )

        # Register alias if provided
        if alias:
            self.module_aliases[alias] = module_name
            self.import_history.append(f"Registered alias: {alias} -> {module_name}")

        return module
    
    def import_from_module(self, module_name, names, aliases=None):
        """
        Import specific names from a module

        Args:
            module_name: Name of the module
            names: List of names to import
            aliases: Optional list of aliases for the names

        Returns:
            Dictionary of imported names
        """
        # Check if module is safe
        if not self._is_safe_module(module_name):
            raise ImportError(f"Module '{module_name}' is not in the safe list")

        # Import the module
        module = self.import_module(module_name)

        # Extract requested names
        imported = {}
        for i, name in enumerate(names):
            if hasattr(module, name):
                imported[name] = getattr(module, name)
                self.import_history.append(f"Imported from {module_name}: {name}")
            else:
                available = [attr for attr in dir(module) if not attr.startswith('_')]
                raise ImportError(
                    f"Cannot import name '{name}' from '{module_name}'. "
                    f"Available: {', '.join(available[:5])}..."
                )

            # Register alias if provided
            if aliases and i < len(aliases) and aliases[i]:
                self.module_aliases[aliases[i]] = name
                self.import_history.append(f"Registered alias: {aliases[i]} -> {name}")

        return imported

    def import_local_module(self, file_path, module_name=None, alias=None):
        """
        Import a local Python file as a module

        Args:
            file_path: Path to the Python file
            module_name: Name for the module (defaults to filename without .py)
            alias: Optional alias for the module

        Returns:
            The imported module
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Module file not found: {file_path}")

        if not path.suffix == '.py':
            raise ValueError(f"File must be a Python file (.py): {file_path}")

        if module_name is None:
            module_name = path.stem

        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Cannot load module from {file_path}")

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            self.imported_modules[module_name] = module
            self.import_history.append(f"Imported local module: {file_path}")

            if alias:
                self.module_aliases[alias] = module_name
                self.import_history.append(f"Registered alias: {alias} -> {module_name}")

            return module
        except Exception as e:
            raise ImportError(f"Failed to import local module {file_path}: {str(e)}")
    
    def get_module(self, module_name):
        """
        Get an imported module by name or alias

        Args:
            module_name: Name or alias of the module

        Returns:
            The module object or None if not found
        """
        if module_name in self.module_aliases:
            actual_name = self.module_aliases[module_name]
            return self.imported_modules.get(actual_name)
        return self.imported_modules.get(module_name)

    def get_attribute(self, module_name, attr_name):
        """
        Get an attribute from a module

        Args:
            module_name: Name or alias of the module
            attr_name: Name of the attribute

        Returns:
            The attribute value

        Raises:
            NameError: If module not imported
            AttributeError: If attribute not found
        """
        module = self.get_module(module_name)
        if module is None:
            raise NameError(f"Module '{module_name}' not imported")

        if hasattr(module, attr_name):
            return getattr(module, attr_name)
        else:
            available = [attr for attr in dir(module) if not attr.startswith('_')]
            raise AttributeError(
                f"Module '{module_name}' has no attribute '{attr_name}'. "
                f"Available: {', '.join(available[:5])}..."
            )

    def _is_safe_module(self, module_name):
        """
        Check if a module is safe to import

        Args:
            module_name: Name of the module to check

        Returns:
            True if module is safe, False otherwise
        """
        # Check exact match in safe modules
        if module_name in self.safe_modules:
            return True

        # Check custom modules if allowed
        if self.allow_custom and module_name in self.custom_modules:
            return True

        # Check parent modules (e.g., urllib.request -> urllib)
        parts = module_name.split('.')
        for i in range(len(parts)):
            parent = '.'.join(parts[:i+1])
            if parent in self.safe_modules:
                return True
            if self.allow_custom and parent in self.custom_modules:
                return True

        return False

    def list_imported_modules(self):
        """List all imported modules"""
        return list(self.imported_modules.keys())

    def list_safe_modules(self):
        """List all safe modules"""
        return sorted(list(self.safe_modules))

    def list_custom_modules(self):
        """List all custom modules"""
        return sorted(list(self.custom_modules))

    def get_import_history(self):
        """Get the import history for debugging"""
        return self.import_history.copy()

    def clear_imports(self):
        """Clear all imports"""
        self.imported_modules.clear()
        self.module_aliases.clear()
        self.import_history.append("Cleared all imports")

    def get_statistics(self):
        """Get import system statistics"""
        return {
            'imported_modules': len(self.imported_modules),
            'aliases': len(self.module_aliases),
            'safe_modules': len(self.safe_modules),
            'custom_modules': len(self.custom_modules),
            'custom_paths': len(self.custom_paths),
            'history_entries': len(self.import_history)
        }


