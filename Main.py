from Codes import *
from Errors import *
from DataSet import DataSet
from Scanner import Scanner
from Attribute import *

import sys

def translate(filename):
    DIGITS = DataSet(500, 750)
    STRINGS = DataSet(750, 1000)
    scanner = Scanner(filename)
    attributesTable = getTableOfAttributes()

    buf = ''

    while True:
        if buf:
            c = buf
            buf = ''
            scanner.decreaseCol()
        else:
            c = scanner.read(True)

        if not c:
          break

        if attributesTable[ord(c)] == SymbolType.empty:
            continue

        if attributesTable[ord(c)] == SymbolType.delim:
            scanner.append(ord(c), c)
            continue

        if attributesTable[ord(c)] == SymbolType.letter:
            res = get_string(c, attributesTable, scanner)

            str = res['str']
            buf = res['c']

            if is_keyword(str):
                scanner.append(keywords[str], str)
            else:
                scanner.append(STRINGS.add(str), str)

            continue

        if attributesTable[ord(c)] == SymbolType.digit:
            dgstr = c
            is_digit_flag = True

            while True:
                c = scanner.read()
                if attributesTable[ord(c)] == SymbolType.digit:
                    dgstr += c
                    continue
                elif attributesTable[ord(c)] == SymbolType.delim or attributesTable[ord(c)] == SymbolType.empty or not c:
                    break
                elif attributesTable[ord(c)] == SymbolType.letter:
                    res = get_string(c, attributesTable, scanner)

                    dgstr += res['str']
                    buf = res['c']

                    is_digit_flag = False
                    break
                else:
                    raise UnexpectedSymbolException([scanner.line, scanner.column - 1], c)

            if is_digit_flag:
                scanner.append(DIGITS.add(dgstr), dgstr)
            elif is_keyword(dgstr):
                scanner.append(keywords[dgstr], dgstr)
            else:
                scanner.append(STRINGS.add(dgstr), dgstr)

            if attributesTable[ord(c)] == SymbolType.delim:
                buf = c

            continue

        if c == '(':
            c = scanner.read(True)
            if c == '*':
                while True:
                    c = scanner.read(True)

                    if c == '*':
                        while c == '*':
                            c = scanner.read(True)
                        if c == ')':
                            flag = True
                            break
                        else:
                            continue
                    elif not c:
                        scanner.exception(EndOfFileException)
                    else:
                        continue

                if flag:
                    continue
            else:
                raise UnexpectedSymbolException([scanner.line, scanner.column - 2], '(')

        scanner.exception(UnexpectedSymbolException, c)

    # scanner.handleEndOfReading()

    return {'out': scanner.out, 'STRINGS': STRINGS.set, 'DIGITS': DIGITS.set, 'positions': scanner.positions}


def get_string(c, attributesTable, f):
    str = c

    while True:
        c = f.read()

        if attributesTable[ord(c)] == SymbolType.letter or attributesTable[ord(c)] == SymbolType.digit:
            str += c
            continue
        else:
            break

    return {'str': str, 'c': c}


# res = translate('tests/lab1/Test3')

#
# print 'Strings', res['STRINGS']
# print 'Digits', res['DIGITS']

# if len(sys.argv) > 1:
#     res = translate(sys.argv[1])
#
#     print 'Strings', res['STRINGS']
#     print 'Digits', res['DIGITS']
# else:
#     print 'You haven\'t entered the filename\n\n'
