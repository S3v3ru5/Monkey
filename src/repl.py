

from monkey.lexer.lexer import Lexer
from monkey.ast.parser import Parser
from monkey.evaluator.environment import Environment
from monkey.evaluator.evaluator import m_eval
from monkey.evaluator import mobjects

PROMPT = ">> "

def run():
    env = Environment()
    while True:
        src = input(PROMPT)
        l = Lexer(src)
        p = Parser(l)
        program = p.parse()
        if len(p.errors) > 0:
            print(p.errors)
            continue
        result = m_eval(program, env)
        if not result.type() == "NULL":
            print(result)

if __name__ == "__main__":
    run()