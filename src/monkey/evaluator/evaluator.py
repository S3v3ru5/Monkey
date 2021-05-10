"""Evaluator of Monkey Language"""

from typing import List
import operator as py_operator

from monkey.ast import ast
from monkey.evaluator import mobjects
from monkey.evaluator.environment import Environment
from monkey.evaluator.builtins import builtins

TRUE = mobjects.Boolean(True)
FALSE = mobjects.Boolean(False)
NULL = mobjects.Null()

def construct_boolean(value: bool) -> mobjects.Boolean:
    return TRUE if value else FALSE

def m_type(value_obj: mobjects.Object) -> str:
    """return type of the value_obj."""
    return value_obj.type()

def m_is_type(value_obj: mobjects.Object, obj_type: str) -> bool:
    """check if value_obj is of given type"""
    return m_type(value_obj) == obj_type

def m_error(msg) -> mobjects.Error:
    """create an error in Monkey"""
    return mobjects.Error(msg)

def m_is_error(obj: mobjects.Object) -> bool:
    return m_is_type(obj, mobjects.ERROR_OBJ)

def m_is_true(value_obj: mobjects.Object) -> bool:
    """determine whether an value/object evaluates to true.

    Check whether the given value is considered true or not.
    Integer values are considered true for all values other than zero.
    Null values are considered false.

    Args:
        value_obj: object to check.
    Returns:
        True if value_obj is considered "true" in Monkey else False.
    """
    if m_is_type(value_obj, mobjects.BOOLEAN_OBJ):
        return value_obj.value
    elif m_is_type(value_obj, mobjects.NULL_OBJ):
        return False
    elif m_is_type(value_obj, mobjects.INTEGER_OBJ):
        return value_obj.value != 0
    return True

def m_eval_identifier(node: ast.Identifier, env: Environment) -> mobjects.Object:
    """evaluate a identifier."""
    value = env.get(node.name)
    if value is not None:
        return value
    value = builtins.get(node.name)
    if value is not None:
        return value
    return m_error(f"name '{node.name}' is not defined")

def m_eval_not_operator(right: mobjects.Object) -> mobjects.Boolean:
    """evaluate boolean not operator
    
    Args:
        right: value to apply on.
    Returns:
        boolean value representing the result
    
    examples:
        "!true" -> Boolean(False)
        "!false" -> Boolean(True) 
    """
    if m_is_true(right):
        return FALSE
    return TRUE

def m_eval_prefix_sub_operator(right: mobjects.Object) -> mobjects.Integer:
    """evaluate prefix sub(minus) operator.
    
    Args:
        right: right side of prefix expression
    Returns:
        returns NULL if right is not of type Integer else
        returns new Integer object with value of -1*right.value.
    """
    if not m_is_type(right, mobjects.INTEGER_OBJ):
        return m_error(f"unsupported operand type for -: '{right.type()}'")
    return mobjects.Integer(-right.value)

def m_eval_prefix_expression(operator: str, right: mobjects.Object) -> mobjects.Object:
    """evaluate prefix(unary) expression.

    Args:
        operator: "-" or "!"
        right: expression to apply operator to.
    Returns:
        resultant value.
    """
    if operator == "!":
        return m_eval_not_operator(right)
    elif operator == "-":
        return m_eval_prefix_sub_operator(right)
    return m_error(f"unknown prefix operator: {operator}")

def m_eval_infix_integer_expression(
        left: mobjects.Object, operator: str, 
        right: mobjects.Object) -> mobjects.Object:
    """Evaluate infix(binary) integer expresssion."""
    func = {
        "+": py_operator.add,
        "-": py_operator.sub,
        "*": py_operator.mul,
        "/": py_operator.floordiv,
    }.get(operator)
    if func is not None:
        result = func(left.value, right.value)
        return mobjects.Integer(value = result)
    func = {
        "<": py_operator.lt,
        ">": py_operator.gt,
        "==": py_operator.eq,
        "!=": py_operator.ne,
    }.get(operator)
    if func is not None:
        return construct_boolean(func(left.value, right.value))
    return m_error(f"unknown infix operator {operator}: {left} {operator} {right}")

def m_eval_infix_string_expression(
        left: mobjects.String, operator: str,
        right: mobjects.String) -> mobjects.Object:
    """Evaluate string operators
    
    Args:
        left: lhs of the expression
        operator: "+", "==" or "!="
        right: rhs of the expression
    Returns:
        returns error if given operator is not one of the
        above mentioned otherwise returns the evaluated result. 
    """
    if operator == "+":
        return mobjects.String(left.value + right.value)
    elif operator == "==":
        return construct_boolean(left.value == right.value)
    elif operator == "!=":
        return construct_boolean(left.value != right.value)
    return m_error(f"unsupported operand type for {operator}: 'STRING' and 'STRING'")

def m_eval_infix_expression(
        left: mobjects.Object, operator: str, 
        right: mobjects.Object) -> mobjects.Object:
    """evaluate infix(binary) expression.

    Args:
        left: left side(lhs) of the expression.
        operator: one of "+", "-", "*", "/", "==", "<", ">", "!="
        right: right side(rhs) of the expression.
    Returns:
        return NULL if given operator is not binary operator.
    """
    if m_is_type(left, mobjects.INTEGER_OBJ) and m_is_type(right, mobjects.INTEGER_OBJ):
        return m_eval_infix_integer_expression(left, operator, right)
    elif m_is_type(left, mobjects.STRING_OBJ) and m_is_type(right, mobjects.STRING_OBJ):
        return m_eval_infix_string_expression(left, operator, right)
    elif operator == "==":
        return construct_boolean(left == right)
    elif operator == "!=":
        return construct_boolean(left != right)
    return m_error(f"unsupported operand type for {operator}: '{left.type()}' and '{right.type()}'")

def m_eval_if_expression(node: ast.IfExpression, env: Environment) -> mobjects.Object:
    """evaluate if expression.

    evaluate "if" block if condition is "true" and "else" block
    otherwise. if condition is "false" and no else is present then
    "NULL" is returned.result of the last statement is returned 
    whichever block is evaluated.

    Args: 
        node: root node of "if" expression in ast.
    Returns:
        result of last statement of whichever block is executed.
    """
    condition = m_eval(node.condition, env)
    if m_is_error(condition):
        return condition

    if m_is_true(condition):
        return m_eval(node.consequence, env)
    if node.alternative is not None:
        return m_eval(node.alternative, env)
    return NULL

def m_eval_array_index(left: mobjects.Array, index: mobjects.Integer) -> mobjects.Object:
    index = index.value
    if index < 0:
        return m_error("negative indexes are not supported")
    if not index < len(left.elements):
        return m_error(f"array index({index}) out of range")
    return left.elements[index]

def m_eval_index_expression(left: mobjects.Object, index: mobjects.Object) -> mobjects.Object:
    """evaluate index expression.

    Args:
        left: Object to access from.
        index: index of the element to acess.
    Returns:
        value at index if index is in range of array len.
        returns error object if index is out of bounds or 
        index is negative. 
    """
    if m_is_type(left, mobjects.ARRAY_OBJ) and m_is_type(index, mobjects.INTEGER_OBJ):
        return m_eval_array_index(left, index)
    return m_error(f"{left.type()} is not subscriptable")

def m_eval_call_expression(
            function: mobjects.Object,
            args: List[mobjects.Object]) -> mobjects.Object:
    """Evaluate a call expression(function call).

    Args:
        function: function to call.
        args: arguments to pass to given function.
    Returns:
        returns the result of function call.
    """
    if m_is_type(function, mobjects.BUILTIN_OBJ):
        return function.function(*args)
    if not m_is_type(function, mobjects.FUNCTION_OBJ):
        return m_error(f"{function.type()} is not callable")
    if len(function.parameters) != len(args):
        msg = f"function expected {len(function.parameters)} arguments but"
        msg += f" {len(args)} were given"
        return m_error(msg)
    extended_env = Environment(outer=function.env)
    for ind, parameter in enumerate(function.parameters):
        extended_env.set(parameter.name, args[ind])
    result = m_eval(function.body, extended_env)
    if m_is_type(result, mobjects.RETURN_VALUE_OBJ):
        return result.value
    return result

def m_eval_expressions(
            expressions: List[ast.Expression],
             env: Environment) -> List[mobjects.Object]:
    """evaluate list of expressions.
    
    Args:
        expressions: list of expressions to evaluate.
        env: current environment to evaluate expressions in.
    Returns:
        result: list of result objects corresponding to each expression
            in given list.
        error: None if all expressions are evaluated without any error else
            corresponding error.
    """
    result = []
    for expr in expressions:
        value = m_eval(expr, env)
        if m_is_error(value):
            return result, value
        result.append(value)
    return result, None

def m_eval_statements(stmts: List[ast.Statement], env: Environment) -> mobjects.Object:
    """evaluate list of statements.

    linear evaluation of the statements stops at the
    first "return" statement if there is one.
    value of "return" statement is returned when a 
    "return" statement is evaluated.

    Args:
        stmts: List of statements.
    Returns:
        result of evaluating last statement.
    """
    result = NULL
    for stmt in stmts:
        result = m_eval(stmt, env)
        if m_is_type(result, mobjects.RETURN_VALUE_OBJ):
            return result.value
    return result

def m_eval_block_statement(block: ast.BlockStatement, env: Environment) -> mobjects.Object:
    """evaluate block of statements.
    
    Args:
        block: object of type ast.BlockStatement representing block of 
            statements in syntax tree.
    Returns:
        result of last statement evaluated.
    """
    for stmt in block.statements:
        result = m_eval(stmt, env)
        if result is not None:
            if (m_is_type(result, mobjects.RETURN_VALUE_OBJ)
                or m_is_type(result, mobjects.ERROR_OBJ)):
                return result
    return result

def m_eval_program(program: ast.Program, env: Environment) -> mobjects.Object:
    """evaluate Program node."""
    result = NULL
    for stmt in program.statements:
        result = m_eval(stmt, env)
        if m_is_type(result, mobjects.RETURN_VALUE_OBJ):
            return result.value
        elif m_is_type(result, mobjects.ERROR_OBJ):
            return result
    return result

def m_eval(node: ast.Node, env: Environment) -> mobjects.Object:
    """Monkey evaluator function.

    Args:
        node: present node in syntax tree to evaluate.
    
    Returns:
        An instance of mobjects.Object is returned
        representing the result of evaluating given node.
    """
    if isinstance(node, ast.Program):
        return m_eval_program(node, env)
    elif isinstance(node, ast.LetStatement):
        value = m_eval(node.expression, env)
        if m_is_error(value):
            return value
        name = node.identifier.name
        env.set(name, value)
        return NULL
    elif isinstance(node, ast.ReturnStatement):
        value = m_eval(node.expression, env)
        if m_is_error(value):
            return value
        return mobjects.ReturnValue(value = value)
    elif isinstance(node, ast.ExpressionStatement):
        return m_eval(node.expression, env)
    elif isinstance(node, ast.BlockStatement):
        return m_eval_block_statement(node, env)
    elif isinstance(node, ast.PrefixExpression):
        right = m_eval(node.right, env)
        if m_is_error(right):
            return right
        return m_eval_prefix_expression(node.operator, right)
    elif isinstance(node, ast.InfixExpression):
        left = m_eval(node.left, env)
        if m_is_error(left):
            return left
        right = m_eval(node.right, env)
        if m_is_error(right):
            return right
        return m_eval_infix_expression(left, node.operator, right)
    elif isinstance(node, ast.IfExpression):
        return m_eval_if_expression(node, env)
    elif isinstance(node, ast.IndexExpression):
        left = m_eval(node.left, env)
        if m_is_error(left):
            return left
        index = m_eval(node.index, env)
        if m_is_error(index):
            return index
        return m_eval_index_expression(left, index)
    elif isinstance(node, ast.CallExpression):
        function = m_eval(node.function, env)
        if m_is_error(function):
            return function
        args, error = m_eval_expressions(node.arguments, env)
        if error is not None:
            return error
        return m_eval_call_expression(function, args)
    elif isinstance(node, ast.FunctionLiteral):
        parameters = node.parameters
        body = node.body
        return mobjects.Function(parameters, body, env)
    elif isinstance(node, ast.ArrayLiteral):
        elements, error = m_eval_expressions(node.elements, env)
        if error is not None:
            return error
        return mobjects.Array(elements)
    elif isinstance(node, ast.Identifier):
        return m_eval_identifier(node, env)
    elif isinstance(node, ast.IntegerLiteral):
        return mobjects.Integer(node.value)
    elif isinstance(node, ast.Boolean):
        return construct_boolean(node.value)
    elif isinstance(node, ast.StringLiteral):
        return mobjects.String(value=node.value)
    return NULL
