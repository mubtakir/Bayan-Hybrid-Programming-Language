"""
Hybrid Parser for Bayan Language
محلل نحوي هجين للغة بيان
"""

from .lexer import TokenType
from .ast_nodes import *
from .logical_engine import Term, Predicate, Fact, Rule

class HybridParser:
    """Hybrid parser for Bayan language"""

    def __init__(self, tokens, filename=None):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
        self.filename = filename

    def advance(self):
        """Move to the next token"""
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None

    def peek(self, lookahead=1):
        """Look ahead at the next token"""
        pos = self.position + lookahead
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None

    def match(self, *token_types):
        """Check if current token matches any of the given types"""
        if self.current_token is None:
            return False
        return self.current_token.type in token_types

    def eat(self, token_type):
        """Consume a token of the given type"""
        if self.current_token is None or self.current_token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type}, got {self.current_token.type if self.current_token else 'EOF'}"
            )
        token = self.current_token
        self.advance()
        return token
    def _with_pos(self, node, tok):
        """Attach source position from token to node if supported"""
        if node is not None and hasattr(node, 'with_pos') and tok is not None:
            node.with_pos(getattr(tok, 'line', None), getattr(tok, 'column', None), getattr(self, 'filename', None))
        return node


    def parse(self):
        """Parse the entire program"""
        statements = []

        while self.current_token and self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)

        return Program(statements)

    def parse_statement(self):
        """Parse a single statement"""
        if self.match(TokenType.HYBRID):
            return self.parse_hybrid_block()
        elif self.match(TokenType.DEF):
            return self.parse_function_def()
        elif self.match(TokenType.CLASS):
            return self.parse_class_def()
        elif self.match(TokenType.IF):
            return self.parse_if_statement()
        elif self.match(TokenType.FOR):
            return self.parse_for_loop()
        elif self.match(TokenType.WHILE):
            return self.parse_while_loop()
        elif self.match(TokenType.RETURN):
            return self.parse_return_statement()
        elif self.match(TokenType.BREAK):
            self.advance()
            return BreakStatement()
        elif self.match(TokenType.CONTINUE):
            self.advance()
            return ContinueStatement()
        elif self.match(TokenType.PRINT):
            return self.parse_print_statement()
        elif self.match(TokenType.QUERY):
            return self.parse_query()
        elif self.match(TokenType.FACT):
            return self.parse_fact()
        elif self.match(TokenType.RULE):
            return self.parse_rule()
        elif self.match(TokenType.IMPORT):
            return self.parse_import_statement()
        elif self.match(TokenType.FROM):
            return self.parse_from_import_statement()
        elif self.match(TokenType.IDENTIFIER):
            # Could be assignment or expression (supports chained obj.attr[index] = value)
            # Fast path: direct simple assignment `x = ...`
            if self.peek() and self.peek().type == TokenType.ASSIGN:
                return self.parse_assignment()
            # Lookahead to detect chained assignment targets like obj.attr or obj[index]
            elif self.peek() and (self.peek().type == TokenType.DOT or self.peek().type == TokenType.LBRACKET):
                saved_pos = self.position
                # Simulate scanning a target chain to see if it's followed by '=' at top-level
                i = self.position + 1  # start scanning after identifier
                depth_bracket = 0
                depth_paren = 0
                depth_brace = 0
                tokens = self.tokens
                n = len(tokens)
                is_assignment_chain = False
                while i < n:
                    t = tokens[i]
                    # Stop scanning at statement boundaries
                    if t.type in (TokenType.SEMICOLON, TokenType.RBRACE, TokenType.EOF):
                        break
                    # Track nesting so we only consider '=' at top level of the chain
                    if t.type == TokenType.LBRACKET:
                        depth_bracket += 1
                    elif t.type == TokenType.RBRACKET:
                        depth_bracket = max(0, depth_bracket - 1)
                    elif t.type == TokenType.LPAREN:
                        depth_paren += 1
                    elif t.type == TokenType.RPAREN:
                        depth_paren = max(0, depth_paren - 1)
                    elif t.type == TokenType.LBRACE:
                        depth_brace += 1
                    elif t.type == TokenType.RBRACE and depth_brace > 0:
                        depth_brace -= 1
                    # If we hit '=' at top-level of the chain, mark as assignment
                    if t.type == TokenType.ASSIGN and depth_bracket == 0 and depth_paren == 0 and depth_brace == 0:
                        is_assignment_chain = True
                        break
                    # Heuristic: chain can only contain DOT, LBRACKET groups, identifiers, literals inside brackets, and parentheses in indices
                    # If we encounter a token that cannot appear in a target chain and we're not inside brackets/paren, stop
                    if depth_bracket == 0 and depth_paren == 0 and depth_brace == 0 and t.type not in (TokenType.DOT, TokenType.LBRACKET, TokenType.RBRACKET, TokenType.IDENTIFIER, TokenType.STRING, TokenType.NUMBER, TokenType.RPAREN, TokenType.LPAREN, TokenType.COMMA):
                        break
                    i += 1
                if is_assignment_chain:
                    # Rewind and use the robust assignment parser that builds the correct node
                    self.position = saved_pos
                    self.current_token = self.tokens[self.position]
                    return self.parse_assignment()
                else:
                    # Not an assignment chain → it's an expression
                    self.position = saved_pos
                    self.current_token = self.tokens[self.position]
                    return self.parse_expression_statement()
            else:
                return self.parse_expression_statement()
        elif self.match(TokenType.SELF):
            # Could be assignments like self.attr = v, self.attr[idx] = v, self[idx] = v, or just expressions
            saved_pos = self.position
            self.advance()  # consume 'self'
            # Build a potential target chain starting from self
            target_expr = SelfReference()
            progressed = False
            while self.match(TokenType.DOT) or self.match(TokenType.LBRACKET):
                progressed = True
                if self.match(TokenType.DOT):
                    self.eat(TokenType.DOT)
                    attr_name = self.eat(TokenType.IDENTIFIER).value
                    target_expr = AttributeAccess(target_expr, attr_name)
                else:
                    self.eat(TokenType.LBRACKET)
                    index_expr = self.parse_expression()
                    self.eat(TokenType.RBRACKET)
                    target_expr = SubscriptAccess(target_expr, index_expr)
            # If after building the chain we see an assignment, construct the right node
            if progressed and self.match(TokenType.ASSIGN):
                self.eat(TokenType.ASSIGN)
                value = self.parse_expression()
                if isinstance(target_expr, AttributeAccess):
                    return AttributeAssignment(target_expr.object_expr, target_expr.attribute_name, value)
                elif isinstance(target_expr, SubscriptAccess):
                    return SubscriptAssignment(target_expr.object_expr, target_expr.index_expr, value)
                else:
                    raise SyntaxError("Invalid self-assignment target")
            # Otherwise, rewind and parse as a normal expression statement
            self.position = saved_pos
            self.current_token = self.tokens[self.position]
            return self.parse_expression_statement()
        else:
            return self.parse_expression_statement()

    def parse_hybrid_block(self):
        """Parse a hybrid block"""
        self.eat(TokenType.HYBRID)
        self.eat(TokenType.LBRACE)

        traditional_stmts = []
        logical_stmts = []

        while self.current_token and self.current_token.type != TokenType.RBRACE:
            if self.match(TokenType.QUERY):
                logical_stmts.append(self.parse_query())
            elif self.match(TokenType.RULE):
                logical_stmts.append(self.parse_rule())
            elif self.match(TokenType.FACT):
                logical_stmts.append(self.parse_fact())
            elif self.is_logical_rule():
                # Parse as logical rule
                logical_stmts.append(self.parse_rule())
            elif self.is_logical_fact():
                # Parse as logical fact
                logical_stmts.append(self.parse_fact())
            else:
                stmt = self.parse_statement()
                if stmt:
                    traditional_stmts.append(stmt)

        self.eat(TokenType.RBRACE)
        return HybridBlock(traditional_stmts, logical_stmts)

    def is_logical_fact(self):
        """Check if the current token is a logical fact (identifier followed by parentheses and dot)"""
        if not self.current_token or self.current_token.type != TokenType.IDENTIFIER:
            return False

        # Look ahead to see if it's followed by ( and eventually )
        saved_pos = self.position
        try:
            self.advance()  # Skip identifier
            if self.current_token and self.current_token.type == TokenType.LPAREN:
                # Count parentheses to find the matching closing paren
                paren_count = 1
                self.advance()
                while self.current_token and paren_count > 0:
                    if self.current_token.type == TokenType.LPAREN:
                        paren_count += 1
                    elif self.current_token.type == TokenType.RPAREN:
                        paren_count -= 1
                    self.advance()

                # Check if followed by DOT
                result = self.current_token and self.current_token.type == TokenType.DOT
                self.position = saved_pos
                self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None
                return result
        except:
            pass

        self.position = saved_pos
        self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None
        return False

    def is_logical_rule(self):
        """Check if the current token is a logical rule (predicate followed by :- and dot)"""
        if not self.current_token or self.current_token.type != TokenType.IDENTIFIER:
            return False

        # Look ahead to see if it's followed by ( and eventually :- and )
        saved_pos = self.position
        try:
            self.advance()  # Skip identifier
            if self.current_token and self.current_token.type == TokenType.LPAREN:
                # Count parentheses to find the matching closing paren
                paren_count = 1
                self.advance()
                while self.current_token and paren_count > 0:
                    if self.current_token.type == TokenType.LPAREN:
                        paren_count += 1
                    elif self.current_token.type == TokenType.RPAREN:
                        paren_count -= 1
                    self.advance()

                # Check if followed by IMPLIES (:-) or ARROW (←)
                result = self.current_token and self.current_token.type in (TokenType.IMPLIES, TokenType.ARROW)
                self.position = saved_pos
                self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None
                return result
        except:
            pass

        self.position = saved_pos
        self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None
        return False

    def parse_function_def(self):
        """Parse a function definition"""
        def_tok = self.eat(TokenType.DEF)
        name = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.LPAREN)
        params = self.parse_parameter_list()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.COLON)
        body = self.parse_block()

        return self._with_pos(FunctionDef(name, params, body), def_tok)

    def parse_parameter_list(self):
        """Parse function parameters"""
        params = []

        if not self.match(TokenType.RPAREN):
            params.append(self.eat(TokenType.IDENTIFIER).value)

            while self.match(TokenType.COMMA):
                self.eat(TokenType.COMMA)
                params.append(self.eat(TokenType.IDENTIFIER).value)

        return params

    def parse_block(self):
        """Parse a block of statements"""
        self.eat(TokenType.LBRACE)
        statements = []

        while self.current_token and self.current_token.type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)

        self.eat(TokenType.RBRACE)
        return Block(statements)

    def parse_class_def(self):
        """Parse a class definition"""
        class_tok = self.eat(TokenType.CLASS)
        name = self.eat(TokenType.IDENTIFIER).value

        base_class = None
        base_classes = None
        if self.match(TokenType.LPAREN):
            self.eat(TokenType.LPAREN)
            bases = []
            # Allow zero or more bases? We'll require at least one if parens present
            bases.append(self.eat(TokenType.IDENTIFIER).value)
            while self.match(TokenType.COMMA):
                self.eat(TokenType.COMMA)
                bases.append(self.eat(TokenType.IDENTIFIER).value)
            self.eat(TokenType.RPAREN)
            base_classes = bases
            base_class = bases[0] if bases else None

        self.eat(TokenType.COLON)
        body = self.parse_block()

        return self._with_pos(ClassDef(name, base_class, body, base_classes=base_classes), class_tok)

    def parse_if_statement(self):
        """Parse an if statement"""
        if_tok = self.eat(TokenType.IF)
        condition = self.parse_expression()
        self.eat(TokenType.COLON)
        then_branch = self.parse_block()

        else_branch = None
        if self.match(TokenType.ELSE):
            self.eat(TokenType.ELSE)
            self.eat(TokenType.COLON)
            else_branch = self.parse_block()

        return self._with_pos(IfStatement(condition, then_branch, else_branch), if_tok)

    def parse_for_loop(self):
        """Parse a for loop"""
        for_tok = self.eat(TokenType.FOR)
        var_name = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.IN)
        iterable = self.parse_expression()
        self.eat(TokenType.COLON)
        body = self.parse_block()

        return self._with_pos(ForLoop(var_name, iterable, body), for_tok)

    def parse_while_loop(self):
        """Parse a while loop"""
        while_tok = self.eat(TokenType.WHILE)
        condition = self.parse_expression()
        self.eat(TokenType.COLON)
        body = self.parse_block()

        return self._with_pos(WhileLoop(condition, body), while_tok)

    def parse_return_statement(self):
        """Parse a return statement"""
        ret_tok = self.eat(TokenType.RETURN)
        value = None

        if not self.match(TokenType.SEMICOLON, TokenType.RBRACE, TokenType.EOF):
            value = self.parse_expression()

        return self._with_pos(ReturnStatement(value), ret_tok)

    def parse_print_statement(self):
        """Parse a print statement"""
        pr_tok = self.eat(TokenType.PRINT)
        self.eat(TokenType.LPAREN)
        value = self.parse_expression()
        self.eat(TokenType.RPAREN)

        return self._with_pos(PrintStatement(value), pr_tok)

    def parse_assignment(self):
        """Parse an assignment target and value
        Supports: x = v, obj.attr = v, obj[index] = v, and chained obj.attr[index] = v
        """
        # Start with an identifier as assignment target base
        name_tok = self.eat(TokenType.IDENTIFIER)
        base_name = name_tok.value
        target_expr = self._with_pos(Variable(base_name), name_tok)

        # Parse chained attribute/subscript access on the target
        while self.match(TokenType.DOT) or self.match(TokenType.LBRACKET):
            if self.match(TokenType.DOT):
                self.eat(TokenType.DOT)
                attr_tok = self.eat(TokenType.IDENTIFIER)
                attr_name = attr_tok.value
                target_expr = self._with_pos(AttributeAccess(target_expr, attr_name), attr_tok)
            else:
                lb_tok = self.eat(TokenType.LBRACKET)
                index_expr = self.parse_expression()
                self.eat(TokenType.RBRACKET)
                target_expr = self._with_pos(SubscriptAccess(target_expr, index_expr), lb_tok)

        # Now parse assignment operator and value
        assign_tok = self.eat(TokenType.ASSIGN)
        value = self.parse_expression()

        # Build appropriate assignment node
        if isinstance(target_expr, Variable):
            return self._with_pos(Assignment(target_expr.name, value), name_tok)
        elif isinstance(target_expr, AttributeAccess):
            return self._with_pos(AttributeAssignment(target_expr.object_expr, target_expr.attribute_name, value), assign_tok)
        elif isinstance(target_expr, SubscriptAccess):
            return self._with_pos(SubscriptAssignment(target_expr.object_expr, target_expr.index_expr, value), assign_tok)
        else:
            raise SyntaxError("Invalid assignment target")

    def parse_expression_statement(self):
        """Parse an expression statement"""
        expr = self.parse_expression()
        return expr

    def parse_expression(self):
        """Parse an expression"""
        return self.parse_or_expression()

    def parse_or_expression(self):
        """Parse logical OR expression"""
        left = self.parse_and_expression()

        while self.match(TokenType.OR):
            tok = self.current_token
            self.advance()
            right = self.parse_and_expression()
            left = self._with_pos(BinaryOp('or', left, right), tok)

        return left

    def parse_and_expression(self):
        """Parse logical AND expression"""
        left = self.parse_comparison()

        while self.match(TokenType.AND):
            tok = self.current_token
            self.advance()
            right = self.parse_comparison()
            left = self._with_pos(BinaryOp('and', left, right), tok)

        return left

    def parse_comparison(self):
        """Parse comparison expression"""
        left = self.parse_additive()

        while self.match(TokenType.OPERATOR) or self.match(TokenType.IN):
            if self.match(TokenType.IN):
                tok_in = self.eat(TokenType.IN)
                right = self.parse_additive()
                left = self._with_pos(BinaryOp('in', left, right), tok_in)
            else:
                op_tok = self.eat(TokenType.OPERATOR)
                op = op_tok.value
                right = self.parse_additive()
                left = self._with_pos(BinaryOp(op, left, right), op_tok)

        return left

    def parse_additive(self):
        """Parse addition/subtraction"""
        left = self.parse_multiplicative()

        while self.match(TokenType.OPERATOR) and self.current_token.value in ['+', '-']:
            op_tok = self.eat(TokenType.OPERATOR)
            op = op_tok.value
            right = self.parse_multiplicative()
            left = self._with_pos(BinaryOp(op, left, right), op_tok)

        return left

    def parse_multiplicative(self):
        """Parse multiplication/division"""
        left = self.parse_unary()

        while self.match(TokenType.OPERATOR) and self.current_token.value in ['*', '/', '%']:
            op_tok = self.eat(TokenType.OPERATOR)
            op = op_tok.value
            right = self.parse_unary()
            left = self._with_pos(BinaryOp(op, left, right), op_tok)

        return left

    def parse_unary(self):
        """Parse unary expressions"""
        if self.match(TokenType.NOT):
            tok = self.current_token
            self.advance()
            operand = self.parse_unary()
            return self._with_pos(UnaryOp('not', operand), tok)
        elif self.match(TokenType.OPERATOR) and self.current_token.value == '-':
            tok = self.current_token
            self.advance()
            operand = self.parse_unary()
            return self._with_pos(UnaryOp('-', operand), tok)

        return self.parse_primary()

    def parse_primary(self):
        """Parse primary expressions"""
        if self.match(TokenType.NUMBER):
            tok = self.eat(TokenType.NUMBER)
            value = tok.value
            return self._with_pos(Number(float(value) if '.' in value else int(value)), tok)

        elif self.match(TokenType.STRING):
            tok = self.eat(TokenType.STRING)
            value = tok.value
            # Remove quotes
            return self._with_pos(String(value[1:-1]), tok)

        elif self.match(TokenType.TRUE):
            tok = self.eat(TokenType.TRUE)
            return self._with_pos(Boolean(True), tok)

        elif self.match(TokenType.FALSE):
            tok = self.eat(TokenType.FALSE)
            return self._with_pos(Boolean(False), tok)

        elif self.match(TokenType.NONE):
            tok = self.eat(TokenType.NONE)
            return self._with_pos(Variable('None'), tok)

        elif self.match(TokenType.VARIABLE):
            # Logical variable
            tok = self.eat(TokenType.VARIABLE)
            name = tok.value
            return self._with_pos(Variable(name), tok)

        elif self.match(TokenType.IDENTIFIER):
            name_tok = self.eat(TokenType.IDENTIFIER)
            name = name_tok.value

            if self.match(TokenType.LPAREN):
                # Function call
                self.eat(TokenType.LPAREN)
                args = self.parse_argument_list()
                self.eat(TokenType.RPAREN)
                expr = self._with_pos(FunctionCall(name, args), name_tok)

                # Check for chained access: . or [ ] after a function call result
                while self.match(TokenType.DOT) or self.match(TokenType.LBRACKET):
                    if self.match(TokenType.DOT):
                        self.eat(TokenType.DOT)
                        attr_tok = self.eat(TokenType.IDENTIFIER)
                        attr_name = attr_tok.value

                        if self.match(TokenType.LPAREN):
                            self.eat(TokenType.LPAREN)
                            args = self.parse_argument_list()
                            self.eat(TokenType.RPAREN)
                            expr = self._with_pos(MethodCall(expr, attr_name, args), attr_tok)
                        else:
                            expr = self._with_pos(AttributeAccess(expr, attr_name), attr_tok)
                    else:
                        # Subscription: expr[index]
                        lb_tok = self.eat(TokenType.LBRACKET)
                        index_expr = self.parse_expression()
                        self.eat(TokenType.RBRACKET)
                        expr = self._with_pos(SubscriptAccess(expr, index_expr), lb_tok)

                return expr
            elif self.match(TokenType.DOT) or self.match(TokenType.LBRACKET):
                # Attribute access or method call starting from a variable
                expr = self._with_pos(Variable(name), name_tok)

                while self.match(TokenType.DOT) or self.match(TokenType.LBRACKET):
                    if self.match(TokenType.DOT):
                        self.eat(TokenType.DOT)
                        attr_tok = self.eat(TokenType.IDENTIFIER)
                        attr_name = attr_tok.value

                        if self.match(TokenType.LPAREN):
                            # Method call
                            self.eat(TokenType.LPAREN)
                            args = self.parse_argument_list()
                            self.eat(TokenType.RPAREN)
                            expr = self._with_pos(MethodCall(expr, attr_name, args), attr_tok)
                        else:
                            # Attribute access
                            expr = self._with_pos(AttributeAccess(expr, attr_name), attr_tok)
                    else:
                        # Subscription: expr[index]
                        lb_tok = self.eat(TokenType.LBRACKET)
                        index_expr = self.parse_expression()
                        self.eat(TokenType.RBRACKET)
                        expr = self._with_pos(SubscriptAccess(expr, index_expr), lb_tok)

                return expr
            else:
                return self._with_pos(Variable(name), name_tok)

        elif self.match(TokenType.LBRACKET):
            return self.parse_list()

        elif self.match(TokenType.LBRACE):
            return self.parse_dict()

        elif self.match(TokenType.SELF):
            tok_self = self.current_token
            self.advance()
            expr = self._with_pos(SelfReference(), tok_self)

            # Allow chained access after self: . or [ ]
            while self.match(TokenType.DOT) or self.match(TokenType.LBRACKET):
                if self.match(TokenType.DOT):
                    self.eat(TokenType.DOT)
                    attr_tok = self.eat(TokenType.IDENTIFIER)
                    attr_name = attr_tok.value

                    if self.match(TokenType.LPAREN):
                        # Method call
                        self.eat(TokenType.LPAREN)
                        args = self.parse_argument_list()
                        self.eat(TokenType.RPAREN)
                        expr = self._with_pos(MethodCall(expr, attr_name, args), attr_tok)
                    else:
                        # Attribute access
                        expr = self._with_pos(AttributeAccess(expr, attr_name), attr_tok)
                else:
                    # Subscription: self[index]
                    lb_tok = self.eat(TokenType.LBRACKET)
                    index_expr = self.parse_expression()
                    self.eat(TokenType.RBRACKET)
                    expr = self._with_pos(SubscriptAccess(expr, index_expr), lb_tok)

            return expr

        elif self.match(TokenType.SUPER):
            self.eat(TokenType.SUPER)
            self.eat(TokenType.LPAREN)
            # Support both: super(method[, args]) and super().method(args)
            if self.match(TokenType.RPAREN):
                # super().method(args)
                self.eat(TokenType.RPAREN)
                self.eat(TokenType.DOT)
                method_name = self.eat(TokenType.IDENTIFIER).value
                self.eat(TokenType.LPAREN)
                args = self.parse_argument_list()
                self.eat(TokenType.RPAREN)
                return SuperCall(method_name, args)
            else:
                # Legacy form: super(method[, args])
                method_name = self.eat(TokenType.IDENTIFIER).value
                args = []
                if self.match(TokenType.COMMA):
                    self.eat(TokenType.COMMA)
                    args = self.parse_argument_list()
                self.eat(TokenType.RPAREN)
                return SuperCall(method_name, args)

        elif self.match(TokenType.LPAREN):
            self.eat(TokenType.LPAREN)
            expr = self.parse_expression()
            self.eat(TokenType.RPAREN)

            # Check for chained access: . or [ ] after a parenthesized expression
            while self.match(TokenType.DOT) or self.match(TokenType.LBRACKET):
                if self.match(TokenType.DOT):
                    self.eat(TokenType.DOT)
                    attr_tok = self.eat(TokenType.IDENTIFIER)
                    attr_name = attr_tok.value

                    if self.match(TokenType.LPAREN):
                        self.eat(TokenType.LPAREN)
                        args = self.parse_argument_list()
                        self.eat(TokenType.RPAREN)
                        expr = self._with_pos(MethodCall(expr, attr_name, args), attr_tok)
                    else:
                        expr = self._with_pos(AttributeAccess(expr, attr_name), attr_tok)
                else:
                    # Subscription: expr[index]
                    lb_tok = self.eat(TokenType.LBRACKET)
                    index_expr = self.parse_expression()
                    self.eat(TokenType.RBRACKET)
                    expr = self._with_pos(SubscriptAccess(expr, index_expr), lb_tok)

            return expr

        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

    def parse_argument_list(self):
        """Parse function arguments"""
        args = []

        if not self.match(TokenType.RPAREN):
            args.append(self.parse_expression())

            while self.match(TokenType.COMMA):
                self.eat(TokenType.COMMA)
                args.append(self.parse_expression())

        return args

    def parse_dotted_name(self):
        """Parse dotted module name like 'a.b.c'"""
        parts = [self.eat(TokenType.IDENTIFIER).value]
        while self.match(TokenType.DOT):
            self.eat(TokenType.DOT)
            parts.append(self.eat(TokenType.IDENTIFIER).value)
        return '.'.join(parts)

    def parse_import_statement(self):
        """Parse 'import module [as alias]'"""
        imp_tok = self.eat(TokenType.IMPORT)
        module_name = self.parse_dotted_name()
        alias = None
        if self.match(TokenType.AS):
            self.eat(TokenType.AS)
            alias = self.eat(TokenType.IDENTIFIER).value
        return self._with_pos(ImportStatement(module_name, alias), imp_tok)

    def parse_from_import_statement(self):
        """Parse 'from module import name[, name]*'"""
        from_tok = self.eat(TokenType.FROM)
        module_name = self.parse_dotted_name()
        self.eat(TokenType.IMPORT)
        names = [self.eat(TokenType.IDENTIFIER).value]
        while self.match(TokenType.COMMA):
            self.eat(TokenType.COMMA)
            names.append(self.eat(TokenType.IDENTIFIER).value)
        return self._with_pos(FromImportStatement(module_name, names), from_tok)

        return args

    def parse_list(self):
        """Parse a list literal"""
        lb_tok = self.eat(TokenType.LBRACKET)
        elements = []

        if not self.match(TokenType.RBRACKET):
            elements.append(self.parse_expression())

            while self.match(TokenType.COMMA):
                self.eat(TokenType.COMMA)
                elements.append(self.parse_expression())

        self.eat(TokenType.RBRACKET)
        return self._with_pos(List(elements), lb_tok)

    def parse_dict(self):
        """Parse a dictionary literal"""
        lb_tok = self.eat(TokenType.LBRACE)
        pairs = []

        if not self.match(TokenType.RBRACE):
            key = self.parse_expression()
            self.eat(TokenType.COLON)
            value = self.parse_expression()
            pairs.append((key, value))

            while self.match(TokenType.COMMA):
                self.eat(TokenType.COMMA)
                key = self.parse_expression()
                self.eat(TokenType.COLON)
                value = self.parse_expression()
                pairs.append((key, value))

        self.eat(TokenType.RBRACE)
        return self._with_pos(Dict(pairs), lb_tok)

    def parse_query(self):
        """Parse a logical query"""
        self.eat(TokenType.QUERY)
        goal = self.parse_logical_predicate()
        if self.current_token and self.current_token.type == TokenType.DOT:
            self.eat(TokenType.DOT)
        return LogicalQuery(goal)

    def parse_fact(self):
        """Parse a logical fact"""
        if self.match(TokenType.FACT):
            self.eat(TokenType.FACT)

        predicate = self.parse_logical_predicate()
        self.eat(TokenType.DOT)

        return LogicalFact(predicate)

    def parse_rule(self):
        """Parse a logical rule"""
        if self.match(TokenType.RULE):
            self.eat(TokenType.RULE)

        head = self.parse_logical_predicate()

        # Handle both :- and ←
        if self.match(TokenType.IMPLIES):
            self.eat(TokenType.IMPLIES)
        elif self.match(TokenType.ARROW):
            self.eat(TokenType.ARROW)
        else:
            raise SyntaxError(f"Expected :- or ← in rule, got {self.current_token}")

        body = self.parse_logical_body()

        # Handle optional dot at the end
        if self.current_token and self.current_token.type == TokenType.DOT:
            self.eat(TokenType.DOT)

        return LogicalRule(head, body)

    def parse_logical_predicate(self):
        """Parse a logical predicate"""
        name = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.LPAREN)
        args = self.parse_logical_arguments()
        self.eat(TokenType.RPAREN)

        return Predicate(name, args)

    def parse_logical_arguments(self):
        """Parse logical predicate arguments"""
        args = []

        if not self.match(TokenType.RPAREN):
            args.append(self.parse_logical_term())

            while self.match(TokenType.COMMA):
                self.eat(TokenType.COMMA)
                args.append(self.parse_logical_term())

        return args

    def parse_logical_term(self):
        """Parse a logical term"""
        if self.match(TokenType.VARIABLE):
            var_name = self.eat(TokenType.VARIABLE).value[1:]  # Remove ?
            return Term(var_name, is_variable=True)

        elif self.match(TokenType.STRING):
            value = self.eat(TokenType.STRING).value[1:-1]  # Remove quotes
            return Term(value, is_variable=False)

        elif self.match(TokenType.NUMBER):
            value = self.eat(TokenType.NUMBER).value
            return Term(value, is_variable=False)

        elif self.match(TokenType.IDENTIFIER):
            value = self.eat(TokenType.IDENTIFIER).value
            return Term(value, is_variable=False)

        else:
            raise SyntaxError(f"Unexpected token in logical term: {self.current_token}")

    def parse_logical_body(self):
        """Parse the body of a logical rule"""
        goals = [self.parse_logical_predicate()]

        while self.match(TokenType.COMMA):
            self.eat(TokenType.COMMA)
            goals.append(self.parse_logical_predicate())

        return goals

