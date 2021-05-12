"""Internal Object representation of Monkey data"""

INTEGER_OBJ = "INTEGER"
BOOLEAN_OBJ = "BOOLEAN"
STRING_OBJ = "STRING"
NULL_OBJ = "NULL"
RETURN_VALUE_OBJ = "RETURN_VAL"
ERROR_OBJ = "ERROR"
FUNCTION_OBJ = "FUNCTION"
BUILTIN_OBJ = "BUILTIN"
ARRAY_OBJ = "ARRAY"

class Object():
    def __init__(self):
        pass

class Integer(Object):
    def __init__(self, value: int = None):
        self.value:int = value
    
    def type(self):
        return INTEGER_OBJ

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return self.__str__()

class Boolean(Object):
    def __init__(self, value: bool = None):
        self.value: bool = value
    
    def type(self):
        return BOOLEAN_OBJ

    def __str__(self):
        return "true" if self.value else "false"
    
    def __repr__(self):
        return self.__str__()

class String(Object):
    def __init__(self, value: str = None):
        self.value: str = value
    
    def type(self):
        return STRING_OBJ

    def __str__(self):
        return self.value
    
    def __repr__(self):
        return self.__str__()

class Null(Object):
    def __init__(self):
        pass

    def type(self):
        return NULL_OBJ
    
    def __str__(self):
        return "null"
    
    def __repr__(self):
        return self.__str__()

class ReturnValue(Object):
    def __init__(self, value = None):
        self.value: Object = value
    
    def type(self):
        return RETURN_VALUE_OBJ

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return self.__str__()

class Error(Object):
    def __init__(self, msg = None):
        self.msg = msg
    
    def type(self):
        return ERROR_OBJ

    def __str__(self):
        return f"EvaluationError: {self.msg}"
    
    def __repr__(self):
        return self.__str__()

class Function(Object):
    def __init__(self, parameters = None, body = None, env = None):
        self.parameters = parameters
        self.body = body
        self.env = env
    
    def type(self):
        return FUNCTION_OBJ
    
    def __str__(self):
        return "<function>"
    
    def __repr__(self):
        return self.__str__()

class Builtin(Object):
    def __init__(self, function):
        self.function = function
    
    def type(self):
        return BUILTIN_OBJ
    
    def __str__(self):
        return "<built-in function>"
    
    def __repr__(self):
        return self.__str__()

class Array(Object):
    def __init__(self, elements):
        self.elements = elements

    def type(self):
        return ARRAY_OBJ
    
    def __str__(self):
        return "[" + ", ".join(str(element) for element in self.elements) + "]"
    
    def __repr__(self):
        return self.__str__()
