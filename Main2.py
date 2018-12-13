from Codes import *
from DataSet import DataSet
from Main import translate
import json

res = translate('tests/lab1/Test6')
print res
out = res['out']
strings = res['STRINGS']
digits = res['DIGITS']
positions = res['positions']

IDS = DataSet(1000, 1500)
LABELS = DataSet(1000, 1500)
errors = []


def generate_node(name, rule=None, is_leaf=False, is_error=False):
    node = {'text': {'name': name}}

    if rule:
        node['text']['title'] = rule

    if is_error: node['HTMLclass'] = 'error-draw'
    else : node['HTMLclass'] = 'leaf-draw' if is_leaf else 'first-draw'

    node['children'] = []

    return node

def append_child(func, i, node):
    if i >= len(out):
        append_error("<{0}> expected".format(func.__name__), node, i)
        return i

    child = func(i)
    if child['node']:
        node['children'].append(child['node'])
    return child['i']


def append_error(text, node, i):
    _line = ""
    if i < len(out): _line = "Line: {0}:{1} -> ".format(positions[i][0], positions[i][1])
    text = "{0}{1}".format(_line, text)
    errors.append(text)
    node['children'].append(generate_node(text, None, True, True))


def SIG_PROG(i = 0):
    node = generate_node('<SIG_PROG>', 1)
    i = append_child(PROG, i, node)

    if i < len(out):
        append_error('End of file expected', node, i)

    return node


def PROG(i):
    node = generate_node('<PROG>', 2)
    if out[i] != keywords['PROGRAM']:
        append_error('Keyword PROGRAM expected', node, i)
    else:
        node['children'].append(generate_node('PROGRAM', None, True))
        i += 1

    i = append_child(PROC_ID, i, node)

    if i >= len(out) or out[i] != ord(';'):
        append_error('; expected', node, i)
    else:
        node['children'].append(generate_node(';', None, True))
        i += 1

    i = append_child(BLOCK, i, node)

    return {'node': node, 'i': i}


def BLOCK(i):
    node = generate_node('<BLOCK>', 3)
    i = append_child(DECL, i, node)

    if i >= len(out) or out[i] != keywords['BEGIN']:
        append_error('Keyword BEGIN expected', node, i)
    else:
        node['children'].append(generate_node('BEGIN', None, True))
        i += 1

    if i < len(out): i = append_child(ST_LIST, i, node)

    if i >= len(out) or out[i] != keywords['END']:
        append_error('Keyword END expected', node, i)
    else:
        node['children'].append(generate_node('END', None, True))
        i += 1

    return {'node': node, 'i': i}


def DECL(i):
    if out[i] == keywords['BEGIN']:
        return {'node': None, 'i': i}

    node = generate_node('<DECL>', 4)

    if i < len(out): i = append_child(LBL_DECL, i, node)

    return {'node': node, 'i': i}

def LBL_DECL(i):
    if out[i] == keywords['BEGIN']:
        return {'node': None, 'i': i}

    node = generate_node('<LBL_DECL>', 5)

    if out[i] != keywords['LABEL']:
        append_error('Keyword LABEL expected', node, i)
    else:
        node['children'].append(generate_node('LABEL', None, True))
        i += 1

    i = append_child(INT, i, node)
    if i < len(out): i = append_child(LBL_LIST, i, node)

    if out[i] != ord(';'):
        append_error('; expected', node, i)
    else:
        node['children'].append(generate_node(';', None, True))
        i += 1

    return {'node': node, 'i': i}


def LBL_LIST(i):
    if out[i] == ord(';'):
        return {'node': None, 'i': i}

    node = generate_node('<LBL_LIST>', 6)

    if out[i] != ord(','):
        append_error(', expected', node, i)
    else:
        node['children'].append(generate_node(',', None, True))
        i += 1

    _tmp = i
    i = append_child(INT, i, node)
    if _tmp != i: i = append_child(LBL_LIST, i, node)

    return {'node': node, 'i': i}


def ST_LIST(i):
    if i >= len(out) or out[i] == keywords['END']:
        return {'node': None, 'i': i}

    node = generate_node('<ST_LIST>', 7)

    _tmp = i
    i = append_child(ST, i, node)
    if _tmp != i and i < len(out): i = append_child(ST_LIST, i, node)

    return {'node': node, 'i': i}

def ST(i):
    node = generate_node('<ST>', 8)

    _flag = True

    if out[i] in digits:
        _flag = False
        i = append_child(INT, i, node)

        if out[i] != ord(':'):
            append_error(': expected', node, i)
        else:
            node['children'].append(generate_node(':', None, True))
            i += 1

        i = append_child(ST, i, node)

    elif out[i] in (keywords[k] for k in ['GOTO', 'IN', 'OUT']):
        node['children'].append(generate_node(get_keyword_by_code(out[i]), None, True))
        i += 1

        i = append_child(INT, i, node)
    elif out[i] == keywords['LINK']:
        node['children'].append(generate_node('LINK', None, True))
        i += 1

        i = append_child(VAR_ID, i, node)

        if out[i] != ord(','):
            append_error(', expected', node, i)
        else:
            node['children'].append(generate_node(',', None, True))
            i += 1

        i = append_child(INT, i, node)
    else:
        append_error('Invalid statement', node, i)
        i += 1

    if _flag:
        if out[i] != ord(';'):
            append_error('; expected', node, i)
        else:
            node['children'].append(generate_node(';', None, True))
            i += 1

    return {'node': node, 'i': i}


def VAR_ID(i):
    node = generate_node('<VAR_ID>', 9)

    i = append_child(ID, i, node)

    return {'node': node, 'i': i}


def PROC_ID(i):
    node = generate_node('<PROC_ID>', 10)

    i = append_child(ID, i, node)

    return {'node': node, 'i': i}

def ID(i):
    node = generate_node('<ID>', 11)

    if not out[i] in strings:
        append_error('String expected. Line: {0}:{1}', node, i)
    elif IDS.get_id_by_value(out[i]):
        append_error('Identifier is already defined', node, i)
    else:
        node['children'].append(generate_node(strings[out[i]], None, True))

        IDS.add(out[i])
        i += 1

    return {'node': node, 'i': i}


def INT(i):
    node = generate_node('<INT>', 13)

    if not out[i] in digits:
        append_error('Digit expected', node, i)
    else:
        node['children'].append(generate_node(digits[out[i]], None, True))

        i += 1

    return {'node': node, 'i': i}


def print_table(name, table):
    print '\n', name
    for key in table:
        print key, '\t|\t', table[key]

TREE = {}
if len(out): TREE = SIG_PROG(0)

f = open("tree/tree.js","w+")

f.write("var nodeStructure = '")
f.write(json.dumps(TREE))
f.write("'")

f.close()
#
print_table('Strings', strings)
print_table('Digits', digits)
print_table('IDs', IDS.set)

print IDS.set

# print '\n\nLexer ERRORS:'
# for i in res['errors']:
#     print i

print '\n\nSyntax ERRORS:'
for i in errors:
    print i
