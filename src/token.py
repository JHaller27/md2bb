import re


class Token:
    def __init__(self, regex: str):
        self._regex = re.compile(regex)

    def parse(self, text: str) -> Token:
        pass
