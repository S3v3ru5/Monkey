
from monkey.ast.parser import Parser
from monkey.lexer.lexer import Lexer

def debug_program(root):
    stmts = []
    for stmt in root.statements:
        stmts.append(debug_statement(stmt))
    return "\n".join(stmts) + "\n"

def debug_statement(stmt):
    if stmt is None:
        return "NoneStatement"
    if stmt.node_type == "LetStatement":
        res = "let "
        res += debug_expression(stmt.identifier)
        res += " = "
        res += debug_expression(stmt.expression)
    elif stmt.node_type == "ReturnStatement":
        res = "return "
        res += debug_expression(stmt.expression)
    elif stmt.node_type == "ExpressionStatement":
        res = debug_expression(stmt.expression)
    else:
        res = "Unknown Statement"
    res += ";"
    return res

def debug_block_statement(start):
    return debug_program(start)

def debug_expression(expression):
    if expression is None:
        return "NoneExpression"
    if expression.node_type == "Identifier":
        return str(expression.name)
    elif expression.node_type == "IntegerLiteral":
        return str(expression.value)
    elif expression.node_type == "Boolean":
        return str(expression.value)
    elif expression.node_type == "PrefixExpression":
        return "(" + expression.operator + debug_expression(expression.right) + ")"
    elif expression.node_type == "InfixExpression":
        return "(" + debug_expression(expression.left) + " " + expression.operator + " " + debug_expression(expression.right) + ")"
    elif expression.node_type == "IfExpression":
        res = "if ("
        res += debug_expression(expression.condition)
        res += ") {\n"
        res += debug_block_statement(expression.consequence)
        res += "}\n"
        if expression.alternative is None:
            return res
        res += "else {\n"
        res += debug_block_statement(expression.alternative)
        res += "}"
        return res
    elif expression.node_type == "FunctionLiteral":
        res = "fn ("
        res += ", ".join(debug_expression(i) for i in expression.parameters)
        res += ") {\n"
        res += debug_block_statement(expression.body)
        res += "}"
        return res
    elif expression.node_type == "CallExpression":
        res = debug_expression(expression.function)
        res += "("
        res += ", ".join(debug_expression(arg) for arg in expression.arguments)
        res += ")"
        return res
    return "expression"


if __name__ == "__main__":
    while True:
        inp = input(">> ")
        src = inp
        while inp != "":
            inp = input(">> ")
            src += inp
        l = Lexer(src)
        p = Parser(l)
        root = p.parse()
        print(debug_program(root))
        print("\nerrors :: ")
        print("\n".join(p.errors))

