import re
import sys


SECTION_TERM = '%'
COMMENT_PREFIX = '#'


def remove_comment(text: str) -> str:
    global COMMENT_PREFIX

    start = text.find(COMMENT_PREFIX)

    return text if start == -1 else text[:start].strip()


def next_line(file_iter) -> str:
    try:
        return next(file_iter)
    except StopIteration:
        return None


class Spec:
    def __init__(self):
        self._keywords = set()
        self._tokens = []

    def __str__(self) -> str:
        s = 'Keywords:\n'
        for kw in self._keywords:
            s += f'\t{kw}\n'

        s += 'Tokens:\n'
        for t_id, t_re in self._tokens:
            s += f'\t{t_id:20} /{t_re}/\n'

        return s

    def add_keyword(self, keyword: str) -> None:
        self._keywords.add(keyword)

    def add_token(self, identifier: str, regex: str) -> None:
        token = identifier, regex
        self._tokens.append(token)

    def is_keyword(self, text: str) -> bool:
        return text in self._keywords

    def get_tokens(self) -> tuple:
        for token in self._tokens:
            yield token


class SpecBuilder:
    def __init__(self, filename: str):
        self._spec = Spec()
        self._data = {
            "filename": filename
        }

        self._state = _OpenFile(self)
        self.run()

    def run(self) -> None:
        while self._state is not None:
            self._state = self._state.run()

    def set_data(self, key, value) -> None:
        self._data[key] = value

    def get_data(self, key):
        return self._data[key]

    def get_spec(self) -> Spec:
        return self._spec


class _BuilderState:
    def __init__(self, context: SpecBuilder):
        self._context = context
        self._spec = self._context.get_spec()

    def _set_data(self, key, value):
        self._context.set_data(key, value)

    def _get_data(self, key):
        return self._context.get_data(key)

    def _update_data(self, key, update_func):
        data = self._get_data(key)
        update_func(data)
        self._set_data(key, data)

    def run(self) -> '_BuilderState':
        raise NotImplementedError


class _OpenFile(_BuilderState):
    def run(self) -> _BuilderState:
        filename = self._get_data('filename')
        fin = open(filename, 'r')
        self._set_data('fin', fin)
        self._set_data('lines', iter(fin))

        return _ParseKeywords(self._context)


class _ParseKeywords(_BuilderState):
    REGEX = re.compile(r'^[a-zA-Z]+[a-zA-Z0-9_]*$')

    def __init__(self, context: SpecBuilder):
        super().__init__(context)

        self.fin = self._get_data('lines')

    def run(self) -> _BuilderState:
        line = next_line(self.fin)

        line = line.strip()
        line = remove_comment(line)

        # If empty line, ignore and continue
        if line == '':
            return self

        # If end of section, continue to next state
        if line.startswith(SECTION_TERM):
            return _ParseTokens(self._context)

        # If line is not valid (doesn't match regex), then error
        if self.REGEX.match(line) is None:
            return _Error(self._context, f"Invalid keyword '{line}'")

        # Otherwise, parse line
        self._spec.add_keyword(line)

        return self


class _ParseTokens(_BuilderState):
    REGEX = re.compile(r'^[a-zA-Z]+[a-zA-Z0-9_]*$')

    def __init__(self, context: SpecBuilder):
        super().__init__(context)

        self.fin = self._get_data('fin')
        self._set_data('tokens', [])

    def _next_line(self) -> str:
        line = ''

        while len(line) == 0:
            line = next_line(self.fin)

            if line is None:
                return None

            line = line.strip()
            line = remove_comment(line)

        return line

    def run(self) -> _BuilderState:
        # Get token identifier
        token_id = self._next_line()

        # If end of section, continue to next state
        if token_id is None or token_id.startswith(SECTION_TERM):
            return _Cleanup(self._context)

        # If token identifier is not valid (doesn't match regex), then error
        if self.REGEX.match(token_id) is None:
            return _Error(self._context, f"Invalid token identifier '{token_id}'")

        # -------------------

        # Get token regex specification
        token_regex = self._next_line()

        # If end of section, error
        if token_regex.startswith(SECTION_TERM):
            return _Error(self._context, f"No regex specification found for identifier '{token_id}'")

        self._spec.add_token(token_id, token_regex)

        return self


class _Error(_BuilderState):
    def __init__(self, context: SpecBuilder, reason: str = None):
        super().__init__(context)

        self._reason = reason if reason is not None else 'Unspecified error'

    def run(self) -> _BuilderState:
        print(self._reason, file=sys.stderr)

        return _Cleanup(self._context)


class _Cleanup(_BuilderState):
    def run(self) -> _BuilderState:
        fin = self._get_data('fin')
        fin.close()

        return None
