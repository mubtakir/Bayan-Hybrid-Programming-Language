"""
Import System for Bayan Language
نظام الاستيراد للغة بيان
"""

import importlib
import sys

class ImportSystem:
    """Manages importing Python modules and libraries"""
    
    # Whitelist of safe modules
    SAFE_MODULES = {
        'math', 'random', 'datetime', 'time', 'os', 'sys',
        'json', 'csv', 're', 'collections', 'itertools',
        'functools', 'operator', 'string', 'statistics',
        'decimal', 'fractions', 'numbers', 'cmath',
        'urllib', 'urllib.request', 'urllib.parse',
        'http', 'http.client', 'email', 'base64',
        'hashlib', 'hmac', 'secrets', 'sqlite3',
        'pickle', 'shelve', 'dbm', 'zlib', 'gzip',
        'bz2', 'lzma', 'zipfile', 'tarfile', 'io',
        'pathlib', 'glob', 'fnmatch', 'linecache',
        'shutil', 'tempfile', 'struct', 'codecs',
        'unicodedata', 'stringprep', 'readline',
        'rlcompleter', 'pprint', 'reprlib', 'enum',
        'types', 'copy', 'pydoc', 'doctest', 'unittest',
        'logging', 'getpass', 'curses', 'platform',
        'errno', 'ctypes', 'threading', 'multiprocessing',
        'subprocess', 'socket', 'ssl', 'select',
        'selectors', 'asyncio', 'signal', 'mmap',
        'array', 'weakref', 'types', 'copy',
        'pprint', 'reprlib', 'enum', 'graphlib',
        'heapq', 'bisect', 'queue', 'sched',
        'mutex', 'dummy_thread', 'dummy_threading',
        'contextvars', 'abc', 'atexit', 'traceback',
        'gc', 'inspect', 'site', 'user', 'builtins',
        'numpy', 'pandas', 'matplotlib', 'scipy',
        'sklearn', 'tensorflow', 'torch', 'requests',
        'flask', 'django', 'sqlalchemy', 'pytest',
        # Project-local safe modules (examples/utilities)
        'myutils'
    }
    
    def __init__(self):
        """Initialize import system"""
        self.imported_modules = {}
        self.module_aliases = {}
    
    def import_module(self, module_name, alias=None):
        """Import a Python module"""
        # Check if module is safe
        if not self._is_safe_module(module_name):
            raise ImportError(f"Module '{module_name}' is not in the safe list")
        
        # Check if already imported
        if module_name in self.imported_modules:
            module = self.imported_modules[module_name]
        else:
            try:
                module = importlib.import_module(module_name)
                self.imported_modules[module_name] = module
            except ImportError as e:
                raise ImportError(f"Cannot import module '{module_name}': {e}")
        
        # Register alias if provided
        if alias:
            self.module_aliases[alias] = module_name
        
        return module
    
    def import_from_module(self, module_name, names, aliases=None):
        """Import specific names from a module"""
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
            else:
                raise ImportError(f"Cannot import name '{name}' from '{module_name}'")
            
            # Register alias if provided
            if aliases and i < len(aliases) and aliases[i]:
                self.module_aliases[aliases[i]] = name
        
        return imported
    
    def get_module(self, module_name):
        """Get an imported module"""
        if module_name in self.module_aliases:
            actual_name = self.module_aliases[module_name]
            return self.imported_modules.get(actual_name)
        return self.imported_modules.get(module_name)
    
    def get_attribute(self, module_name, attr_name):
        """Get an attribute from a module"""
        module = self.get_module(module_name)
        if module is None:
            raise NameError(f"Module '{module_name}' not imported")
        
        if hasattr(module, attr_name):
            return getattr(module, attr_name)
        else:
            raise AttributeError(f"Module '{module_name}' has no attribute '{attr_name}'")
    
    def _is_safe_module(self, module_name):
        """Check if a module is safe to import"""
        # Check exact match
        if module_name in self.SAFE_MODULES:
            return True
        
        # Check parent modules (e.g., urllib.request -> urllib)
        parts = module_name.split('.')
        for i in range(len(parts)):
            parent = '.'.join(parts[:i+1])
            if parent in self.SAFE_MODULES:
                return True
        
        return False
    
    def list_imported_modules(self):
        """List all imported modules"""
        return list(self.imported_modules.keys())
    
    def clear_imports(self):
        """Clear all imports"""
        self.imported_modules.clear()
        self.module_aliases.clear()


