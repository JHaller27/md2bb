import re
from src.spec import Spec


class Token:
    KEYWORD = 'KEYWORD'

    def __init__(self, name: str, value: str, line: int, column: int):
        self._name = name
        self._value = value
        self._line = line
        self._column = column

    def __str__(self) -> str:
        return f"Token(name='{self._name}', value='{self._value}', line={self._line}, column={self._column})"


class Tokenizer:
    def __init__(self, spec: Spec):
        self._spec = spec

    def tokenize(self, code: str):
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self._spec.get_tokens())
        line_num = 1
        line_start = 0
        for match_obj in re.finditer(tok_regex, code):
            kind = match_obj.lastgroup
            value = match_obj.group()
            column = match_obj.start() - line_start
            if kind == Spec.NEWLINE:
                line_start = match_obj.end()
                line_num += 1
                continue
            elif kind == Spec.MISMATCH:
                raise RuntimeError(f'{value!r} unexpected on line {line_num}')
            elif self._spec.is_keyword(value):
                kind = Token.KEYWORD

            yield Token(kind, value, line_num, column)
