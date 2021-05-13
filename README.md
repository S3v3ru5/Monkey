# Monkey
[![GitHub license](https://img.shields.io/github/license/S3v3ru5/Monkey.svg)](https://github.com/S3v3ru5/Monkey/blob/main/LICENSE) [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)


This is a Python implementation of an interpreter for the Monkey Language.Monkey language is described in the book [Writing an Interpreter in Go](https://interpreterbook.com/) and this interpreter is developed following that book.

## Installation

Monkey can be installed using:
```sh
$ git clone https://github.com/S3v3ru5/Monkey.git
$ pip install Monkey/
```
installing this package will create a command `monkey`.

## Usage

For Monkey REPL, use `monkey` command without any arguments

```
$ monkey
            __,__
   .--.  .-"     "-.  .--.
  / .. \/  .-. .-.  \/ .. \
 | |  '|  /   Y   \  |'  | |
 | \   \  \ 0 | 0 /  /   / |
  \ '- ,\.-"""""""-./, -' /
   ''-' /_   ^ ^   _\ '-''
       |  \._   _./  |
       \   \ '~' /   /
        '._ '-=-' _.'
           '-----'

Monkey v0.1 (May 13 2021, 12:50:41 PM)
[Host-> Python] on linux
>>> 
>>> let i = 0; 
>>> let res = 0;
>>> while (i < 5) { let i = i + 1; let res = res + i;}
>>> res
15
>>> res == 5*(5 + 1)/2
true
>>> 
```

To run a monkey-script, use `monkey` command with filename of the script as the only argument i.e `monkey script.mon`.

```
$ monkey ./samples/fibonacii.mon
calculate nth fibonacii number :
--------------------------------
enter n: 10
result = 55
```
Note: monkey-script filename must have `.mon` extension.

## Changes

changes from [canon monkey language](https://monkeylang.org/)

- This implementation doesn't support HashMaps
- Tracks line number and column of tokens for better error reporting
- Supports while loops

Syntax of while loops
```
while (condition) {
    ...
}
``` 

## License

This source code is licensed under MIT License.