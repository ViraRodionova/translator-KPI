from Codes import *

ascii = {}

def getTableOfAttributes():
    ascii = {}

    for i in range(127):
        if i >= 65 and i <= 90:
            ascii[i] = SymbolType.letter
            continue

        if i >= 48 and i <= 57:
            ascii[i] = SymbolType.digit
            continue

        if i in empty:
            ascii[i] = SymbolType.empty
            continue

        if chr(i) in delims:
            ascii[i] = SymbolType.delim
            continue

        ascii[i] = SymbolType.unexpected

    return ascii




