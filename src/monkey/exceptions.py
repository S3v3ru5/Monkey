
class MonkeyError(Exception):
    """Base class for errors raised in interpretation process"""
    pass

class LexicalError(MonkeyError):
    """Error class for lexical errors"""
    pass