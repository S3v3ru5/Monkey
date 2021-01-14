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
    # supported_types = [
    #     mobjects.INTEGER_OBJ,
    #     mobjects.BOOLEAN_OBJ,
    #     mobjects.NULL_OBJ,
    #     mobjects.STRING_OBJ,
    # ]
    # for value in args:
    #     if value.type() not in supported_types:
    #         return m_error(f"unsupported type for printing: {value.type()}")
    print(" ".join(str(value) for value in args))
    return evaluator.NULL

# def m_remove(*args) -> mobjects.Object:
#     if len(args) != 2:
#         return m_error(f"remove takes exactly 2 arguments ({len(args)} given)")
#     array, value = args
#     if array.type() != mobjects.ARRAY_OBJ:
#         return m_error(f"object of type {args[0].type()} has no remove()")
#     if value.value not in array.elements:
#         return m_error(f"{value.value} not in array")
#     array.elements.remove(value.value)
#     return NULL

def m_append(*args) -> mobjects.Object:
    if len(args) != 2:
        return m_error(f"append takes exactly 2 arguments ({len(args)} given)")
    array, value = args
    if array.type() != mobjects.ARRAY_OBJ:
        return m_error(f"object of type {args[0].type()} has no append()")
    array.elements.append(value)
    return evaluator.NULL

def m_input(*args) -> mobjects.Object:
    if len(args) > 1:
        return m_error(f"input takes atmost one argument ({len(args)} given)")
    print(*args, end="")
    value = input()
    try:
        return mobjects.Integer(int(value))
    except ValueError:
        return m_error(f"invalid literal for integer: '{value}'")

def m_raw_input(*args) -> mobjects.Object:
    if len(args) > 1:
        return m_error(f"raw_input takes atmost ")
    print(*args, end="")
    value = input()
    return mobjects.String(value)

builtins = {
    "len": mobjects.Builtin(m_len),
    "puts": mobjects.Builtin(m_puts),
    "append": mobjects.Builtin(m_append),
    "input": mobjects.Builtin(m_input),
    "raw_input": mobjects.Builtin(m_raw_input),
}
