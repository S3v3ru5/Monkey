"""Defines built-in functions for Monkey Language."""

from monkey.evaluator import mobjects
from monkey.evaluator import evaluator

def m_error(msg) -> mobjects.Error:
    """create an error in Monkey"""
    return mobjects.Error(msg)
    
def m_len(*args) -> mobjects.Object:
    if len(args) != 1:
        return m_error(f"len takes exactly one argument ({len(args)} given)")
    if not isinstance(args[0], mobjects.String):
        return m_error(f"object of type {args[0].type()} has no len()")
    return mobjects.Integer(value=len(args[0].value))

def m_puts(*args) -> mobjects.Object:
    supported_types = [
        mobjects.INTEGER_OBJ,
        mobjects.BOOLEAN_OBJ,
        mobjects.NULL_OBJ,
        mobjects.STRING_OBJ,
    ]
    for value in args:
        if value.type() not in supported_types:
            return m_error(f"unsupported type for printing: {value.type()}")
    print(" ".join(str(value) for value in args))
    return evaluator.NULL


builtins = {
    "len": mobjects.Builtin(m_len),
    "puts": mobjects.Builtin(m_puts),
}