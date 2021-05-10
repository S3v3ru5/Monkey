"""Lexical Analyser for Monkey language"""

from typing import List, Type

from monkey.exceptions import LexicalError
from monkey.lexer.token import Token
from monkey.lexer.token_types import token_types, look_up_identifier

class Lexer:
    """A class for lexical analysis"""
    def __init__(self, source: str) -> None:
        """Initialise Lexer with source code string.

        Args:
            source: input source code to tokenize.
        """
        self.input = source
        self.input_len = len(self.input)
        self.current_char = None
        self.position = 0

        self._advance()
    
    def _peek_char(self, offset: int = 0) -> str:
        """read char without incrementing position.
        
        Args:
            offset: index offset from position variable (default 0).

        Returns:
            character at given offset from position if offset is within
            input length limits else empty string. 
        """
        if not self.position + offset < self.input_len:
            return ""
        return self.input[self.position + offset]
    
    def _advance(self) -> None:
        """advance the position of cursor and set current character"""
        if not self.position < self.input_len:
            self.current_char = None
            return
        self.current_char = self.input[self.position]
        self.position += 1

    def _skip_whitespace(self) -> None:
        """skip whitespaces from the cursor position"""
        while (self.current_char is not None
            and self.current_char.isspace()):
            self._advance()
    
    def tokenize(self) -> List[Type[Token]]:
        """collect all tokens from input.
        
        Returns:
            List of all tokens including EOF token.
        """
        tokens = []
        token = self.get_next_token()
        while token.type != token_types.EOF:
            tokens.append(token)
            token = self.get_next_token()
        tokens.append(token)
        return tokens

    def get_next_token(self) -> Type[Token]:
        """scan input from cursor position and return parsed token.
        
        Returns:
            Token with recognised lexeme.
        Raises:
            raises LexicalError if current char is not a valid lexeme. 
        """
        self._skip_whitespace()

        if self.current_char is None:
            return Token(token_types.EOF, "")

        # Literals
        if self.current_char.isdigit():
            return self._recognise_integer()
        if self.current_char.isalpha() or self.current_char == "_":
            return self._recognise_identifier()
        if self.current_char == '"':
            return self._recognise_string()

        # Arthimetic Operators
        tmp_token = None
        if self.current_char == "+":
            tmp_token = Token(token_types.PLUS, self.current_char)
        elif self.current_char == "-":
            tmp_token = Token(token_types.MINUS, self.current_char)
        elif self.current_char == "*":
            tmp_token = Token(token_types.MUL, self.current_char)
        elif self.current_char == "/":
            tmp_token = Token(token_types.DIV, self.current_char)
        
        if tmp_token is not None:
            self._advance()
            return tmp_token

        # Assignment operator and Equal operator
        if self.current_char == "=":
            buffer = self.current_char
            if self._peek_char() == "=":
                self._advance()
                buffer += self.current_char
                tmp_token = Token(token_types.EQUAL, buffer)
            else:
                tmp_token = Token(token_types.ASSIGN, buffer)
            self._advance()        
            return tmp_token

        # Comparison operators
        tmp_token = None
        if self.current_char == "<":
            tmp_token = Token(token_types.LESSTHAN, self.current_char)
        elif self.current_char == ">":
            tmp_token = Token(token_types.GREATERTHAN, self.current_char)
        elif self.current_char == "!":
            buffer = self.current_char
            if self._peek_char() == "=":
                self._advance()
                buffer += self.current_char
                tmp_token = Token(token_types.NOT_EQUAL, buffer)
            else:
                tmp_token = Token(token_types.NOT, buffer)
        if tmp_token is not None:
            self._advance()
            return tmp_token
        
        # Delimeters
        tmp_token_type = {
            "(": token_types.LPAREN,
            ")": token_types.RPAREN,
            "[": token_types.LBRACKET,
            "]": token_types.RBRACKET,
            "{": token_types.LBRACE,
            "}": token_types.RBRACE,
            ",": token_types.COMMA,
            ";": token_types.SEMICOLON,
        }.get(self.current_char, None)
        
        if tmp_token_type is not None:
            tmp_token = Token(tmp_token_type, self.current_char) 
            self._advance()
            return tmp_token
                     
        raise LexicalError(f"LexicalError: unrecognised token at or near {self.current_char}")

    def _recognise_integer(self) -> Type[Token]:
        """recognise integers.
        
        Integer         ::= decinteger
        decinteger      ::= nonzerodigit (["_"] digit)* | "0"+ (["_"] + "0")*
        nonzerodigit    ::= "1"..."9"
        digit           ::= "0"..."9"
        
        Returns:
            returns INTEGER token with scanned value.
        
        Raises:
            raises LexicalError if any grammar rules are violated. 
        """
        buffer = ""

        # decinteger
        if self.current_char.isdigit() and self.current_char != "0":
            buffer += self.current_char
            self._advance()
            while self.current_char is not None:
                if self.current_char.isdigit():
                    buffer += self.current_char
                    self._advance()
                elif self.current_char == "_":
                    self._advance()
                    if (self.current_char is None
                        or not self.current_char.isdigit()):
                        error_msg = f"invalid integer {buffer + '_'}\n"
                        error_msg += "integers cannot end with '_',"
                        error_msg += "'_' can only used in the middle as"
                        error_msg += "visual separator.\n"
                        error_msg += "LexicalError: Invalid integer literal"
                        raise LexicalError(error_msg)
                    buffer += self.current_char
                    self._advance()
                else:
                    break
        elif self.current_char == "0":
            buffer += self.current_char
            while self.current_char is not None:
                if self.current_char == "0":
                    self._advance()
                elif self.current_char == "_":
                    self._advance()
                    if (self.current_char is None
                        or not self.current_char == "0"):
                        error_msg = f"invalid integer literal {buffer + '_'}"
                        raise LexicalError(f"LexicalError: {error_msg}")
                    self._advance()
                else:
                    break
        
        if (self.current_char is not None
            and self.current_char.isalpha()):
            error_msg = f"invalid identifier {buffer + self.current_char}\n"
            error_msg = "identifiers cannot start with a number\n"
            raise LexicalError(f"{error_msg}\nLexicalError: Invalid Identifier")

        return Token(token_types.INTEGER, int(buffer))

    def _recognise_identifier(self) -> Type[Token]:
        """recognise identifiers and keywords.

        Identifier  ::= (letter | _) (letter | digit | _)*
        letter      ::= [a-zA-z]
        digit       ::= [0-9]
        """
        buffer = ""
        if self.current_char.isalpha() or self.current_char == "_":
            buffer += self.current_char
            self._advance()
        while self.current_char is not None:
            if (self.current_char.isalpha() 
                or self.current_char.isdigit()
                or self.current_char == "_"):

                buffer += self.current_char
                self._advance()
            else:
                break
        tmp_token_type = look_up_identifier(buffer)
        if tmp_token_type is not None:
            return Token(tmp_token_type, buffer)
        return Token(token_types.IDENTIFIER, buffer)
    
    def _recognise_string(self) -> Type[Token]:
        """recognise strings enclosed in double quotation marks.
        
        stringliteral   ::= '"' stringitem* '"'
        stringitem      ::= stringchar
        stringchar      ::= <any source character>

        Returns:
            returns STRING type token with string as value. 
        """
        buffer = ""
        if self.current_char == '"':
            self._advance()
        while self.current_char is not None:
            if self.current_char == '"':
                self._advance()
                break
            buffer += self.current_char
            self._advance()
        return Token(token_types.STRING, buffer)
    
if __name__ == "__main__":
    test = """let five = 5;
    let ten = 10;
    let add = fn(x, y) {
        x + y;
    };
    
    let result = add(five, ten);
    """
    l = Lexer(test)
    while True:
        token = l.get_next_token()
        if token.type == token_types.EOF:
            print(token)
            break
        print(token)
