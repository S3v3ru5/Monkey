"""Define all available Token Types"""

from types import SimpleNamespace
from typing import Optional

token_types = {
    # Keywords
    "LET"       : "let",
    "FUNCTION"  : "fn",
    "TRUE"      : "true",
    "FALSE"     : "false",
    "IF"        : "if",
    "ELSE"      : "else",
    "RETURN"    : "return",
    "WHILE"     : "while",

    # Arthimetic Operators
    "PLUS"  : "+",
    "MINUS" : "-",
    "MUL"   : "*",
    "DIV"   : "/",

    # Assignment Operators
    "ASSIGN": "=",

    # Comparison Operators
    "EQUAL"         : "==",
    "NOT_EQUAL"     : "!=",
    "LESSTHAN"      : "<",
    "GREATERTHAN"   : ">",

    "NOT": "!",
    
    # Delimiters
    "LPAREN"    : "(",
    "RPAREN"    : ")",
    "LBRACKET"  : "[",
    "RBRACKET"  : "]",
    "LBRACE"    : "{",
    "RBRACE"    : "}",
    "COMMA"     : ",",
    "SEMICOLON" : ";",

    # Literals
    "IDENTIFIER": "IDENTIFIER",
    "BOOLEAN"   : "BOOLEAN",
    "STRING"    : "STRING",
    "INTEGER"   : "INTEGER",

    # Others
    "EOF"           : "EOF",
    "UNRECOGNISED"  : "UNRECOGNISED",
}

TOKEN_TYPES = SimpleNamespace(**token_types)

def look_up_identifier(identifier: str) -> Optional[str]:
    """check whether given identifier is keyword or not.

    Args:
        identifier: identifier to check.
    
    Returns:
        returns keyword token type if identifier is keyword
        else None.
    """
    keywords = {
        "let"       : TOKEN_TYPES.LET,
        "fn"        : TOKEN_TYPES.FUNCTION,
        "true"      : TOKEN_TYPES.TRUE,
        "false"     : TOKEN_TYPES.FALSE,
        "if"        : TOKEN_TYPES.IF,
        "else"      : TOKEN_TYPES.ELSE,
        "return"    : TOKEN_TYPES.RETURN,
        "while"     : TOKEN_TYPES.WHILE,
    }
    return keywords.get(identifier, None)
