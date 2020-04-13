import re


class Token:
    def __init__(self, name: str, value: str, line: int, column: int):
        self._name = name
        self._value = value
        self._line = line
        self._column = column

    def __str__(self) -> str:
        return f"Token(name='{self._name}', value='{self._value}', line={self._line}, column={self._column})"


class Tokenizer:
    def __init__(self, keywords: set, token_map: list):
        self._keywords = keywords
        self._token_map = token_map

    def tokenize(self, code: str):
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self._token_map)
        line_num = 1
        line_start = 0
        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif kind == 'ID' and value in self._keywords:
                kind = value
            elif kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
                continue
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {line_num}')
            yield Token(kind, value, line_num, column)
