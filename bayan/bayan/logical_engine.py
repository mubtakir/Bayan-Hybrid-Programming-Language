"""
Logical Engine for Bayan Language
محرك منطقي للغة بيان
"""

class Term:
    """Represents a logical term (constant, variable, or compound)"""
    def __init__(self, value, is_variable=False):
        self.value = value
        self.is_variable = is_variable
    
    def __repr__(self):
        if self.is_variable:
            return f"?{self.value}"
        return str(self.value)
    
    def __eq__(self, other):
        if not isinstance(other, Term):
            return False
        return self.value == other.value and self.is_variable == other.is_variable
    
    def __hash__(self):
        return hash((self.value, self.is_variable))

class Predicate:
    """Represents a logical predicate"""
    def __init__(self, name, args):
        self.name = name
        self.args = args  # List of Term objects
    
    def __repr__(self):
        args_str = ", ".join(str(arg) for arg in self.args)
        return f"{self.name}({args_str})"
    
    def __eq__(self, other):
        if not isinstance(other, Predicate):
            return False
        return self.name == other.name and self.args == other.args

class Fact:
    """Represents a logical fact"""
    def __init__(self, predicate):
        self.predicate = predicate
    
    def __repr__(self):
        return f"{self.predicate}."

class Rule:
    """Represents a logical rule: head :- body"""
    def __init__(self, head, body):
        self.head = head  # Predicate
        self.body = body  # List of Predicates
    
    def __repr__(self):
        body_str = ", ".join(str(p) for p in self.body)
        return f"{self.head} :- {body_str}."

class Substitution:
    """Represents variable substitutions"""
    def __init__(self, bindings=None):
        self.bindings = bindings or {}
    
    def bind(self, var_name, value):
        """Bind a variable to a value"""
        self.bindings[var_name] = value
    
    def lookup(self, var_name):
        """Look up a variable"""
        return self.bindings.get(var_name)
    
    def copy(self):
        """Create a copy of this substitution"""
        return Substitution(self.bindings.copy())
    
    def __repr__(self):
        return f"Substitution({self.bindings})"

class LogicalEngine:
    """The logical inference engine"""
    
    def __init__(self):
        self.knowledge_base = {}  # {predicate_name: [facts/rules]}
        self.call_stack = []
        self.max_depth = 1000
    
    def add_fact(self, fact):
        """Add a fact to the knowledge base"""
        pred_name = fact.predicate.name
        if pred_name not in self.knowledge_base:
            self.knowledge_base[pred_name] = []
        self.knowledge_base[pred_name].append(fact)
    
    def add_rule(self, rule):
        """Add a rule to the knowledge base"""
        pred_name = rule.head.name
        if pred_name not in self.knowledge_base:
            self.knowledge_base[pred_name] = []
        self.knowledge_base[pred_name].append(rule)

    def assertz(self, fact_or_rule):
        """Add a fact or rule at the end of the knowledge base (Prolog assertz)"""
        if isinstance(fact_or_rule, Fact):
            self.add_fact(fact_or_rule)
        elif isinstance(fact_or_rule, Rule):
            self.add_rule(fact_or_rule)
        else:
            raise TypeError("assertz requires a Fact or Rule")

    def asserta(self, fact_or_rule):
        """Add a fact or rule at the beginning of the knowledge base (Prolog asserta)"""
        if isinstance(fact_or_rule, Fact):
            pred_name = fact_or_rule.predicate.name
            if pred_name not in self.knowledge_base:
                self.knowledge_base[pred_name] = []
            self.knowledge_base[pred_name].insert(0, fact_or_rule)
        elif isinstance(fact_or_rule, Rule):
            pred_name = fact_or_rule.head.name
            if pred_name not in self.knowledge_base:
                self.knowledge_base[pred_name] = []
            self.knowledge_base[pred_name].insert(0, fact_or_rule)
        else:
            raise TypeError("asserta requires a Fact or Rule")

    def retract(self, predicate):
        """Remove the first matching fact or rule from the knowledge base (Prolog retract)"""
        pred_name = predicate.name
        if pred_name not in self.knowledge_base:
            return False

        # Find and remove first matching fact/rule
        for i, item in enumerate(self.knowledge_base[pred_name]):
            if isinstance(item, Fact):
                if self._unify(item.predicate, predicate, Substitution()) is not None:
                    self.knowledge_base[pred_name].pop(i)
                    return True
            elif isinstance(item, Rule):
                if self._unify(item.head, predicate, Substitution()) is not None:
                    self.knowledge_base[pred_name].pop(i)
                    return True
        return False

    def retractall(self, predicate):
        """Remove all matching facts or rules from the knowledge base (Prolog retractall)"""
        pred_name = predicate.name
        if pred_name not in self.knowledge_base:
            return 0

        # Find and remove all matching facts/rules
        count = 0
        items_to_keep = []
        for item in self.knowledge_base[pred_name]:
            if isinstance(item, Fact):
                if self._unify(item.predicate, predicate, Substitution()) is None:
                    items_to_keep.append(item)
                else:
                    count += 1
            elif isinstance(item, Rule):
                if self._unify(item.head, predicate, Substitution()) is None:
                    items_to_keep.append(item)
                else:
                    count += 1

        self.knowledge_base[pred_name] = items_to_keep
        return count

    def query(self, goal, substitution=None):
        """Execute a query and return all solutions"""
        if substitution is None:
            substitution = Substitution()
        
        if len(self.call_stack) > self.max_depth:
            raise RuntimeError("Maximum recursion depth exceeded")
        
        self.call_stack.append(goal)
        try:
            solutions = self._solve_goal(goal, substitution)
        finally:
            self.call_stack.pop()
        
        return solutions
    
    def _solve_goal(self, goal, substitution):
        """Solve a single goal (predicate, IsExpression, or comparison)"""
        from .ast_nodes import IsExpression

        solutions = []

        # Handle IsExpression: ?X is 5 + 3
        if isinstance(goal, IsExpression):
            result = self._evaluate_is_expression(goal, substitution)
            if result is not None:
                solutions.append(result)
            return solutions

        # Handle comparison predicates: _compare_>, _compare_<, etc.
        if isinstance(goal, Predicate) and goal.name.startswith('_compare_'):
            result = self._evaluate_comparison(goal, substitution)
            if result is not None:
                solutions.append(result)
            return solutions

        # Handle built-in predicates
        if isinstance(goal, Predicate):
            # Handle findall/3: findall(?Template, ?Goal, ?Result)
            if goal.name == 'findall' and len(goal.args) == 3:
                return self._handle_findall(goal, substitution)

            # Handle bagof/3: bagof(?Template, ?Goal, ?Result)
            if goal.name == 'bagof' and len(goal.args) == 3:
                return self._handle_bagof(goal, substitution)

            # Handle setof/3: setof(?Template, ?Goal, ?Result)
            if goal.name == 'setof' and len(goal.args) == 3:
                return self._handle_setof(goal, substitution)

            # Handle not/1: not(?Goal) - negation as failure
            if goal.name == 'not' and len(goal.args) == 1:
                return self._handle_not(goal, substitution)

        # Apply current substitution to the goal
        goal = self._apply_substitution(goal, substitution)

        pred_name = goal.name
        if pred_name not in self.knowledge_base:
            return solutions

        # Try to unify with facts and rules
        for item in self.knowledge_base[pred_name]:
            if isinstance(item, Fact):
                # Try to unify with the fact
                new_sub = self._unify(goal, item.predicate, substitution.copy())
                if new_sub is not None:
                    solutions.append(new_sub)

            elif isinstance(item, Rule):
                # Try to prove the rule
                rule_solutions = self._prove_rule(item, goal, substitution)
                solutions.extend(rule_solutions)

        return solutions
    
    def _prove_rule(self, rule, goal, substitution):
        """Prove a rule"""
        solutions = []

        # Rename variables in the rule to avoid conflicts
        renamed_rule = self._rename_variables(rule)
        var_mapping = self.var_mapping.copy()  # Save the mapping

        # Unify the goal with the rule head
        head_sub = self._unify(goal, renamed_rule.head, substitution)
        if head_sub is None:
            return solutions

        # Prove the body
        body_solutions = self._prove_body(renamed_rule.body, head_sub)

        # Map renamed variables back to original variables
        for sol in body_solutions:
            for renamed_var, original_var in var_mapping.items():
                if renamed_var in sol.bindings:
                    sol.bindings[original_var] = sol.bindings[renamed_var]
            solutions.append(sol)

        return solutions
    
    def _prove_body(self, body, substitution):
        """Prove a list of goals (conjunction) with cut support"""
        from .ast_nodes import Cut

        if not body:
            return [substitution]

        solutions = []
        first_goal = body[0]
        rest_goals = body[1:]

        # Handle cut operator
        if isinstance(first_goal, Cut):
            # Cut prevents backtracking
            # Execute remaining goals without allowing backtracking
            if rest_goals:
                rest_solutions = self._prove_body(rest_goals, substitution)
                # Return only the first solution (or all solutions from remaining goals)
                # but prevent backtracking to alternative clauses
                return rest_solutions
            else:
                return [substitution]

        # Solve the first goal
        first_solutions = self._solve_goal(first_goal, substitution)

        # Check if there's a cut in the remaining goals
        has_cut = any(isinstance(g, Cut) for g in rest_goals)

        # For each solution, solve the rest
        for sol in first_solutions:
            if rest_goals:
                rest_solutions = self._prove_body(rest_goals, sol)
                solutions.extend(rest_solutions)

                # If we found a cut in the remaining goals, stop backtracking
                if has_cut and rest_solutions:
                    break
            else:
                solutions.append(sol)

        return solutions
    
    def _unify(self, term1, term2, substitution):
        """Unify two terms with support for list patterns [H|T]"""
        # Apply substitution
        term1 = self._deref(term1, substitution)
        term2 = self._deref(term2, substitution)

        # Handle list pattern unification
        # Case 1: ListPattern with list
        if self._is_list_pattern(term1) and isinstance(term2, list):
            return self._unify_list_pattern(term1, term2, substitution)
        elif isinstance(term1, list) and self._is_list_pattern(term2):
            return self._unify_list_pattern(term2, term1, substitution)

        # Case 2: Two ListPatterns
        elif self._is_list_pattern(term1) and self._is_list_pattern(term2):
            # Convert both to lists and unify
            # This is complex - for now, fail
            return None

        # Case 3: Two lists
        elif isinstance(term1, list) and isinstance(term2, list):
            if len(term1) != len(term2):
                return None
            for e1, e2 in zip(term1, term2):
                substitution = self._unify(e1, e2, substitution)
                if substitution is None:
                    return None
            return substitution

        # If they're the same, unification succeeds
        if isinstance(term1, Term) and isinstance(term2, Term):
            if term1.value == term2.value and term1.is_variable == term2.is_variable:
                return substitution
        elif isinstance(term1, str) and isinstance(term2, str):
            if term1 == term2:
                return substitution
        elif isinstance(term1, str) and isinstance(term2, Term):
            if term2.is_variable:
                if self._occurs_check(term2.value, term1, substitution):
                    return None
                substitution.bind(term2.value, term1)
                return substitution
            else:
                if term1 == term2.value:
                    return substitution
        elif isinstance(term1, Term) and isinstance(term2, str):
            if term1.is_variable:
                if self._occurs_check(term1.value, term2, substitution):
                    return None
                substitution.bind(term1.value, term2)
                return substitution
            else:
                if term1.value == term2:
                    return substitution
        elif term1 == term2:
            return substitution

        # If term1 is a variable, bind it
        if isinstance(term1, Term) and term1.is_variable:
            if self._occurs_check(term1.value, term2, substitution):
                return None
            substitution.bind(term1.value, term2)
            return substitution

        # If term2 is a variable, bind it
        if isinstance(term2, Term) and term2.is_variable:
            if self._occurs_check(term2.value, term1, substitution):
                return None
            substitution.bind(term2.value, term1)
            return substitution

        # If both are predicates, unify their arguments
        if isinstance(term1, Predicate) and isinstance(term2, Predicate):
            if term1.name != term2.name or len(term1.args) != len(term2.args):
                return None

            for arg1, arg2 in zip(term1.args, term2.args):
                substitution = self._unify(arg1, arg2, substitution)
                if substitution is None:
                    return None

            return substitution

        # Otherwise, unification fails
        return None

    def _is_list_pattern(self, term):
        """Check if term is a list pattern [H|T]"""
        # A list pattern is represented as a dict with 'head' and 'tail' keys
        return isinstance(term, dict) and 'list_pattern' in term

    def _unify_list_pattern(self, pattern, lst, substitution):
        """Unify a list pattern [H1, H2, ...|T] with a list"""
        if not isinstance(pattern, dict) or 'list_pattern' not in pattern:
            return None

        head_elements = pattern['head']
        tail_var = pattern['tail']

        # Check if list has enough elements
        if len(lst) < len(head_elements):
            return None

        # Unify head elements
        for i, head_elem in enumerate(head_elements):
            substitution = self._unify(head_elem, lst[i], substitution)
            if substitution is None:
                return None

        # Unify tail with remaining elements
        remaining = lst[len(head_elements):]
        substitution = self._unify(tail_var, remaining, substitution)

        return substitution
    
    def _deref(self, term, substitution):
        """Dereference a term by following variable bindings"""
        if isinstance(term, Term) and term.is_variable:
            value = substitution.lookup(term.value)
            if value is not None:
                # If value is a Term, dereference it recursively
                if isinstance(value, Term):
                    return self._deref(value, substitution)
                else:
                    # If value is a string, return it as is
                    return value
        return term
    
    def _occurs_check(self, var_name, term, substitution):
        """Check if a variable occurs in a term (prevents infinite structures)"""
        term = self._deref(term, substitution)
        
        if isinstance(term, Term):
            if term.is_variable and term.value == var_name:
                return True
        elif isinstance(term, Predicate):
            for arg in term.args:
                if self._occurs_check(var_name, arg, substitution):
                    return True
        
        return False
    
    def _apply_substitution(self, term, substitution):
        """Apply substitution to a term"""
        if isinstance(term, Predicate):
            new_args = []
            for arg in term.args:
                deref_arg = self._deref(arg, substitution)
                if isinstance(deref_arg, Predicate):
                    new_args.append(self._apply_substitution(deref_arg, substitution))
                elif isinstance(deref_arg, Term):
                    new_args.append(deref_arg)
                else:
                    # If it's a string, convert it to a Term
                    new_args.append(Term(deref_arg, is_variable=False))
            return Predicate(term.name, new_args)

        deref_term = self._deref(term, substitution)
        if isinstance(deref_term, Term):
            return deref_term
        else:
            # If it's a string, convert it to a Term
            return Term(deref_term, is_variable=False)
    
    def _rename_variables(self, rule):
        """Rename variables in a rule to avoid conflicts"""
        import time
        suffix = str(int(time.time() * 1000000) % 1000000)
        self.var_mapping = {}  # Store mapping from renamed to original

        def rename_term(term):
            if isinstance(term, Term) and term.is_variable:
                renamed = f"{term.value}_{suffix}"
                self.var_mapping[renamed] = term.value  # Store mapping
                return Term(renamed, is_variable=True)
            elif isinstance(term, Predicate):
                new_args = [rename_term(arg) for arg in term.args]
                return Predicate(term.name, new_args)
            return term

        new_head = rename_term(rule.head)
        new_body = [rename_term(goal) for goal in rule.body]

        return Rule(new_head, new_body)

    def _evaluate_is_expression(self, is_expr, substitution):
        """Evaluate an 'is' expression: ?X is 5 + 3"""
        from .ast_nodes import BinaryOp, Number, Variable

        # Evaluate the arithmetic expression
        result = self._evaluate_arithmetic(is_expr.expression, substitution)

        if result is None:
            return None

        # Unify the variable with the result
        new_sub = self._unify(is_expr.variable, result, substitution.copy())
        return new_sub

    def _evaluate_arithmetic(self, expr, substitution):
        """Evaluate an arithmetic expression"""
        from .ast_nodes import BinaryOp, Number, Variable, UnaryOp

        # Handle numbers
        if isinstance(expr, Number):
            return expr.value

        # Handle plain numbers (int/float)
        if isinstance(expr, (int, float)):
            return expr

        # Handle variables
        if isinstance(expr, Variable):
            var_name = expr.name
            if var_name.startswith('?'):
                var_name = var_name[1:]
            value = substitution.lookup(var_name)
            if value is not None:
                return self._evaluate_arithmetic(value, substitution)
            return None

        # Handle Terms
        if isinstance(expr, Term):
            if expr.is_variable:
                value = substitution.lookup(expr.value)
                if value is not None:
                    return self._evaluate_arithmetic(value, substitution)
                return None
            else:
                # Try to convert to number
                try:
                    return float(expr.value) if '.' in str(expr.value) else int(expr.value)
                except:
                    return None

        # Handle binary operations
        if isinstance(expr, BinaryOp):
            left = self._evaluate_arithmetic(expr.left, substitution)
            right = self._evaluate_arithmetic(expr.right, substitution)

            if left is None or right is None:
                return None

            op = expr.operator
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                return left / right if right != 0 else None
            elif op == '%':
                return left % right if right != 0 else None
            elif op == '**':
                return left ** right
            else:
                return None

        # Handle unary operations
        if isinstance(expr, UnaryOp):
            operand = self._evaluate_arithmetic(expr.operand, substitution)
            if operand is None:
                return None

            if expr.operator == '-':
                return -operand
            elif expr.operator == '+':
                return operand
            else:
                return None

        return None

    def _evaluate_comparison(self, comp_pred, substitution):
        """Evaluate a comparison predicate: _compare_>, _compare_<, etc."""
        # Extract operator from predicate name
        op = comp_pred.name.replace('_compare_', '')

        # Get the two arguments
        if len(comp_pred.args) != 2:
            return None

        left = self._evaluate_arithmetic(comp_pred.args[0], substitution)
        right = self._evaluate_arithmetic(comp_pred.args[1], substitution)

        if left is None or right is None:
            return None

        # Perform comparison
        result = False
        if op == '>':
            result = left > right
        elif op == '<':
            result = left < right
        elif op == '>=':
            result = left >= right
        elif op == '<=':
            result = left <= right
        elif op == '==':
            result = left == right
        elif op == '!=':
            result = left != right

        # If comparison succeeds, return the substitution unchanged
        if result:
            return substitution
        else:
            return None

    def _handle_findall(self, findall_pred, substitution):
        """Handle findall/3: findall(?Template, ?Goal, ?Result)

        Collects all solutions of Goal and instantiates Template for each,
        returning the list in Result.

        Example: findall(?X, parent(?X, john), ?List)
        """
        template = findall_pred.args[0]
        goal = findall_pred.args[1]
        result_var = findall_pred.args[2]

        # Find all solutions to the goal
        solutions = self._solve_goal(goal, substitution)

        # Collect instantiated templates
        results = []
        for sol in solutions:
            instantiated = self._apply_substitution(template, sol)
            # Convert Term to actual value
            if isinstance(instantiated, Term):
                results.append(instantiated.value)
            else:
                results.append(instantiated)

        # Unify the result with the result variable
        new_sub = self._unify(result_var, results, substitution.copy())

        if new_sub is not None:
            return [new_sub]
        return []

    def _handle_bagof(self, bagof_pred, substitution):
        """Handle bagof/3: bagof(?Template, ?Goal, ?Result)

        Like findall, but fails if there are no solutions.
        Collects all solutions of Goal and instantiates Template for each,
        returning the list in Result.

        Example: bagof(?X, parent(?X, john), ?List)
        """
        template = bagof_pred.args[0]
        goal = bagof_pred.args[1]
        result_var = bagof_pred.args[2]

        # Find all solutions to the goal
        solutions = self._solve_goal(goal, substitution)

        # bagof fails if there are no solutions (unlike findall)
        if not solutions:
            return []

        # Collect instantiated templates
        results = []
        for sol in solutions:
            instantiated = self._apply_substitution(template, sol)
            # Convert Term to actual value
            if isinstance(instantiated, Term):
                results.append(instantiated.value)
            else:
                results.append(instantiated)

        # Unify the result with the result variable
        new_sub = self._unify(result_var, results, substitution.copy())

        if new_sub is not None:
            return [new_sub]
        return []

    def _handle_setof(self, setof_pred, substitution):
        """Handle setof/3: setof(?Template, ?Goal, ?Result)

        Like bagof, but removes duplicates and sorts the results.
        Fails if there are no solutions.

        Example: setof(?X, parent(?X, john), ?List)
        """
        template = setof_pred.args[0]
        goal = setof_pred.args[1]
        result_var = setof_pred.args[2]

        # Find all solutions to the goal
        solutions = self._solve_goal(goal, substitution)

        # setof fails if there are no solutions
        if not solutions:
            return []

        # Collect instantiated templates
        results = []
        for sol in solutions:
            instantiated = self._apply_substitution(template, sol)
            # Convert Term to actual value
            if isinstance(instantiated, Term):
                results.append(instantiated.value)
            else:
                results.append(instantiated)

        # Remove duplicates and sort
        # Convert to set to remove duplicates, then back to sorted list
        try:
            unique_results = list(set(results))
            unique_results.sort()
        except TypeError:
            # If items are not sortable (e.g., mixed types), just remove duplicates
            unique_results = []
            seen = set()
            for item in results:
                if item not in seen:
                    unique_results.append(item)
                    seen.add(item)

        # Unify the result with the result variable
        new_sub = self._unify(result_var, unique_results, substitution.copy())

        if new_sub is not None:
            return [new_sub]
        return []

    def _handle_not(self, not_pred, substitution):
        """Handle not/1: not(?Goal) - negation as failure

        Succeeds if Goal fails, fails if Goal succeeds.

        Example: not(parent(john, mary))
        """
        goal = not_pred.args[0]

        # Try to solve the goal
        solutions = self._solve_goal(goal, substitution)

        # Negation as failure: succeed if no solutions found
        if len(solutions) == 0:
            return [substitution]
        return []

