IF
THEN
ENDIF
FOR
NEXT
GOSUB
RETURN

%

# Integer or decimal number
NUMBER
\d+(\.\d*)?

# Assignment operator
ASSIGN
:=

# Statement terminator
END
;

# Identifiers
ID
[A-Za-z]+

# Arithmetic operators
OP
[+\-*/]

# Line endings
NEWLINE
\n

# Skip over spaces and tabs
SKIP
[ \t]+

# Any other character
MISMATCH
.
