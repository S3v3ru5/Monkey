
import argparse
import os.path
import sys
from datetime import datetime

from monkey.lexer.lexer import Lexer
from monkey.ast.parser import Parser
from monkey.evaluator.environment import Environment
from monkey.evaluator.evaluator import m_eval
from monkey.evaluator import mobjects
from monkey import exceptions

MONKEY_FACE = '''            __,__
   .--.  .-"     "-.  .--.
  / .. \/  .-. .-.  \/ .. \\
 | |  '|  /   Y   \  |'  | |
 | \   \  \ 0 | 0 /  /   / |
  \ '- ,\.-"""""""-./, -' /
   ''-' /_   ^ ^   _\ '-''
       |  \._   _./  |
       \   \ '~' /   /
        '._ '-=-' _.'
           '-----'
'''

PROMPT = ">>> "

def run_script(script_path):
    if not os.path.isfile(script_path):
        print(f"Error: {script_path} is not a file")
        return
    if not script_path.endswith(".mon"):
        print(f"Error: {script_path} is not a monkey script")
        return
    with open(script_path) as f:
        src = f.read()
    try:
        env = Environment()
        l = Lexer(src)
        p = Parser(l)
        program = p.parse()
        if len(p.errors) > 0:
            print(p.errors)
            return
        result = m_eval(program, env)
        if not result.type() == "NULL":
            print(result)
    except exceptions.MonkeyError as e:
        print(e)
        exit()
        

def repl():
    print(MONKEY_FACE)
    print("Monkey v0.0 ", end="")
    print(datetime.now().strftime("(%b %d %Y, %I:%M:%S %p)"))
    print("[Host-> Python] on linux")
    env = Environment()
    try:
        while True:
            src = input(PROMPT)
            try:
                l = Lexer(src)
                p = Parser(l)
                program = p.parse()

                result = m_eval(program, env)
                if not result.type() == "NULL":
                    print(result)
            except (exceptions.LexicalError, exceptions.SyntaxError) as e:
                print(e)
    except (KeyboardInterrupt, EOFError) as e:
        print()
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", default=None)
    args = parser.parse_args()
    if args.file is None:
        repl()
    else:
        run_script(args.file)

if __name__ == "__main__":
    repl()
