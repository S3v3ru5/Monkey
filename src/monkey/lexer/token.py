"""Define Token class"""

from typing import Any

class Token:
    """class describing a token.

    Attributes:
        type: Token type.
        value: value of the Token.
    """
    def __init__(self, token_type: str, value: Any, line = 0, column = 0) -> None:
        """define a token."""
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"<{self.type}, {self.value}, {self.line}, {self.column}>"
    
    def __repr__(self) -> str:
        return self.__str__()
    