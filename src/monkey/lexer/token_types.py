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

token_types = SimpleNamespace(**token_types)

def look_up_identifier(identifier: str) -> Optional[str]:
    """check whether given identifier is keyword or not.

    Args:
        identifier: identifier to check.
    
    Returns:
        returns keyword token type if identifier is keyword
        else None.
    """
    keywords = {
        "let"       : token_types.LET,
        "fn"        : token_types.FUNCTION,
        "true"      : token_types.TRUE,
        "false"     : token_types.FALSE,
        "if"        : token_types.IF,
        "else"      : token_types.ELSE,
        "return"    : token_types.RETURN,
    }
    return keywords.get(identifier, None)