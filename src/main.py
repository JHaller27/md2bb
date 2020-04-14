from parser import Tokenizer
from spec import Spec, SpecBuilder
import argparse


# Parse arguments
# -------------------------------------

parser = argparse.ArgumentParser()

parser.add_argument('spec', type=str,
    help='Path to language specification file')

parser.add_argument('input_file', type=str, default='-', metavar='[input_file]',
    help='Path to file to parse, or - to read from stdin (default: -)')

parser.add_argument('--show-spec', '-s', action='store_true', dest='show_spec',
    help='Show parsed language specification')

args = parser.parse_args()


# Build language spec and input data
# -------------------------------------

spec = SpecBuilder(args.spec).get_spec()
if args.show_spec:
    print(spec)

statements = []
if args.input_file == '-':
    try:
        while line := input():
            statements.append(line)
    except EOFError:
        pass

else:
    with open(args.input_file, 'r') as fin:
        for line in fin:
            statements.append(line)
statements = '\n'.join(statements)


# Parse input into Tokens
# -------------------------------------

tokenizer = Tokenizer(spec)


# Debug print tokens
# -------------------------------------

for token in tokenizer.tokenize(statements):
    print(token)
