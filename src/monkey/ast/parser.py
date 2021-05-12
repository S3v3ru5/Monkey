"""Parser for Monkey language"""

import typing
from types import SimpleNamespace

from monkey.exceptions import SyntaxError
from monkey.ast import ast
from monkey.lexer.token_types import token_types as TOKEN_TYPES

PRECEDENCE_ORDERS = {
    "LOWEST": 1,
    "EQUALS": 2,
    "LESSGREATER": 3,
    "SUM": 4,
    "PRODUCT": 5,
    "PREFIX": 6,
    "CALL": 7,
    "INDEX": 8,
}

PRECEDENCE_ORDERS = SimpleNamespace(**PRECEDENCE_ORDERS)

PRECEDENCES = {
    TOKEN_TYPES.EQUAL:          PRECEDENCE_ORDERS.EQUALS,
    TOKEN_TYPES.NOT_EQUAL:      PRECEDENCE_ORDERS.EQUALS,
    TOKEN_TYPES.LESSTHAN:       PRECEDENCE_ORDERS.LESSGREATER,
    TOKEN_TYPES.GREATERTHAN:    PRECEDENCE_ORDERS.LESSGREATER,
    TOKEN_TYPES.PLUS:           PRECEDENCE_ORDERS.SUM,
    TOKEN_TYPES.MINUS:          PRECEDENCE_ORDERS.SUM,
    TOKEN_TYPES.MUL:            PRECEDENCE_ORDERS.PRODUCT,
    TOKEN_TYPES.DIV:            PRECEDENCE_ORDERS.PRODUCT,
    TOKEN_TYPES.LPAREN:         PRECEDENCE_ORDERS.CALL,
    TOKEN_TYPES.LBRACKET:       PRECEDENCE_ORDERS.INDEX,
}

class Parser:
    """Main Parser Class for Monkey language"""

    def __init__(self, lexer) -> None:
        self.lexer = lexer
        
        self.prev_token = None
        self.current_token = None
        self.peek_token = None

        self.prefix_funcs = dict()
        self.infix_funcs = dict()
        self._register_prefixes()
        self._register_infixes()

        self.errors = []
    
        self._advance()
        self._advance()

    def _advance(self):
        """increment the parser cursor"""
        self.prev_token = self.current_token
        self.current_token = self.peek_token
        self.peek_token = self.lexer.get_next_token()
    
    def _iscurrenttoken(self, token_type):
        return self.current_token.type == token_type

    def _ispeektoken(self, token_type):
        return self.peek_token.type == token_type

    def _peek_precedence(self):
        return PRECEDENCES.get(self.peek_token.type, PRECEDENCE_ORDERS.LOWEST)

    def _current_precedence(self):
        return PRECEDENCES.get(self.current_token.type, PRECEDENCE_ORDERS.LOWEST)

    def _error(self, msg = None):
        """method to call to raise an error."""
        if msg is None:
            msg = f"invalid syntax at or near {self.current_token.value}"
            msg += f"\n\nSyntaxError: Invalid Syntax"
        raise SyntaxError(msg)

    def _get_error_msg(self, expected, got, previous_token = None):
        if previous_token is None:
            msg = f"expected a {expected}, instead got a {got}"
        else:
            msg = f"expected {expected} after {previous_token.value}, "
            msg += f"instead got {got}"
        msg += "\n\nSyntaxError: Invalid Syntax"
        return msg

    def _eat(self, token_type):
        """verify current token type.
        
        if current token is of the expected type then increment
        the parser cursor and get next token else raise Error. 
        """
        if self.current_token.type != token_type:
            msg = self._get_error_msg(token_type,
                    self.current_token.type,
                    self.prev_token
                )
            self._error(msg)
        else:
            self._advance()

    def p_let_statement(self) -> ast.LetStatement:
        """parse a let statement.
        
        let <identifier> = <expression>;

        Returns:
            reference to root node of let subtree.
        """
        self._eat(TOKEN_TYPES.LET)
        var_name = self.current_token.value
        self._eat(TOKEN_TYPES.IDENTIFIER)
        self._eat(TOKEN_TYPES.ASSIGN)

        expression = self.p_expression(PRECEDENCE_ORDERS.LOWEST)
        self._advance()

        identifier = ast.Identifier(var_name)
        let_stmt = ast.LetStatement(identifier, expression)
        
        if self._iscurrenttoken(TOKEN_TYPES.SEMICOLON):
            self._eat(TOKEN_TYPES.SEMICOLON)

        return let_stmt
    
    def p_return_statement(self) -> ast.ReturnStatement:
        """parse a return statement.

        return <expression>;
        """
        self._eat(TOKEN_TYPES.RETURN)
        expression = self.p_expression(PRECEDENCE_ORDERS.LOWEST)
        self._advance()

        if self._iscurrenttoken(TOKEN_TYPES.SEMICOLON):
            self._eat(TOKEN_TYPES.SEMICOLON)

        return ast.ReturnStatement(expression)

    def p_expression_statement(self) -> ast.ExpressionStatement:
        """Statement Wrapper for expressions"""
        expr = self.p_expression(PRECEDENCE_ORDERS.LOWEST)
        self._advance()
        stmt = ast.ExpressionStatement(expr)
        if self._iscurrenttoken(TOKEN_TYPES.SEMICOLON):
            self._eat(TOKEN_TYPES.SEMICOLON)
        return stmt

    def p_statement(self) -> ast.Statement:
        """parse a statement.

        let statements, return statements, expression statement.
        """
        if self._iscurrenttoken(TOKEN_TYPES.LET):
            return self.p_let_statement()
        elif self._iscurrenttoken(TOKEN_TYPES.RETURN):
            return self.p_return_statement()
        else:
            return self.p_expression_statement()

    def _register_prefix(self, token_type, func):
        self.prefix_funcs[token_type] = func

    def _register_infix(self, token_type, func):
        self.infix_funcs[token_type] = func

    def _register_prefixes(self) -> None:
        self._register_prefix(TOKEN_TYPES.IDENTIFIER, self.p_identifier)
        self._register_prefix(TOKEN_TYPES.INTEGER, self.p_integer_literal)
        self._register_prefix(TOKEN_TYPES.STRING, self.p_string_literal)
        self._register_prefix(TOKEN_TYPES.TRUE, self.p_boolean)
        self._register_prefix(TOKEN_TYPES.FALSE, self.p_boolean)
        self._register_prefix(TOKEN_TYPES.NOT, self.p_prefix_expression)
        self._register_prefix(TOKEN_TYPES.MINUS, self.p_prefix_expression)
        self._register_prefix(TOKEN_TYPES.LPAREN, self.p_grouped_expression)
        self._register_prefix(TOKEN_TYPES.LBRACKET, self.p_array_literal)
        self._register_prefix(TOKEN_TYPES.IF, self.p_if_expression)
        self._register_prefix(TOKEN_TYPES.FUNCTION, self.p_function_literal)

    def _register_infixes(self) -> None:
        self._register_infix(TOKEN_TYPES.PLUS, self.p_infix_expression)
        self._register_infix(TOKEN_TYPES.MINUS, self.p_infix_expression)
        self._register_infix(TOKEN_TYPES.MUL, self.p_infix_expression)
        self._register_infix(TOKEN_TYPES.DIV, self.p_infix_expression)
        self._register_infix(TOKEN_TYPES.EQUAL, self.p_infix_expression)
        self._register_infix(TOKEN_TYPES.NOT_EQUAL, self.p_infix_expression)
        self._register_infix(TOKEN_TYPES.LESSTHAN, self.p_infix_expression)
        self._register_infix(TOKEN_TYPES.GREATERTHAN, self.p_infix_expression)
        self._register_infix(TOKEN_TYPES.LPAREN, self.p_call_expression)
        self._register_infix(TOKEN_TYPES.LBRACKET, self.p_index_expression)

    def p_identifier(self) -> ast.Identifier:
        return ast.Identifier(self.current_token.value)

    def p_integer_literal(self) -> ast.IntegerLiteral:
        return ast.IntegerLiteral(self.current_token.value)
    
    def p_string_literal(self) -> ast.StringLiteral:
        return ast.StringLiteral(self.current_token.value)

    def p_boolean(self) -> ast.Boolean:
        if self._iscurrenttoken(TOKEN_TYPES.TRUE):
            value = True
        elif self._iscurrenttoken(TOKEN_TYPES.FALSE):
            value = False
        else:
            self._error()
            value = None
        return ast.Boolean(value)

    def p_array_literal(self) -> ast.ArrayLiteral:
        """parse arrays.

        arrays :: "[" <expression>, <expression>, ..."]"
        """
        elements = self.p_expression_list(TOKEN_TYPES.RBRACKET)
        return ast.ArrayLiteral(elements)
    
    def p_prefix_expression(self) -> ast.PrefixExpression:
        """parse prefix expressions(unary).

        prefix operators :: "!", "-"
        PrefixExpression :: <prefix_operator> <expression>
        """
        operator = self.current_token.value
        self._advance()
        right = self.p_expression(PRECEDENCE_ORDERS.PREFIX)
        return ast.PrefixExpression(operator, right)

    def p_infix_expression(self, left: ast.Expression) -> ast.InfixExpression:
        """parse infix expressions(binary).

        infix operators :: "+", "-", "*", "/", "==", "<", ">"
        InfixExpression :: <expression> <infix_operator> <expression>
        """
        operator = self.current_token.value
        precedence = self._current_precedence()
        self._advance()
        right = self.p_expression(precedence)
        return ast.InfixExpression(left, operator, right)

    def p_grouped_expression(self) -> ast.Expression:
        """parse a grouped(paranthesised) expression.

        ==> "(" <expression> ")"
        """
        self._advance()

        exp = self.p_expression(PRECEDENCE_ORDERS.LOWEST)

        if not self._ispeektoken(TOKEN_TYPES.RPAREN):
            msg = self._get_error_msg(TOKEN_TYPES.RPAREN,
                        self.peek_token.type,
                        self.current_token
                    )
            self._error(msg)
        self._advance()
        return exp

    def p_if_expression(self) -> ast.IfExpression:
        """parse an if expression.

        condition :: "(" <expression> ")"
        BlockStatement :: "{" <statement>* "}" 
        consequence :: BlockStatement
        alternative :: BlockStatement
        IfExpression :: if <condition> <consequence>
                        | if <condition> <consequence> else <alternative>
        """
        self._advance()
        if not self._iscurrenttoken(TOKEN_TYPES.LPAREN):
            msg = self._get_error_msg(TOKEN_TYPES.LPAREN,
                        self.current_token.type,
                        self.prev_token
                    )
            self._error(msg)
        self._advance()
        condition = self.p_expression(PRECEDENCE_ORDERS.LOWEST)

        if not self._ispeektoken(TOKEN_TYPES.RPAREN):
            msg = self._get_error_msg(TOKEN_TYPES.RPAREN,
                        self.peek_token.type,
                        self.current_token
                    )
            self._error(msg)
        self._advance()
        if not self._ispeektoken(TOKEN_TYPES.LBRACE):
            msg = self._get_error_msg(TOKEN_TYPES.LBRACE,
                        self.peek_token.type,
                        self.current_token.value
                    )
            self._error(msg)
        self._advance()

        consequence = self.p_block_statement()

        if self._ispeektoken(TOKEN_TYPES.ELSE):
            self._advance()
            if not self._ispeektoken(TOKEN_TYPES.LBRACE):
                msg = self._get_error_msg(TOKEN_TYPES.LBRACE,
                            self.peek_token.type,
                            self.current_token.value
                        )
                self._error(msg)
            self._advance()
            alternative = self.p_block_statement()
        else:
            alternative = None
        
        return ast.IfExpression(condition, consequence, alternative)

    def p_index_expression(self, left) -> ast.IndexExpression:
        """parse an index expression.

        IndexExpression :: <expression> "[" <expression> "]"
        """
        self._advance()
        index = self.p_expression(PRECEDENCE_ORDERS.LOWEST)
        self._advance()
        if not self._iscurrenttoken(TOKEN_TYPES.RBRACKET):
            msg = self._get_error_msg(TOKEN_TYPES.RBRACKET,
                        self.current_token.type,
                        self.prev_token
                    )
            self._error(msg)
        return ast.IndexExpression(left, index)

    def p_expression_list(self, end_marker):
        """parse comma separated expressions until end_marker."""
        args = []
        self._advance()
        if self._iscurrenttoken(end_marker):
            return args
        expression = self.p_expression(PRECEDENCE_ORDERS.LOWEST)
        self._advance()
        args.append(expression)
        while self._iscurrenttoken(TOKEN_TYPES.COMMA):
            self._eat(TOKEN_TYPES.COMMA)
            expression = self.p_expression(PRECEDENCE_ORDERS.LOWEST)
            self._advance()
            args.append(expression)
        if not self._iscurrenttoken(end_marker):
            msg = self._get_error_msg(end_marker,
                        self.current_token.type,
                        self.prev_token
                    )
            self._error(msg)
        return args

    def p_call_arguments(self):
        return self.p_expression_list(TOKEN_TYPES.RPAREN)

    def p_call_expression(self, function) -> ast.CallExpression:
        """parse a call expression(function calling).
        
        arguments :: <expression> ("," <expression>)*
        CallExpression :: <expression> "(" <arguments> ")"
        """
        arguments = self.p_call_arguments()
        return ast.CallExpression(function, arguments)

    def p_function_parameters(self):
        """parse function parameters."""
        parameters = []
        self._advance()
        if self._iscurrenttoken(TOKEN_TYPES.RPAREN):
            self._eat(TOKEN_TYPES.RPAREN)
            return parameters
        
        identifier = ast.Identifier(self.current_token.value)
        self._eat(TOKEN_TYPES.IDENTIFIER)
        
        parameters.append(identifier)
        while self._iscurrenttoken(TOKEN_TYPES.COMMA):
            self._eat(TOKEN_TYPES.COMMA)
            identifier = ast.Identifier(self.current_token.value)
            self._eat(TOKEN_TYPES.IDENTIFIER)
            parameters.append(identifier)
        self._eat(TOKEN_TYPES.RPAREN)

        return parameters

    def p_function_literal(self) -> ast.FunctionLiteral:
        """parse a function literal.

        parameter :: <identifier>
        parameters :: "(" <parameter> ",", <parameter> "," ... ")"
        FunctionLiteral :: fn <parameters> <BlockStatement> 
        """
        self._advance()
        if not self._iscurrenttoken(TOKEN_TYPES.LPAREN):
            msg = self._get_error_msg(TOKEN_TYPES.LPAREN,
                        self.current_token.type,
                        self.prev_token
                    )
            self._error(msg)
        
        parameters = self.p_function_parameters()
        if not self._iscurrenttoken(TOKEN_TYPES.LBRACE):
            msg = self._get_error_msg(TOKEN_TYPES.LBRACE,
                        self.current_token.type,
                        self.prev_token
                    )
            self._error(msg)

        body = self.p_block_statement()

        return ast.FunctionLiteral(parameters, body)

    def p_block_statement(self) -> ast.BlockStatement:
        """parse a block of statements.

        BlockStatement :: "{" <statement>* "}"
        """
        block = ast.BlockStatement()

        self._advance()

        while not self._iscurrenttoken(TOKEN_TYPES.RBRACE):
            stmt = self.p_statement()
            block.statements.append(stmt)
        return block

    def p_expression(self, precedence) -> ast.Expression:
        """parse an expression."""
        prefix_func = self.prefix_funcs.get(self.current_token.type)
        if prefix_func is None:
            self._error()
            return None
        left_exp = prefix_func()
       
        while not self._ispeektoken(TOKEN_TYPES.SEMICOLON) and precedence < self._peek_precedence():
            infix_func = self.infix_funcs.get(self.peek_token.type)
            if infix_func is None:
                self._error()
                return left_exp
            self._advance()
            left_exp = infix_func(left_exp)

        return left_exp

    def parse(self) -> ast.Program:
        """Main parse method"""
        program = ast.Program()
        while not self._iscurrenttoken(TOKEN_TYPES.EOF):
            stmt = self.p_statement()
            if stmt is None:
                self._error()
            program.statements.append(stmt)
        return program
    

if __name__ == "__main__":
    pass
