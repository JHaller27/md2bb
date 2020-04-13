from parser import Tokenizer

keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}
token_specification = [
    ('NUMBER',   r'\d+(\.\d*)?'),  # Integer or decimal number
    ('ASSIGN',   r':='),           # Assignment operator
    ('END',      r';'),            # Statement terminator
    ('ID',       r'[A-Za-z]+'),    # Identifiers
    ('OP',       r'[+\-*/]'),      # Arithmetic operators
    ('NEWLINE',  r'\n'),           # Line endings
    ('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
    ('MISMATCH', r'.'),            # Any other character
]

statements = '''
    IF quantity THEN
        total := total + price * quantity;
        tax := price * 0.05;
    ENDIF;
'''

tokenizer = Tokenizer(keywords, token_specification)

for token in tokenizer.tokenize(statements):
    print(token)
