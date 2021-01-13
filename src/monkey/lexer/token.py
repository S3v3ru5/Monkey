"""Define Token class"""

from typing import Any

class Token:
    """class describing a token.

    Attributes:
        type: Token type.
        value: value of the Token.
    """
    def __init__(self, token_type: str, value: Any) -> None:
        """define a token."""
        self.type = token_type
        self.value = value

    def __str__(self) -> str:
        return f"<{self.type}, {self.value}>"
    
    def __repr__(self) -> str:
        return self.__str__()
    