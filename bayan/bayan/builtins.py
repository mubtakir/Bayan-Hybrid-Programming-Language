"""
Built-in functions and utilities for Bayan Language
دوال مدمجة وأدوات للغة بيان
"""

from .logical_engine import Term, Predicate

class BuiltinFunctions:
    """Collection of built-in functions"""
    
    @staticmethod
    def member(element, lst):
        """Check if element is member of list"""
        return element in lst
    
    @staticmethod
    def append(lst, element):
        """Append element to list"""
        lst.append(element)
        return lst
    
    @staticmethod
    def length(lst):
        """Get length of list"""
        return len(lst)
    
    @staticmethod
    def reverse(lst):
        """Reverse a list"""
        return list(reversed(lst))
    
    @staticmethod
    def sort(lst):
        """Sort a list"""
        return sorted(lst)
    
    @staticmethod
    def max_val(lst):
        """Get maximum value from list"""
        return max(lst)
    
    @staticmethod
    def min_val(lst):
        """Get minimum value from list"""
        return min(lst)
    
    @staticmethod
    def sum_val(lst):
        """Sum all values in list"""
        return sum(lst)
    
    @staticmethod
    def average(lst):
        """Calculate average of list"""
        return sum(lst) / len(lst) if lst else 0
    
    @staticmethod
    def abs_val(x):
        """Absolute value"""
        return abs(x)
    
    @staticmethod
    def power(x, y):
        """Power function"""
        return x ** y
    
    @staticmethod
    def sqrt(x):
        """Square root"""
        return x ** 0.5
    
    @staticmethod
    def round_val(x, decimals=0):
        """Round a number"""
        return round(x, decimals)
    
    @staticmethod
    def floor_val(x):
        """Floor function"""
        import math
        return math.floor(x)
    
    @staticmethod
    def ceil_val(x):
        """Ceiling function"""
        import math
        return math.ceil(x)
    
    @staticmethod
    def upper(s):
        """Convert string to uppercase"""
        return s.upper()
    
    @staticmethod
    def lower(s):
        """Convert string to lowercase"""
        return s.lower()
    
    @staticmethod
    def strip(s):
        """Strip whitespace from string"""
        return s.strip()
    
    @staticmethod
    def split(s, delimiter=' '):
        """Split string"""
        return s.split(delimiter)
    
    @staticmethod
    def join(lst, delimiter=''):
        """Join list into string"""
        return delimiter.join(str(x) for x in lst)
    
    @staticmethod
    def replace(s, old, new):
        """Replace substring"""
        return s.replace(old, new)
    
    @staticmethod
    def contains(s, substring):
        """Check if string contains substring"""
        return substring in s
    
    @staticmethod
    def starts_with(s, prefix):
        """Check if string starts with prefix"""
        return s.startswith(prefix)
    
    @staticmethod
    def ends_with(s, suffix):
        """Check if string ends with suffix"""
        return s.endswith(suffix)
    
    @staticmethod
    def find(s, substring):
        """Find index of substring"""
        return s.find(substring)
    
    @staticmethod
    def keys(d):
        """Get dictionary keys"""
        return list(d.keys())
    
    @staticmethod
    def values(d):
        """Get dictionary values"""
        return list(d.values())
    
    @staticmethod
    def items(d):
        """Get dictionary items"""
        return list(d.items())
    
    @staticmethod
    def get(d, key, default=None):
        """Get value from dictionary"""
        return d.get(key, default)
    
    @staticmethod
    def set_val(d, key, value):
        """Set value in dictionary"""
        d[key] = value
        return d
    
    @staticmethod
    def delete(d, key):
        """Delete key from dictionary"""
        if key in d:
            del d[key]
        return d
    
    @staticmethod
    def type_of(obj):
        """Get type of object"""
        return type(obj).__name__
    
    @staticmethod
    def is_number(obj):
        """Check if object is number"""
        return isinstance(obj, (int, float))
    
    @staticmethod
    def is_string(obj):
        """Check if object is string"""
        return isinstance(obj, str)
    
    @staticmethod
    def is_list(obj):
        """Check if object is list"""
        return isinstance(obj, list)
    
    @staticmethod
    def is_dict(obj):
        """Check if object is dictionary"""
        return isinstance(obj, dict)
    
    @staticmethod
    def is_boolean(obj):
        """Check if object is boolean"""
        return isinstance(obj, bool)
    
    @staticmethod
    def is_none(obj):
        """Check if object is None"""
        return obj is None
    
    @staticmethod
    def to_string(obj):
        """Convert object to string"""
        return str(obj)
    
    @staticmethod
    def to_number(obj):
        """Convert object to number"""
        try:
            if isinstance(obj, float):
                return obj
            return int(obj)
        except:
            return float(obj)
    
    @staticmethod
    def to_list(obj):
        """Convert object to list"""
        return list(obj)
    
    @staticmethod
    def to_dict(obj):
        """Convert object to dictionary"""
        if isinstance(obj, dict):
            return obj
        return {}

class LogicalBuiltins:
    """Built-in logical predicates"""
    
    @staticmethod
    def create_member_rules(engine):
        """Add member/2 predicate to logical engine"""
        # member(X, [X|_]).
        # member(X, [_|T]) :- member(X, T).
        pass
    
    @staticmethod
    def create_append_rules(engine):
        """Add append/3 predicate to logical engine"""
        # append([], L, L).
        # append([H|T1], L2, [H|T3]) :- append(T1, L2, T3).
        pass
    
    @staticmethod
    def create_length_rules(engine):
        """Add length/2 predicate to logical engine"""
        # length([], 0).
        # length([_|T], N) :- length(T, N1), N is N1 + 1.
        pass

