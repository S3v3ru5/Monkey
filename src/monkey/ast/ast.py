"""Base classes for Syntax Tree nodes"""

from typing import List

class Node(object):
    node_type: str = "Node"
    pass

class Statement(Node):
    node_type: str = "Statement"
    pass

class Expression(Node):
    node_type: str = "Expression"
    pass

class Program(Node):
    node_type: str = "Program"
    def __init__(self):
        self.statements: List[Statement] = []

class LetStatement(Statement):
    node_type: str = "LetStatement"
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class ReturnStatement(Statement):
    node_type: str = "ReturnStatement"
    def __init__(self, expression) -> None:
        self.expression = expression

class ExpressionStatement(Statement):
    node_type: str = "ExpressionStatement"
    def __init__(self, expression = None) -> None:
        self.expression = expression

class Identifier(Expression):
    node_type: str = "Identifier"
    def __init__(self, name: str) -> None:
        self.name = name

class IntegerLiteral(Expression):
    node_type: str = "IntegerLiteral"
    def __init__(self, value: int) -> None:
        self.value = value

class Boolean(Expression):
    node_type: str = "Boolean"
    def __init__(self, value: bool) -> None:
        self.value: bool = value

class PrefixExpression(Expression):
    node_type: str = "PrefixExpression"
    def __init__(self, operator, expression) -> None:
        self.operator = operator
        self.right = expression

class InfixExpression(Expression):
    node_type: str = "InfixExpression"
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class BlockStatement(Statement):
    node_type: str = "BlockStatement"
    def __init__(self):
        self.statements = []

class IfExpression(Expression):
    node_type: str = "IfExpression"
    def __init__(self, condition, consequence, alternative = None) -> None:
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

class FunctionLiteral(Expression):
    node_type: str = "FunctionLiteral"
    def __init__(self, parameters, body):
        self.parameters = parameters
        self.body: BlockStatement = body

class CallExpression(Expression):
    node_type: str = "CallExpression"
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments