
import pytest

from monkey.lexer.lexer import Lexer
from monkey.ast.parser import Parser
from monkey.evaluator import mobjects
from monkey.evaluator.environment import Environment
from monkey.evaluator.evaluator import m_eval


def run_eval(src):
    l = Lexer(src)
    p = Parser(l)
    program_ast = p.parse() 
    return m_eval(program_ast, Environment())

def assert_integer(integer_obj: mobjects.Object, target):
    assert isinstance(integer_obj, mobjects.Integer)
    assert integer_obj.value == target

def assert_boolean(boolean_obj: mobjects.Object, target):
    assert isinstance(boolean_obj, mobjects.Boolean)
    assert boolean_obj.value == target

def assert_string(string_obj: mobjects.Object, target):
    assert isinstance(string_obj, mobjects.String)
    assert string_obj.value == target

def assert_null(null_obj: mobjects.Object):
    assert isinstance(null_obj, mobjects.Null)

def test_integer_eval():
    test_cases = [
        # Integer Literals
        ("1", 1),
        ("190", 190),
        ("190_12", 19012),
        ("9_123", 9123),
        # Prefix SUB Operator
        ("-100", -100),
        ("0", 0),
        ("--123", 123),
        # Infix Arthimetic Expressions
        ("1 + 1 + 1", 3),
        ("1 + 2 * 3", 7),
        ("5 / 2 * 2", 4),
        ("5 / (2 * 2)", 1),
        ("1 + 2 / 2", 2),
        ("(1 + 1) * 2", 4),
        ("1 + 2 - 3 * 4 / 5", 1),
        ("(1 + 2) - ((3 * 4) / 5)", 1),
    ]
    for src, target in test_cases:
        result = run_eval(src)
        assert_integer(result, target)

def test_boolean_eval():
    test_cases = [
        # Boolean Literals
        ("true", True),
        ("false", False),
        # Infix Boolean Expressions
        ("1 == 1", True),
        ("1 != 1", False),
        ("1 < 1", False),
        ("1 > 1", False),
        ("2 > 1", True),
        ("0 < 1", True),
        ("0 < 1 == 1 < 2", True),
        ("true == true", True),
        ("true != false", True),
    ]
    for src, target in test_cases:
        result = run_eval(src)
        assert_boolean(result, target)

def test_not_operator():
    test_cases = [
        ("!true", False),
        ("!false", True),
        ("!0", True),
        ("!1", False),
        ("!!true", True)
    ]
    for src, target in test_cases:
        result = run_eval(src)
        assert_boolean(result, target)

def test_if_expression():
    test_cases = [
        ("if (true) { 1; }", 1),
        ("if (1) { 1; }", 1),
        ("if (!false) { 1; }", 1),
        ("if (false) {1;}", None),
        ("if (1 == 1) {1;}", 1),
        ("if (1 < 2) {1;} else {2;};", 1),
        ("if (1 > 2) {1;} else {2;};", 2),
        ("""
        if (true) {
            if (true) {
                return 2;
            }

            return 1;
        }
        """, 2),
    ]
    for src, target in test_cases:
        result = run_eval(src)
        if target is None:
            assert_null(result)
        else:
            assert_integer(result, target)

def test_return_statement():
    test_cases = [
        ("return 1;", 1),
        ("1; return 2; return 3;", 2),
        ("1; return 2*3; 4;", 2*3),
    ]
    for src, target in test_cases:
        result = run_eval(src)
        assert_integer(result, target)

def test_errors():
    test_cases = [
        ("1 + true", "unsupported operand type for +: 'INTEGER' and 'BOOLEAN'"),
        ("false + true", "unsupported operand type for +: 'BOOLEAN' and 'BOOLEAN'"),
        ("false * true", "unsupported operand type for *: 'BOOLEAN' and 'BOOLEAN'"),
        ("-true", "unsupported operand type for -: 'BOOLEAN'"),
        ("-false; 1", "unsupported operand type for -: 'BOOLEAN'"),
        ("a;", "name 'a' is not defined"),
    ]
    for src, target in test_cases:
        result = run_eval(src)
        assert isinstance(result, mobjects.Error)
        assert result.msg == target

def test_let_statements():
    test_cases = [
        ("let x = 1; x;", 1),
        ("let _1 = 1; _1;", 1),
        ("let xx = 1 + 1; xx;", 2),
        ("let x = 1; let y = x; x + y", 2),
        ("let x = 1; let y = x; let z = x + y; z", 2),
    ]
    for src, target in test_cases:
        result = run_eval(src)
        assert_integer(result, target)

def test_functions():
    test_cases = [
        ("let add = fn(a, b) { a + b }; add(1, 2);", 3),
        ("let con = fn(){return 1;}; con()", 1),
        ("let max = fn(a, b) { if (a > b) { a; } else { b; };}; max(1*3, 2)", 3),
        ("fn(a, b) {a - b}(2, 1)", 1),
    ]
    for src, target in test_cases:
        result = run_eval(src)
        assert_integer(result, target)

def test_string():
    test_cases = [
        ('"STR"', "STR"),
        ('"strings!!!"', "strings!!!"),
        ('"String" + " " + "Concatenation"', "String Concatenation"),
        ('"Black" + "" + "Magic"', "BlackMagic"),
    ]
    for src, target in test_cases:
        result = run_eval(src)
        assert_string(result, target)