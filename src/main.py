from parser import Tokenizer
from spec import Spec, SpecBuilder

spec = SpecBuilder('./data/md.spec').get_spec()
print(spec)

statements = '''
    IF quantity THEN
        total := total + price * quantity;
        tax := price * 0.05;
    ENDIF;
'''

tokenizer = Tokenizer(spec)

for token in tokenizer.tokenize(statements):
    print(token)
