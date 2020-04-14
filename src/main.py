from parser import Tokenizer
from spec import Spec, SpecBuilder
import argparse


# Parse arguments
# -------------------------------------

parser = argparse.ArgumentParser()

parser.add_argument('spec', type=str, help='Location of spec file')

args = parser.parse_args()


# Build language spec and input data
# -------------------------------------

spec = SpecBuilder(args.spec).get_spec()
#print(spec)

statements = '''
    IF quantity THEN
        total := total + price * quantity;
        tax := price * 0.05;
    ENDIF;
'''

# Parse input into Tokens
# -------------------------------------

tokenizer = Tokenizer(spec)


# Debug print tokens
# -------------------------------------

for token in tokenizer.tokenize(statements):
    print(token)
