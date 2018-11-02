from Codes import *
from Errors import *
from DataSet import DataSet
from Scaner import Scaner


def translate(filename):
    DIGITS = DataSet(500, 750)
    STRINGS = DataSet(750, 1000)

    scanner = Scaner(filename)

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

        if is_empty(c):
            continue

        if is_dm(c):
            scanner.append(ord(c), c)
            continue

        if is_lt(c):
            res = get_string(c, scanner)

            str = res['str']
            buf = res['c']

            if is_keyword(str):
                scanner.append(keywords[str], str)
            else:
                scanner.append(STRINGS.add(str), str)

            continue

        if is_dg(c):
            dgstr = c
            is_digit_flag = True

            while True:
                c = scanner.read()
                if is_dg(c):
                    dgstr += c
                    continue
                elif is_dm(c) or is_empty(c) or not c:
                    break
                elif is_lt(c):
                    res = get_string(c, scanner)

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

            if is_dm(c):
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

    return {'out': scanner.out, 'STRINGS': STRINGS.set, 'DIGITS': DIGITS.set, 'positions': scanner.positions}


def get_string(c, f):
    str = c

    while True:
        c = f.read()
        if is_lt(c) or is_dg(c):
            str += c
            continue
        else:
            break

    return {'str': str, 'c': c}


res = translate('tests/lab1/Test3')

print 'Strings', res['STRINGS']
print 'Digits', res['DIGITS']

# if len(sys.argv) > 1:
#     res = translate(sys.argv[1])
#
#     print 'Strings', res['TBSTR']
#     print 'Digits', res['TBDS']
#     print 'IDs', res['IDS']
# else:
#     print 'You haven\'t entered the filename\n\n'
