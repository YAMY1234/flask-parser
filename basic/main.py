# coding:utf-8
from __future__ import print_function
import re
import os
import io
import copy
import json

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'for': 'FOR',
    'int': 'INT',
    'char': 'CHAR',
    'float': 'FLOAT',
    'return': 'RETURN',
    'void': 'VOID',
    # 'function':'FUNCTION',
    'goto': 'GOTO',
    'number': 'NUMBER'
}  # 保留字

type = [
    'seperator', 'operator', 'identifier', 'float', 'int', 'char'
]  # 类别
# 注意上面下面两个的对应顺序一定要关联起来
regexs = [
    '\{|\}|\[|\]|\(|\)|,|;|\?|\:'  # 界符    |\.   这个表示浮点的我暂时去掉了
    , '\+|-|\*|%|/|>=|<=|>|<|==|!=|='  # 操作符
    , '[a-zA-Z_][a-zA-Z_0-9]*'  # 标识符
    # ,'\".+?\"'#字符串
    , '-?\d+\.\d+?'  # 浮点数--之前的
    , '\d+'  # 整数
    , '\'.{1}\''  # 字符
]  # 词法分析所使用的正则表达式

SOURCE_PATH = os.getcwd()+'/source_file'


NAME_SOURCE_CODE = "test.c"
NAME_GRAMMER_JSON = "grammer.json"
NAME_GRAMMER_PLAIN = "grammer.txt"
NAME_LR1 = "lr1.table"
NAME_ANALYSIS = "analysis.table"
# newly added
NAME_INTERMEDIATE_CODE = "result.middle"
NAME_ASM = "result.asm"


CURRENT_LINE = 1
CURRENT_LABLE = 0
CURRENT_TEMP = 0
CURRENT_FUNCTION = 0
CURRENT_STEP = 0
CURRENT_OFFSET = 0
CURRENT_PRODUCTION = None
CURRENT_FUNCTION_SYMBOL = None

PRODUCTION_GROUP = []  # 所有产生式的集合
PRODUCTION_GROUP_DOTED = []  # 所有加点的产生式，这个就是所谓的项目了
TERMINAL_SYMBOL_GROUP = []
NONE_TERMINAL_SYMBOL_GROUP = []  # 非终结符集合

STATE_INDEX_TABLE = {}
TERMINAL_INDEX_TABLE = {}
NONE_TERMINAL_INDEX_TABLE = {}

ACTION = []
GOTO = []
REDUCE = {}
SHIFT = {}
FIRST = {}
FOLLOW = {}

OP_STACK = []
STATE_STACK = []
SEMANTIC_STACK = []

SYMBOL_TABLE = []
FUNCTION_TABLE = []
REGISTER_TABLE = {'$' + str(x): '' for x in range(7, 26)}

RECORD_TABLE = None
START_PRODUCTION = None
TEMP_VALUE_STATUS = {}
TOKENS = []
MIPS_CODE = []
INTERMEDIATE_CODE = []
STACK_OFFSET = 8000
DATA_SEGMENT = 10010000

ERROR_TOKEN = ''

'''
renew_variables(): 刷新所有全局变量
'''


def renew_variables():
    global CURRENT_LINE
    global CURRENT_LABLE
    global CURRENT_TEMP
    global CURRENT_FUNCTION
    global CURRENT_STEP
    global CURRENT_OFFSET
    global CURRENT_PRODUCTION
    global CURRENT_FUNCTION_SYMBOL

    global PRODUCTION_GROUP  # 所有产生式的集合
    global PRODUCTION_GROUP_DOTED  # 所有加点的产生式，这个应该就是所谓的项目了
    global TERMINAL_SYMBOL_GROUP
    global NONE_TERMINAL_SYMBOL_GROUP  # 看上去像是非终结符集合？？下面的那些表达的是什么含义呢

    global STATE_INDEX_TABLE
    global TERMINAL_INDEX_TABLE
    global NONE_TERMINAL_INDEX_TABLE

    global ACTION
    global GOTO
    global REDUCE
    global SHIFT
    global FIRST
    global FOLLOW

    global OP_STACK
    global STATE_STACK
    global SEMANTIC_STACK

    global SYMBOL_TABLE
    global FUNCTION_TABLE
    global REGISTER_TABLE

    global RECORD_TABLE
    global START_PRODUCTION
    global TEMP_VALUE_STATUS
    global TOKENS
    global MIPS_CODE
    global INTERMEDIATE_CODE
    global STACK_OFFSET
    global DATA_SEGMENT

    CURRENT_LINE = 1
    CURRENT_LABLE = 0
    CURRENT_TEMP = 0
    CURRENT_FUNCTION = 0
    CURRENT_STEP = 0
    CURRENT_OFFSET = 0
    CURRENT_PRODUCTION = None
    CURRENT_FUNCTION_SYMBOL = None

    PRODUCTION_GROUP = []  # 所有产生式的集合
    PRODUCTION_GROUP_DOTED = []  # 所有加点的产生式，这个应该就是所谓的项目了
    TERMINAL_SYMBOL_GROUP = []
    NONE_TERMINAL_SYMBOL_GROUP = []  # 看上去像是非终结符集合？？下面的那些表达的是什么含义呢
    # ['expression_statement', 'function_implement', 'operator', 'iteration_statement', 'expression_profix', 'assignment_expression', 'external_declaration', 'type_specifier', 'compound_statement', 'assignment_expression_list', 'selection_statement', 'start', 'statement', 'constant_expression', 'arithmetic_expression', 'declaration_init', 'function_declaration_suffix', 'function_declaration_list', 'assignment_expression_profix', 'declaration', 'declaration_assign', 'declaration_init_list', 'jump_statement', 'function_definition', 'function_declaration', 'expression_list', 'assignment_operator', 'statement_list', 'function_expression', 'expression', 'primary_expression']

    STATE_INDEX_TABLE = {}
    TERMINAL_INDEX_TABLE = {}
    NONE_TERMINAL_INDEX_TABLE = {}

    ACTION = []
    GOTO = []
    REDUCE = {}
    SHIFT = {}
    FIRST = {}
    FOLLOW = {}

    OP_STACK = []
    STATE_STACK = []
    SEMANTIC_STACK = []

    SYMBOL_TABLE = []
    FUNCTION_TABLE = []
    REGISTER_TABLE = {'$' + str(x): '' for x in range(7, 26)}

    RECORD_TABLE = None
    START_PRODUCTION = None
    TEMP_VALUE_STATUS = {}
    TOKENS = []
    MIPS_CODE = []
    INTERMEDIATE_CODE = []
    STACK_OFFSET = 8000
    DATA_SEGMENT = 10010000


'''
下面是类定义
'''


class Node():
    def __init__(self):
        self.place = None  # 语句块入口的中间变量
        self.code = []  # 传递而来的或者生成的中间代码
        self.stack = []  # 翻译闭包表达式所用的临时栈
        self.name = None  # 语句块的标识符
        self.type = None  # 结点的数据类型
        self.data = None  # 结点携带的数据
        self.begin = None  # 循环入口
        self.end = None  # 循环出口
        self.true = None  # 为真时的跳转位置
        self.false = None  # 为假时的跳转位置


class Symbol:
    def __init__(self):
        self.name = None  # 符号的标识符
        self.type = None  # 类型
        self.size = None  # 占用字节数
        self.offset = None  # 内存偏移量
        self.place = None  # 对应的中间变量
        self.function = None  # 所在函数


class FunctionSymbol:
    def __init__(self):
        self.name = None  # 函数的标识符
        self.type = None  # 返回值类型
        self.lable = None  # 入口处的标签
        self.params = []  # 形参列表
        self.temp = []  # 局部变量列表


class Production():
    def __init__(self, left, right, position=0, terminals=None):
        self.left = left
        self.right = right
        self.position = position
        self.terminals = terminals

    def next_doted_production(self):
        return Production(self.left,
                          self.right,
                          self.position + 1,
                          self.terminals)

    def to_string(self):
        result = self.left+'->'
        position = 1
        for data in self.right:
            if position == self.position:
                result += '@'
            result += data['type']+' '
            position += 1
        if position == self.position:
            result += '@'
        result += ',['
        if self.terminals != None:
            if len(self.terminals) > 0:
                for item in sorted(self.terminals):
                    result += '\''+item+'\''+','
                result = result[:-1]
        result += ']'
        return result

    def to_string_compact(self):
        result = self.left+'->'
        for data in self.right:
            result += data['type']+' '
        return result


class State():
    def __init__(self, name):
        self.name = name
        self.productions = []
        self.string = []

    def to_string(self):
        for production in self.productions:
            if production.to_string() not in self.string:
                self.string.append(production.to_string())
        return "\n".join(sorted(self.string))

    def get_item(self):
        result = []
        for production in self.productions:
            expressions = production.right
            position = production.position
            if position < len(expressions) + 1:
                node = expressions[position - 1]
                if node not in result:
                    result.append(node)
        return result


class DFA():
    def __init__(self):
        self.state = []
        self.edge = []

    def add_state(self, Ix):
        self.state.append(Ix)

    def add_edge(self, Ia, t, Ib):
        self.edge.append((Ia, t, Ib))


'''
词法分析部分开始
'''


def remove_comments(text):  # 去除注释
    comments = re.findall('//.*?\n', text, flags=re.DOTALL)
    if(len(comments) > 0):
        for i in comments:
            text = text.replace(i, "")
    comments = re.findall('/\*.*?\*/', text, flags=re.DOTALL)
    if(len(comments) > 0):
        for i in comments:
            text = text.replace(i, "")
    return text


def scan(line):  # 经行一次扫描，返回得到的token以及剩余的字符串
    global ERROR_TOKEN
    max = ''
    target_regex = regexs[0]
    index_sub = 0
    match = False
    for regex in regexs:
        result = re.findall(regex, line, flags=re.DOTALL)
        if regex == '-?\\d+\\.\\d+?' and result != []:
            for index, i in enumerate(result):
                linesplit = line.split(i)
                for tchar in linesplit[1]:
                    if tchar in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                        i += tchar  # 这个是局部还是全局我不知道
                result[index] = i
        if(len(result) > 0):
            result = result[0]
            index = line.find(result)
            if(index != 0):
                continue
            else:
                if(len(result) > len(max)):
                    match = True
                    max = result
                    target_regex = regex
    if(match == False):  # 出错处理
        print(u"非法字符："+line[0])
        ERROR_TOKEN = line[0]
        exit(1)
        return {"data": line[0], "regex": None, "remain": line[1:]}
    else:
        return {"data": max, "regex": target_regex, "remain": line[index_sub+len(max):]}


def scan_line(line):  # 对一行进行重复扫描，获得一组token
    tokens = []
    result = line.strip().strip('\t')
    origin = result
    while True:
        if result == "":
            break
        before = result
        result = scan(result)
        if result['regex']:
            token = {}
            token['class'] = "T"
            token['row'] = CURRENT_LINE
            token['colum'] = origin.find(before)+1
            token['name'] = type[regexs.index(result['regex'])].upper()
            token['data'] = result['data']
            token['type'] = token['name']
            if result['data'] in reserved:  # 保留字，对应文法中->不加引号，认定为终结符
                token['name'] = reserved[result['data']].lower()
                token['type'] = token['name']
            if token['name'] == "operator".upper() or token['name'] == "seperator".upper():
                # 操作符或者界符，对应文法中->加引号，认定为终结符
                token['type'] = token['data']
            if token['name'] == "int" and token['type'] != "int":
                token['data'] = int(token['data'])
            if token['name'] == "float" and token['type'] != "float":
                token['data'] = float(token['data'])
            if token['name'] == "INT" or token['name'] == "FLOAT":
                # 整数与浮点数统一
                token['type'] = 'number'
            tokens.append(token)
        result = result['remain'].strip().strip('\t')
        if (result == ""):
            return tokens
    return tokens


'''
函数名：generate_tokens(path, type, datastr)
函数功能：根据测试数据和正则表达式匹配规则生成tokens词表
输入参数：path：测试文件路径，type：测试方式，datastr：测试数据
输出参数：tokens返回的tokens列表
'''


def generate_tokens(path, type, datastr):
    if type == 0:
        fd = open(path, 'r')
        lines = remove_comments(fd.read()).split('\n')
    else:
        lines = remove_comments(datastr).split('\n')
    # with io.open(path,'w',encoding="utf-8")as f:
    #     for line in lines:
    #         f.write(line.strip().strip('\t')+'\n')
    tokens = []
    for line in lines:
        tokens_temp = scan_line(line)
        tokens += tokens_temp
        global CURRENT_LINE
        CURRENT_LINE += 1
    return tokens


def read_grammer_from_json(path):  # 从json读取LR(1)文法产生式
    global PRODUCTION_GROUP
    global TERMINAL_SYMBOL_GROUP
    global NONE_TERMINAL_SYMBOL_GROUP
    global START_PRODUCTION
    TERMINAL_SYMBOL_GROUP.append({'class': 'T', 'type': '#'})
    START_PRODUCTION = Production(
        'S', [{'class': 'NT', 'type': 'start'}], 1, terminals=['#'])
    PRODUCTION_GROUP.append(START_PRODUCTION)
    path = path.replace('\\', '/')
    fd = io.open(path, "r", encoding="utf-8")
    data = fd.read()
    grammer = json.loads(data)
    for none_terminal in grammer:
        if none_terminal not in NONE_TERMINAL_SYMBOL_GROUP:
            NONE_TERMINAL_SYMBOL_GROUP.append(none_terminal)
        group = grammer[none_terminal]
        for expressions in group:
            production_temp = Production(
                none_terminal, expressions, terminals=['#'])
            PRODUCTION_GROUP.append(production_temp)
            for item in expressions:
                if item['class'] != 'NT':
                    if not item in TERMINAL_SYMBOL_GROUP:
                        TERMINAL_SYMBOL_GROUP.append(item)


def print_grammer(PRODUCTION_GROUP):  # 打印读取的文法
    for production in PRODUCTION_GROUP:
        print(production.to_string_compact())


def add_dot_to_productions(production):  # 对产生式加点
    result = []
    if len(production.right) == 1 and production.right[0]['type'] == '$':
        result.append(Production(production.left, production.right, 1))
    else:
        productions_temp = [Production(production.left, production.right, i + 1)
                            for i in range(len(production.right) + 1)]
        for item in productions_temp:
            result.append(item)
    return result


def generate_doted_productions():  # 获得所有加点的产生式
    global PRODUCTION_GROUP_DOTED
    for production in PRODUCTION_GROUP:
        for item in add_dot_to_productions(production):
            PRODUCTION_GROUP_DOTED.append(item)


def find_production(none_terminal):  # 在所有加点的产生式中，找到其中左侧非终结符为NT的
    result = []
    for production in PRODUCTION_GROUP_DOTED:
        if production.left == none_terminal:
            result.append(production)
    return result


def get_closure(productions):  # 求一个项目集的CLOSURE
    def expand_production(production):
        data = []
        right = production.right
        position = production.position
        terminals = production.terminals

        def get_first_set_final(node):
            if node['class'] == 'NT':
                return FIRST[next['type']]
            else:
                return get_first_set(next['type'])
        if position < len(right) + 1 and right[position - 1]['class'] == 'NT':
            first = []
            flag = True
            for i in range(position, len(right)):
                next = right[i]
                first_set = copy.deepcopy(get_first_set_final(next))
                terminal_end = {'class': 'T', 'type': '$'}
                if terminal_end in first_set:
                    first_set.remove(terminal_end)
                    for item in first_set:
                        if not item in first:
                            first.append(item)
                else:
                    for item in first_set:
                        if not item in first:
                            first.append(item)
                    flag = False
                    break
            if flag:
                for item in terminals:
                    if not item in first:
                        first.append({'class': 'T', 'type': item})
            productions = find_production(right[position - 1]['type'])
            for item in productions:
                if item.position == 1:
                    temp = copy.deepcopy(item)
                    temp.terminals = [item['type'] for item in first]
                    data.append(temp)
        return data
    productions_string_group = set(production.to_string()
                                   for production in productions)
    result = [production for production in productions]
    procession = [production for production in productions]
    while len(procession) > 0:
        production = procession.pop()
        data = expand_production(production)
        for item in data:
            if item.to_string() not in productions_string_group:
                result.append(item)
                productions_string_group.add(item.to_string())
                procession.append(item)
    return result


def get_go(State, item):  # 求一个项目集对于item的GO
    params = []
    for production in State.productions:
        expressions = production.right
        position = production.position
        if position < len(expressions)+1:
            node = expressions[position-1]
            if node['type'] == '$' and len(expressions) == 1:
                continue
            if node == item and production.next_doted_production() not in params:
                params.append(production.next_doted_production())
    return get_closure(params)


def get_first_set(symbol):  # 初步获取First集
    global FIRST
    result = []
    productions = [
        production for production in PRODUCTION_GROUP if production.left == symbol]
    if len(productions) == 0:
        return [{'class': 'T', 'type': symbol}]
    terminal_end = {'class': 'T', 'type': '$'}
    for production in productions:
        expressions = production.right
        if expressions == [terminal_end] and terminal_end not in result:
            result.append(terminal_end)
        else:
            count = len(expressions)
            if expressions[0]['class'] == 'T' and expressions[0] not in result:
                result.append(expressions[0])
                continue
            else:
                if expressions[0]['type'] != symbol:
                    temp_first = expressions[0]
                    if temp_first not in result:
                        result.append(temp_first)
            if count > 1:
                previous = expressions[0]
                for i in range(1, count):
                    if previous['type'] != symbol:
                        if not terminal_end in get_first_set(previous['type']):
                            break
                        else:
                            if expressions[i]['type'] != symbol:
                                temp_first = get_first_set(
                                    expressions[i]['type'])
                                if temp_first not in result:
                                    result.append(temp_first[0])
                                previous = expressions[i]
    FIRST[symbol] = result
    return result


def make_up_first():  # 补全Fisrt集
    def is_first_set_complete(key):
        first = FIRST[key]
        for item in first:
            if item['class'] == 'NT':
                return False
        return True
    global FIRST
    procession = list(FIRST.keys())
    while len(procession) > 0:
        for key in procession:
            first = FIRST[key]
            for item in first:
                if item['class'] == 'NT':
                    if is_first_set_complete(item['type']):
                        for value in FIRST[item['type']]:
                            if value not in first:
                                first.append(value)
                        first.remove(item)
            if is_first_set_complete(key):
                procession.remove(key)
    return


def generate_first():  # 产生First集
    for none_terminal in NONE_TERMINAL_SYMBOL_GROUP:
        get_first_set(none_terminal)
    make_up_first()
    return


def generate_dfa():  # 构造LR(1)项目集规范族的DFA
    global dfa

    def merge(productions):
        result = []
        table = {}
        reversed = {}
        for production in productions:
            production_temp = Production(
                production.left, production.right, production.position)
            teiminals = production.terminals
            if not production_temp.to_string() in table:
                table[production_temp.to_string()] = teiminals
                reversed[production_temp.to_string()] = production_temp
            else:
                for teiminal in teiminals:
                    table[production_temp.to_string()].append(teiminal)
        for key in table:
            production_temp = reversed[key]
            production_temp.terminals = table[key]
            result.append(production_temp)
        return result
    state_table = {}
    tranfer = []
    current_state = 0
    states = []
    procession = []
    state_top = State('I'+str(current_state))
    state_top.productions = get_closure([START_PRODUCTION])
    state_table[state_top.name] = state_top.to_string()
    procession.append(state_top)
    dfa.add_state(state_top)
    states.append(state_top)
    current_state += 1
    while len(procession) > 0:
        state_top = procession.pop(0)
        items = state_top.get_item()
        for item in items:
            state_temp = State('I'+str(current_state))
            state_temp.productions = merge(get_go(state_top, item))
            state_string = state_temp.to_string()
            if state_string == '':
                continue
            if state_string not in state_table.values():
                states.append(state_temp)
                state_table[state_temp.name] = state_string
                dfa.add_state(state_temp)
                dfa.add_edge(state_top, item, state_temp)
                tranfer.append((state_top.name, item['type'], state_temp.name))
                procession.append(state_temp)
                current_state += 1
            else:
                for state in states:
                    if state_table[state.name] == state_string:
                        dfa.add_edge(state_top, item, state)
                        tranfer.append(
                            (state_top.name, item['type'], state.name))
                        break
    return


def search_go_to_state(state, target):  # 查找GO(I,X)所到达的项目集
    for tuple in dfa.edge:
        state_from, item, state_to = tuple
        if (state_from, item) == (state, target):
            return state_to
    return


def generate_table():  # 生成LR(1)分析表
    global ACTION
    global GOTO
    global STATE_INDEX_TABLE
    global TERMINAL_INDEX_TABLE
    global NONE_TERMINAL_INDEX_TABLE
    global REDUCE
    global SHIFT
    states = dfa.state
    edges = dfa.edge
    production_string_group = copy.deepcopy(PRODUCTION_GROUP)
    production_string_group[0].position = 0
    production_string_group = [production.to_string()
                               for production in production_string_group]
    STATE_INDEX_TABLE = {states[i].name: i for i in range(len(states))}
    TERMINAL_INDEX_TABLE = {
        TERMINAL_SYMBOL_GROUP[i]["type"]: i for i in range(len(TERMINAL_SYMBOL_GROUP))}
    NONE_TERMINAL_INDEX_TABLE = {NONE_TERMINAL_SYMBOL_GROUP[i]: i for i in range(
        len(NONE_TERMINAL_SYMBOL_GROUP))}
    ACTION = [[" " for x in range(len(TERMINAL_SYMBOL_GROUP))]
              for y in range(len(states))]
    GOTO = [[" " for x in range(len(NONE_TERMINAL_SYMBOL_GROUP))]
            for y in range(len(states))]
    for state in states:
        x = STATE_INDEX_TABLE[state.name]
        production_end = copy.deepcopy(START_PRODUCTION)
        production_end.position += 1
        lable_group = [production.to_string()
                       for production in state.productions]
        if production_end.to_string() in lable_group:
            y = TERMINAL_INDEX_TABLE["#"]
            ACTION[x][y] = 'acc'
            continue
        for production in state.productions:
            expressions = production.right
            position = production.position
            if position < len(expressions) + 1:
                node = expressions[position - 1]
                if node['class'] == 'T':
                    y = TERMINAL_INDEX_TABLE[node["type"]]
                    state_to = search_go_to_state(state, node)
                    if node['type'] != '$':
                        table_item_name = 's'+state_to.name[1:]
                        if ACTION[x][y] != "" and ACTION[x][y] != table_item_name:
                            pass
                        ACTION[x][y] = table_item_name
                        production_temp = copy.deepcopy(production)
                        production_temp.position = 0
                        production_temp.terminals = ('#')
                        SHIFT[table_item_name] = production_temp
                    else:
                        for i in range(len(production.terminals)):
                            y = TERMINAL_INDEX_TABLE[production.terminals[i]]
                            production_temp = copy.deepcopy(production)
                            production_temp.position = 0
                            production_temp.terminals = ('#')
                            table_item_name = 'r' + \
                                str(production_string_group.index(
                                    production_temp.to_string()))
                            if ACTION[x][y] != "" and ACTION[x][y] != table_item_name:
                                pass
                            ACTION[x][y] = table_item_name
                            REDUCE[table_item_name] = production_temp
            elif position == len(expressions) + 1:
                for i in range(len(production.terminals)):
                    y = TERMINAL_INDEX_TABLE[production.terminals[i]]
                    production_temp = copy.deepcopy(production)
                    production_temp.position = 0
                    production_temp.terminals = ('#')
                    table_item_name = 'r' + \
                        str(production_string_group.index(
                            production_temp.to_string()))
                    if ACTION[x][y] != "" and ACTION[x][y] != table_item_name:
                        pass
                    ACTION[x][y] = table_item_name
                    REDUCE[table_item_name] = production_temp
    for tuple in edges:
        state_from, item, state_to = tuple
        if item['class'] == 'NT':
            x = STATE_INDEX_TABLE[state_from.name]
            y = NONE_TERMINAL_INDEX_TABLE[item['type']]
            if GOTO[x][y] != "" and GOTO[x][y] != state_to.name:
                pass
            GOTO[x][y] = state_to.name
    return


def write_to_table():  # 将LR(1)分析表写入文件
    title = [""]
    for i in range(len(TERMINAL_SYMBOL_GROUP)):
        title.append(TERMINAL_SYMBOL_GROUP[i]['type'])
    for i in range(len(NONE_TERMINAL_SYMBOL_GROUP)):
        title.append(NONE_TERMINAL_SYMBOL_GROUP[i])
    x = [title]
    for i in range(len(dfa.state)):
        row = [dfa.state[i].name]
        for j in range(len(TERMINAL_SYMBOL_GROUP)):
            row.append(ACTION[i][j])
        for j in range(len(NONE_TERMINAL_SYMBOL_GROUP)):
            row.append(GOTO[i][j])
        x.append(row)
    with open(os.path.join(SOURCE_PATH, NAME_LR1), 'w') as fd:
        for row in x:
            for colum in row:
                fd.write(colum + '\t')
            fd.write('\n')
    return


def add_table_colum(operation, action, state):
    global RECORD_TABLE
    global CURRENT_STEP
    global stackTB
    CURRENT_STEP += 1
    op_stack_column = ""
    tokens_column = ""
    if len([x['type'] for x in OP_STACK]) > 5:
        op_stack_column = "...... "
    op_stack_column += " ".join([x['type'] for x in OP_STACK][-5:])
    tokens_column += " ".join([x['type'] for x in TOKENS][:5])
    if len([x['type'] for x in TOKENS]) > 5:
        tokens_column += " ......"
    state_stack_column = " ".join([x.name for x in STATE_STACK])
    row = [str(CURRENT_STEP), op_stack_column, tokens_column,
           operation, state_stack_column, action, state]
    obj = {
        "步骤": str(CURRENT_STEP),
        "当前栈": op_stack_column,
        "输入串": tokens_column,
        "动作": operation,
        "状态栈": state_stack_column,
        "ACTION": action,
        "GOTO": state
    }
    RECORD_TABLE.append(row)
    stackTB.append(obj)
    return


def disp_exp(expression):
    left = expression.left
    right = expression.right
    print('left: ', end='')
    print(left)
    print('right: ', end='')
    print(right)


def start_analyse():  # 进行语法分析
    global OP_STACK
    global STATE_STACK
    global CURRENT_PRODUCTION
    global RECORD_TABLE
    global TOKENS
    global ERROR_MSG
    title = ["步骤", "当前栈", "输入串", "动作", "状态栈", "ACTION", "GOTO"]
    RECORD_TABLE = [title]

    def find_state_by_name(name):
        for state in dfa.state:
            if state.name == name:
                return state
    terminal_end = {'class': 'T', 'type': '#'}
    OP_STACK = [terminal_end]
    STATE_STACK = [dfa.state[0]]
    ERROR_MSG = []
    while True:
        current_state = STATE_STACK[-1]
        if len(TOKENS) == 0:
            token = terminal_end
        else:
            token = TOKENS[0]
        x = STATE_INDEX_TABLE[current_state.name]
        y = TERMINAL_INDEX_TABLE[token['type']]
        # x表示当前状态，yvia哦是当前接收到的字符，然后查询action表格就知道接下来应该去哪里了
        action = ACTION[x][y]
        # if action[0] == 's':
        #     print('当前操作为移入，移入的字符为：name:'+token['name']+' data:'+token['data'])
        # else:
        #     print('当前操作为规约：')
        if action == ' ':
            print("wrong")
            return 1
            # exit(1)
        if action == 'acc':
            operation = "accept"
            add_table_colum(operation, action, "")
            with open(os.path.join(SOURCE_PATH, NAME_ANALYSIS), 'w') as fd:
                for row in RECORD_TABLE:
                    for colum in row:
                        fd.write(colum + '\t')
                    fd.write('\n')
            break
        elif action[0] == 's':  # 表示移进的状态
            next_state = find_state_by_name(
                'I'+action[1:])  # 比如是s4，那么就是下一个进入到’4‘号状态了
            # disp_exp(next_state.productions[0])
            STATE_STACK.append(next_state)  # 下一个状态，入栈
            token_temp = TOKENS.pop(0)  # 从tokens里面读取下一个字符
            OP_STACK.append(token_temp)  # 放入OP_STACK当中存储接下来的字符
            operation = "shift"
            add_table_colum(operation, action, "")
            # row = [str(CURRENT_STEP), op_stack_column, tokens_column, operation, state_stack_column, action, state]
        elif action[0] == 'r':
            CURRENT_PRODUCTION = REDUCE[action]
            try:
                semantic_analysis()
            except:
                global INTERMEDIATE_CODE
                INTERMEDIATE_CODE=[('','','','')]
                return 1
            count = len(CURRENT_PRODUCTION.right)
            if count == 1 and CURRENT_PRODUCTION.right[0]['type'] == '$':
                symbol_destination = {'class': 'NT',
                                      'type': CURRENT_PRODUCTION.left}
                current_state = STATE_STACK[-1]
                temp_state = search_go_to_state(
                    current_state, symbol_destination)
                STATE_STACK.append(search_go_to_state(
                    current_state, symbol_destination))
                OP_STACK.append(symbol_destination)
                production_temp = copy.deepcopy(CURRENT_PRODUCTION)
                production_temp.position = 0
                operation = "reduce({})".format(production_temp.to_string())
                add_table_colum(operation, action, temp_state.name)
                continue
            for i in range(count):
                item = CURRENT_PRODUCTION.right[count - i - 1]
                back = OP_STACK[-1]
                if item['class'] != back['class'] and item['type'] != back['type']:
                    print("error in parser place row:{},colum{}".format(
                        token['row'], token['colum']))
                    # exit(-1)
                    return 1
                else:
                    OP_STACK.pop(-1)
                    STATE_STACK.pop(-1)
            current_state = STATE_STACK[-1]
            none_terminal = CURRENT_PRODUCTION.left
            x = STATE_INDEX_TABLE[current_state.name]
            y = NONE_TERMINAL_INDEX_TABLE[none_terminal]
            next_state = find_state_by_name(GOTO[x][y])
            STATE_STACK.append(next_state)
            OP_STACK.append({'class': 'NT', 'type': none_terminal})
            production_temp = copy.deepcopy(CURRENT_PRODUCTION)
            production_temp.position = 0
            operation = "reduce({})".format(production_temp.to_string())
            add_table_colum(operation, action, next_state.name)
    return 0


def get_new_label():  # 生成一个新的lable
    global CURRENT_LABLE
    CURRENT_LABLE += 1
    return "l"+str(CURRENT_LABLE)


def get_new_function_lable():  # 生成一个新的函数lable
    global CURRENT_FUNCTION
    CURRENT_FUNCTION += 1
    return "f"+str(CURRENT_FUNCTION)


def get_new_temp():  # 生成一个新的中间变量lable
    global CURRENT_TEMP
    CURRENT_TEMP += 1
    return "t"+str(CURRENT_TEMP)


'''
工具函数
'''


def find_symbol(name, function):  # 根据所在函数及标识符，找到符号表中的符号
    for item in SYMBOL_TABLE:
        # print(item.name, "function", item.function, "type", item.type)
        if item.name == name and (item.function == function or item.function == 'global'):
            return item
    return None


def printSymbolTable():
    for item in SYMBOL_TABLE:
        print("Symbol: ", item.name, "Function ",
              item.function, "Type: ", item.type)


def update_symbol_table(symbol):  # 更新或者插入符号表
    global SYMBOL_TABLE
    for item in SYMBOL_TABLE:
        if item.name == symbol.name and item.function == symbol.function:
            SYMBOL_TABLE.remove(item)
            break
    SYMBOL_TABLE.append(symbol)


def find_function_by_name(name):  # 根据函数名找到函数表中的函数
    for item in FUNCTION_TABLE:
        if item.name == name:
            return item
    return None


def update_function_table(symbol):  # 更新或者插入函数表
    global FUNCTION_TABLE
    for item in FUNCTION_TABLE:
        print("func ", item.name)
        if item.name == symbol.name:
            FUNCTION_TABLE.remove(item)
            break
    FUNCTION_TABLE.append(symbol)


def printNode(node):
    print("place: {}".format(node.place))
    print("code: {}".format(node.code))
    print("stack: {}".format(node.stack))
    print("name: {}".format(node.name))
    print("type: {}".format(node.type))
    print("data: {}".format(node.data))


def disp_SEMANTIC_STACK_stack(stack, level):
    for i in stack:
        print(level*'   '+'{')
        if i.name:
            print((level+1)*'   '+'name: '+i.name)
        try:
            print((level+1) * '   '+'id: ' + i.id)
        except:
            pass
        try:
            print((level+1) * '   ' + 'data: ' + i.data)
        except:
            pass
        if len(i.stack) != 0:
            disp_SEMANTIC_STACK_stack(i.stack, level+1)
        print(level * '   ' + '}')


def stack_disp_top():
    print('-------stack-------')
    disp_SEMANTIC_STACK_stack(SEMANTIC_STACK, 0)
    print('-------------------')


def write_my_intermediate_code():  # 将中间代码写入文件(用于测试)
    with open(r"./source_file/middle.txt", 'w') as f:
        for i in INTERMEDIATE_CODE:
            f.write(str(i)+'\n')


####################################################################
# 定义与error有关的东西
ERROR_MSG = []
FATAL_ERROR_FLAG = 0


def error_Handler_RedefinedSymbol(nodename, token):  # 重定义处理
    global ERROR_MSG
    msg = "Error at line {}: multiple defination of symbol: {}".format(
        token['row']-1, nodename)
    print(msg)
    ERROR_MSG.append(msg)


def error_Handler_RedefinedFunction(func, token):  # 重定义处理
    global ERROR_MSG
    global FATAL_ERROR_FLAG
    msg = "Error at line {}: multiple defination of function: {}".format(
        token['row'], func.name)
    print(msg)
    FATAL_ERROR_FLAG = 1
    ERROR_MSG.append(msg)


def error_Handler_RedefinedFunctionNoLineNum(funcName):  # 重定义处理
    global ERROR_MSG
    msg = "Error: multiple defination of function: {}".format(funcName)
    print(msg)
    ERROR_MSG.append(msg)


def error_Handler_UndefinedSymbol(id, token):
    global ERROR_MSG
    msg = "Error at line {}: can't find defination of symbol: {}".format(
        token['row'], id)
    print(msg)
    ERROR_MSG.append(msg)


def error_Handler_UndefinedFunction(funcName, token):
    global ERROR_MSG
    msg = "Error at line {}: can't find defination of function: {}".format(
        token['row'], funcName)
    print(msg)
    ERROR_MSG.append(msg)


def error_Handler_TypeError(token):
    global ERROR_MSG
    msg = ("Error at line {}: type error".format(token['row']-1))
    print(msg)
    ERROR_MSG.append(msg)


def error_Handler_ArithmeticTypeError(left, right, token):
    global ERROR_MSG
    if left.type == 'int' and right.type == 'int':
        return
    elif left.type == 'float' and right.type == 'float':
        return
    elif left.type == 'char' and right.type == 'chae':
        return
    else:
        msg = ("Warning at line {}: Left Type: {} doesn't match with the Right Type: {}".format(
            token['row'], left.type, right.type))
        print(msg)
        ERROR_MSG.append(msg)


def error_Handler_FunctionCallArgumentNumber(function, given, token):
    global ERROR_MSG
    msg = ("Error at line {}: function {} takes {} arguments, but received {}".format(
        token['row'], function.name, len(function.params), len(given)))
    print(msg)
    ERROR_MSG.append(msg)


def error_Handler_FunctionCallArgumentType(function, given, token, index):
    global ERROR_MSG
    msg = ("Error at line {}: function {}()'s argument {} is of type {}, but {} was given".format(
        token['row'], function.name, function.params[index][0], function.params[index][1], given.type))
    print(msg)
    ERROR_MSG.append(msg)

#######################################################
# 语义分析部分
#######################################################


def semantic_analysis():  # 语义分析子程序
    global CURRENT_OFFSET
    global CURRENT_FUNCTION_SYMBOL
    global SEMANTIC_STACK
    global FATAL_ERROR_FLAG
    if FATAL_ERROR_FLAG == 1:
        return
    none_terminal = CURRENT_PRODUCTION.left
    expressions = CURRENT_PRODUCTION.right
    # disp_exp(CURRENT_PRODUCTION)
    # if(len(TOKENS) > 0):
    #     print("now token:"+TOKENS[0]['name']+' '+TOKENS[0]['data'])
    #     print('none_terminal: '+none_terminal)
    # stack_disp_top()
    if none_terminal == 'operator':
        node_new = Node()
        node_new.name = 'operator'
        node_new.type = ''
        for i in range(len(expressions)):
            token = OP_STACK[-(len(expressions) - i)]
            node_new.type += token['type']
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'assignment_operator':
        node_new = Node()
        node_new.name = 'assignment_operator'
        node_new.type = []
        for i in range(len(expressions)):
            node_new.type.append(expressions[i]['type'])
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'type_specifier':
        node_new = Node()
        node_new.name = 'type_specifier'
        node_new.type = expressions[0]['type']
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'primary_expression':
        node_new = Node()
        if expressions[0]['type'] == 'IDENTIFIER':
            node_new.data = OP_STACK[-1]['data']
            node_temp = find_symbol(
                node_new.data, CURRENT_FUNCTION_SYMBOL.lable)
            node_new.place = node_temp.place
            node_new.type = node_temp.type
        elif expressions[0]['type'] == 'number':
            node_new.data = OP_STACK[-1]['data']
            node_new.type = OP_STACK[-1]['name'].lower()
        elif expressions[1]['type'] == 'expression':
            node_new = copy.deepcopy(SEMANTIC_STACK.pop(-1))
        node_new.name = 'primary_expression'
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'arithmetic_expression':
        node_new = Node()
        node_new.name = 'arithmetic_expression'
        if len(expressions) == 1:
            node_new.stack = []
        else:
            node_new = copy.deepcopy(SEMANTIC_STACK.pop(-1))
            node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
            node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'constant_expression':  # ! 错误类型7：操作数类型不匹配或操作数类型与操作符不匹配
        node_new = SEMANTIC_STACK.pop(-1)
        node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
        node_new.name = 'constant_expression'
        if len(node_new.stack) == 1:
            node_new = copy.deepcopy(node_new.stack[0])
        else:
            node_left = node_new.stack.pop(0)
            while len(node_new.stack) > 0:
                node_op = node_new.stack.pop(0)
                node_right = node_new.stack.pop(0)
                #! handle possible type error: Start
                token = TOKENS[0]
                error_Handler_ArithmeticTypeError(node_left, node_right, token)
                #! handle possible type error: End
                if node_left.place == None:
                    arg1 = node_left.data
                else:
                    arg1 = node_left.place
                if node_right.place == None:
                    arg2 = node_right.data
                else:
                    arg2 = node_right.place
                if len(node_left.code) > 0:
                    for code in node_left.code:
                        node_new.code.append(code)
                if len(node_right.code) > 0:
                    for code in node_right.code:
                        node_new.code.append(code)
                node_result = Node()
                node_result.name = 'primary_expression'
                node_result.place = get_new_temp()
                node_result.type = node_right.type
                code = (node_op.type, arg1, arg2, node_result.place)
                node_new.code.append(code)
                node_left = node_result
                node_new.type = node_right.type
            node_new.place = node_new.code[-1][3]
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'declaration_assign':
        node_new = Node()
        if len(expressions) == 2:  # 内涵赋值语句
            id = OP_STACK[-3]['data']
            node_new = SEMANTIC_STACK.pop(-1)
            node_new.id = id
        else:  # 内不含赋值语句，直接一个声明
            id = OP_STACK[-1]['data']
            node_new.id = id
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'declaration_init':
        node_new = SEMANTIC_STACK.pop(-1)
        node_new.name = 'declaration_init'
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'declaration_init_list':
        node_new = Node()
        node_new.name = 'declaration_init_list'
        if len(expressions) == 1:
            node_new.stack = []
        else:
            node_new = SEMANTIC_STACK.pop(-1)
            node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'declaration':  # ! 错误类型3：变量出现重复定义，错误类型5：赋值号两边的表达式类型不匹配。
        node_new = SEMANTIC_STACK.pop(-1)
        node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
        node_new.name = 'declaration'
        type = SEMANTIC_STACK.pop(-1).type
        for node in node_new.stack:
            symbol = find_symbol(node.id, CURRENT_FUNCTION_SYMBOL.lable)
            if symbol != None and symbol.function == CURRENT_FUNCTION_SYMBOL.lable:
                token = TOKENS[0]
                # print("multiple defination of {} in row{}".format(node.id,token['row']))
                # ! handle multiple defination of variable: Start
                error_Handler_RedefinedSymbol(node.id, token)
                # ! handle multiple defination of variable: End
            else:
                symbol = Symbol()
            if node.place == None:
                symbol.name = node.id
                symbol.place = get_new_temp()
                symbol.type = type
                symbol.function = CURRENT_FUNCTION_SYMBOL.lable
                symbol.size = 4
                symbol.offset = CURRENT_OFFSET
                CURRENT_OFFSET += symbol.size
                update_symbol_table(symbol)
                if node.data != None:
                    if(node.type != type):
                        token = TOKENS[0]
                        # print("type error in row{}".format(token['row']))
                        # ! Handle type error: Start
                        error_Handler_TypeError(token)
                        # ! Handle type error: End
                    code = (':=', node.data, '_', symbol.place)
                    node_new.code.append(code)
            else:
                symbol.name = node.id
                symbol.place = node.place
                symbol.type = type
                symbol.function = CURRENT_FUNCTION_SYMBOL.lable
                symbol.size = 4
                symbol.offset = CURRENT_OFFSET
                CURRENT_OFFSET += symbol.size
                update_symbol_table(symbol)
                for code in node.code:
                    node_new.code.append(code)
        node_new.stack = []
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'assignment_expression':  # ! 错误类型 1 ：变量在使用时未经定义。错误类型5：赋值号两边的表达式类型不匹配。
        node_new = SEMANTIC_STACK.pop(-1)
        node_op = SEMANTIC_STACK.pop(-1)
        id = OP_STACK[-3]['data']
        symbol = find_symbol(id, CURRENT_FUNCTION_SYMBOL.lable)
        if symbol == None:
            token = TOKENS[0]
            # print("none defination of {} in row{}".format(id, token['row']))
            # ! Handle undefined symbol: Start
            error_Handler_UndefinedSymbol(id, token)
            # ! Handle undefined symbol: End
            symbol = Symbol()
            symbol.place = get_new_temp()
            symbol.name = id
            symbol.type = node_new.type
            symbol.function = CURRENT_FUNCTION_SYMBOL.lable
            symbol.size = 4
            symbol.offset = CURRENT_OFFSET
            CURRENT_OFFSET += symbol.size
            update_symbol_table(symbol)
            # ! Handle type error: Start
            if node_new.type != symbol.type:
                token = TOKENS[0]
                error_Handler_TypeError(token)
            # ! Handle type error: End
        if node_new.place == None:
            arg = node_new.data
        else:
            arg = node_new.place
        if len(node_op.type) == 1:
            code = (':=', arg, '_', symbol.place)
            node_new.code.append(code)
        else:
            code = (node_op.type[0], symbol.place, arg, symbol.place)
            node_new.code.append(code)
        node_new.name = 'assignment_expression'
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'assignment_expression_profix':
        node_new = Node()
        node_new.name = 'assignment_expression_profix'
        if len(expressions) == 1:
            node_new.stack = []
        else:
            node_new = SEMANTIC_STACK.pop(-1)
            node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'assignment_expression_list':
        node_new = Node()
        node_new.name = 'assignment_expression_list'
        if len(expressions) == 1:
            node_new.stack = []
        else:
            node_new = SEMANTIC_STACK.pop(-1)
            node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
            for node in node_new.stack:
                for code in reversed(node.code):
                    node_new.code.insert(0, code)
            node_new.stack = []
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'expression':
        node_new = SEMANTIC_STACK.pop(-1)
        node_new.name = 'expression'
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'expression_profix':
        node_new = Node()
        node_new.name = 'expression_profix'
        if len(expressions) == 1:
            node_new.stack = []
        else:
            node_new = SEMANTIC_STACK.pop(-1)
            node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'expression_list':
        node_new = Node()
        node_new.name = 'expression_list'
        if len(expressions) == 1:
            node_new.stack = []
        else:
            node_new = SEMANTIC_STACK.pop(-1)
            node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
            for node in reversed(node_new.stack):
                for code in node.code:
                    node_new.code.insert(0, code)
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'expression_statement':
        node_new = SEMANTIC_STACK.pop(-1)
        node_new.name = 'expression_statement'
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'statement':
        node_new = SEMANTIC_STACK.pop(-1)
        node_new.name = 'statement'
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'statement_list':
        # origin:
        node_new = Node()
        node_new.name = 'statement_list'
        if len(expressions) == 1:
            node_new.stack = []
            SEMANTIC_STACK.append(node_new)
        else:
            node_new = SEMANTIC_STACK.pop(-1)
            node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
            for node in node_new.stack:
                for code in reversed(node.code):
                    node_new.code.insert(0, code)
            node_new.stack = []
            SEMANTIC_STACK.append(node_new)
        '''
        这个东西我要改一下，因为我觉得之前的东西规约不完就很离谱
        '''
        # node_new = Node()
        # node_new.name = 'statement_list'
        # if len(expressions)==1:
        #     node_new.stack=[]
        #     SEMANTIC_STACK.append(node_new)
        # else:
        #     while(1): # 这里以while循环的方式一次性完成所有statement的规约操作
        #         temp_node = SEMANTIC_STACK[-2]
        #         if temp_node.name!='statement':
        #             break
        #         node_new=SEMANTIC_STACK.pop(-1)
        #         node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
        #         for node in node_new.stack:
        #             for code in reversed(node.code):
        #                 node_new.code.insert(0,code)
        #         node_new.stack=[]
        #         SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'compound_statement':
        # 如果执行到函数最末尾的地方就执行这样的一个操作（当然这个判断并不全面如果完全这样的话并不行），这个也是没有办法的办法了，先就这样吧，就比如说如果定义了两个函数之类的话这个就很麻烦了
        while(len(TOKENS) == 0 or (len(TOKENS) >= 3 and TOKENS[3]['data'] == '(')):
            temp_node = SEMANTIC_STACK[-2]
            if temp_node.name != 'statement':
                break
            node_new = SEMANTIC_STACK.pop(-1)
            node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
            for node in node_new.stack:
                for code in (node.code):  # reversed buyaole
                    node_new.code.insert(0, code)
            node_new.stack = []
            SEMANTIC_STACK.append(node_new)
        node_new = SEMANTIC_STACK.pop(-1)
        node_new.name = 'compound_statement'
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'jump_statement':
        node_new = Node()
        node_new.name = 'jump_statement'
        node_new.type = expressions[0]['type']
        if node_new.type != 'return_statement':  # 虽然不知道为啥，但不append上去确实是没有问题的，还需要经历进一步的检验才行的哈
            node_new.code.append((node_new.type, '_', '_', '_'))
            SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'return_statement':
        node_new = Node()
        node_new.name = 'return_statement'
        node_new.type = expressions[0]['type']
        if len(expressions) == 3:
            node_temp = SEMANTIC_STACK.pop(-1)
            if node_temp.place != None:
                node_result = node_temp.place
            else:
                node_result = node_temp.data
            node_new.code.append((':=', node_result, '_', 'v0'))
        node_new.code.append((node_new.type, '_', '_', '_'))
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'selection_statement':
        node_new = Node()
        node_new.name = 'selection_statement'
        Node.true = get_new_label()
        Node.false = get_new_label()
        Node.end = get_new_label()
        FalseStmt = SEMANTIC_STACK.pop(-1)
        TrueStmt = SEMANTIC_STACK.pop(-1)
        expression = SEMANTIC_STACK.pop(-1)
        for code in expression.code:
            node_new.code.append(code)
        node_new.code.append(('j>', expression.place, '0', Node.true))
        node_new.code.append(('j', '_', '_', Node.false))
        node_new.code.append((Node.true, ':', '_', '_'))
        for code in TrueStmt.code:
            node_new.code.append(code)
        node_new.code.append(('j', '_', '_', Node.end))
        node_new.code.append((Node.false, ':', '_', '_'))
        for code in FalseStmt.code:
            node_new.code.append(code)
        node_new.code.append((Node.end, ':', '_', '_'))
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'iteration_statement':
        node_new = Node()  # 生成新节点
        node_new.name = 'iteration_statement'
        node_new.true = get_new_label()  # 四个分支的入口
        node_new.false = get_new_label()
        node_new.begin = get_new_label()
        node_new.end = get_new_label()
        if expressions[0]['type'] == 'while':
            statement = SEMANTIC_STACK.pop(-1)  # 获得expression结点和statement结点
            expression = SEMANTIC_STACK.pop(-1)
            node_new.code.append((node_new.begin, ':', '_', '_'))  # begin入口
            for code in expression.code:  # 传递expression的中间代码
                node_new.code.append(code)
            # 当expression的计算结果大于0时，跳转到true
            node_new.code.append(('j>', expression.place, '0', node_new.true))
            node_new.code.append(
                ('j', '_', '_', node_new.false))  # 否则，跳转到false
            node_new.code.append((node_new.true, ':', '_', '_'))  # true入口
            for code in statement.code:  # 传递statement的中间代码
                if code[0] == 'break':  # 当中间代码为break时，添加跳转到false的中间代码
                    node_new.code.append(('j', '_', '_', node_new.false))
                elif code[0] == 'continue':  # 当中间代码为continue时，添加跳转到begin的中间代码
                    node_new.code.append(('j', '_', '_', node_new.begin))
                else:
                    node_new.code.append(code)
            node_new.code.append(('j', '_', '_', node_new.begin))  # 跳转回begin
            node_new.code.append((node_new.false, ':', '_', '_'))  # false入口
        elif expressions[0]['type'] == 'for':
            statement = SEMANTIC_STACK.pop(-1)
            assign = SEMANTIC_STACK.pop(-1)
            expression = SEMANTIC_STACK.pop(-1)
            Declaration = SEMANTIC_STACK.pop(-1)
            for code in Declaration.code:
                node_new.code.append(code)
            node_new.code.append((node_new.begin, ':', '_', '_'))
            for code in expression.code:
                node_new.code.append(code)
            node_new.code.append(('j>', expression.place, '0', node_new.true))
            node_new.code.append(('j', '_', '_', node_new.false))
            node_new.code.append((node_new.true, ':', '_', '_'))
            is_continue_existed = False
            for code in statement.code:
                if code[0] == 'break':
                    node_new.code.append(('j', '_', '_', node_new.false))
                elif code[0] == 'continue':
                    node_new.code.append(('j', '_', '_', node_new.end))
                    is_continue_existed = True
                else:
                    node_new.code.append(code)
            if is_continue_existed:
                node_new.code.append((node_new.end, ':', '_', '_'))
            for code in assign.code:
                node_new.code.append(code)
            node_new.code.append(('j', '_', '_', node_new.begin))
            node_new.code.append((node_new.false, ':', '_', '_'))
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'function_declaration':
        node_new = Node()
        node_new.name = 'function_declaration'
        id = OP_STACK[-1]['data']
        node_new.id = id
        node_new.type = SEMANTIC_STACK.pop(-1).type
        node_new.place = get_new_temp()
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'function_declaration_suffix':
        node_new = Node()
        node_new.name = 'function_declaration_suffix'
        if len(expressions) == 1:
            node_new.stack = []
        else:
            node_new = SEMANTIC_STACK.pop(-1)
            node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'function_declaration_list':
        node_new = Node()
        node_new.name = 'function_declaration_list'
        if len(expressions) == 1:
            node_new.stack = []
        else:
            node_new = SEMANTIC_STACK.pop(-1)
            node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
        SEMANTIC_STACK.append(node_new)
        ''' # 这个东西也不对啊，得改，基本上要改的东西得归纳在哪个部分之内的 主要这个void有点离谱。可能暂时也用不到，就先别管了
            "function_declaration_list": [
        [{
            "name": "void",
            "class": "T",
            "type": "void"
        }],
        [{
                "type": "function_declaration",
                "class": "NT"
            },
            {
                "type": "function_declaration_suffix",
                "class": "NT"
            }
        ],
        [{
            "type": "$",
            "class": "T"
        }]
    ],
        '''
    elif none_terminal == 'function_definition':  # ! 函数重复定义
        node_new = SEMANTIC_STACK.pop(-1)
        node_new.name = 'function_definition'
        # ! Handle function_redefinition Start
        tmpfunction = find_function_by_name(OP_STACK[-4]['data'])
        if tmpfunction is not None:
            token = TOKENS[0]
            error_Handler_RedefinedFunction(tmpfunction, token)
        # ! Handle function_redefinition End
        else:
            function = FunctionSymbol()
            function.type = 'int'
            function.name = OP_STACK[-4]['data']
            if function.name == 'main':
                function.lable = 'main'
            else:
                function.lable = get_new_function_lable()
            for arg in node_new.stack:
                symbol = Symbol()
                symbol.name = arg.id
                symbol.type = arg.type
                symbol.place = arg.place
                symbol.function = function.lable
                symbol.size = 4
                symbol.offset = CURRENT_OFFSET
                CURRENT_OFFSET += symbol.size
                update_symbol_table(symbol)
                function.params.append((arg.id, arg.type, arg.place))
            node_new.data = function.lable
            update_function_table(function)
            CURRENT_FUNCTION_SYMBOL = function
            SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'function_implement':
        node_new = SEMANTIC_STACK.pop(-1)
        node_definition = SEMANTIC_STACK.pop(-1)
        node_new.name = 'function_implement'
        code_temp = []
        code_temp.append((node_definition.data, ':', '_', '_'))
        for node in node_definition.stack:
            code_temp.append(
                ('pop', '_', 4*node_definition.stack.index(node), node.place))
        if len(node_definition.stack) > 0:
            code_temp.append(('-', 'fp', 4*len(node_definition.stack), 'fp'))
        for code in reversed(code_temp):
            node_new.code.insert(0, code)
        code_end = node_new.code[-1]
        if code_end[0][0] == 'l':
            lable = code_end[0]
            node_new.code.remove(code_end)
            for code in node_new.code:
                if code[3] == lable:
                    node_new.code.remove(code)
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'function_expression':  # ! 错误类型2：函数在调用时未经定义。错误类型9：函数调用时实参与形参的数目或类型不匹配
        function = find_function_by_name(OP_STACK[-4]['data'])
        #! Error Handling Start
        if function is None:
            token = TOKENS[0]
            error_Handler_UndefinedFunction(OP_STACK[-4]['data'], token)
        else:
            # ! Error Handling End
            node_new = SEMANTIC_STACK.pop(-1)
            node_new.name = 'function_expression'
            code_temp = []
            symbol_temp_list = copy.deepcopy(CURRENT_FUNCTION_SYMBOL.params)
            code_temp.append(('-', 'sp', 4 * len(symbol_temp_list)+4, 'sp'))
            code_temp.append(('store', '_', 4 * len(symbol_temp_list), 'ra'))
            for symbol in symbol_temp_list:
                code_temp.append(
                    ('store', '_', 4 * symbol_temp_list.index(symbol), symbol[2]))
            for code in reversed(code_temp):
                node_new.code.insert(0, code)

            if len(function.params) > 0:
                node_new.code.append(('+', 'fp', 4*len(function.params), 'fp'))
            #! Error Handling Start
                if len(function.params) != len(node_new.stack):
                    token = TOKENS[0]
                    error_Handler_FunctionCallArgumentNumber(
                        function, node_new.stack, token)
                for arg in node_new.stack:
                    index = node_new.stack.index(arg)
                    symbol = find_symbol(
                        arg.data, CURRENT_FUNCTION_SYMBOL.lable)
                    # print(function.params[index])
                    if symbol != None:
                        if symbol.type != function.params[index][1]:
                            print("Symbol ", symbol)
                            print("Symbol type", symbol.type)
                            print("arg.data ", arg.data)
                            print("CURRENT_FUNCTION_SYMBOL.lable ",
                                  CURRENT_FUNCTION_SYMBOL.lable)
                            token = TOKENS[0]
                            error_Handler_FunctionCallArgumentType(
                                function, symbol, token, index)
            #! Error Handling End
            for node in node_new.stack:
                if node.place != None:
                    node_result = node.place
                else:
                    node_result = node.data
                node_new.code.append(
                    ('push', '_', 4*node_new.stack.index(node), node_result))
            node_new.code.append(('call', '_', '_', function.lable))

            symbol_temp_list.reverse()
            for symbol in symbol_temp_list:
                node_new.code.append(
                    ('load', '_', 4 * symbol_temp_list.index(symbol), symbol[2]))
            node_new.code.append(
                ('load', '_', 4 * len(symbol_temp_list), 'ra'))
            node_new.code.append(
                ('+', 'sp', 4 * len(CURRENT_FUNCTION_SYMBOL.params) + 4, 'sp'))

            node_new.place = get_new_temp()
            node_new.code.append((':=', 'v0', '_', node_new.place))
            SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'external_declaration':
        node_new = Node()
        node_new.name = 'external_declaration'
        # if FLAG ==1 :
        #     return
        if len(expressions) == 1:
            node_new.stack = []
            SEMANTIC_STACK.append(node_new)
        else:
            node_new = SEMANTIC_STACK.pop(-1)
            node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
            for node in node_new.stack:
                for code in reversed(node.code):  # reversed
                    node_new.code.insert(0, code)
            node_new.stack = []
            SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'start':
        node_new = Node()
        node_new.name = 'start'
        if len(expressions) == 1:
            node_new.stack = []
        else:
            node_new = SEMANTIC_STACK.pop(-1)
            node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
            for node in node_new.stack:
                for code in reversed(node.code):
                    node_new.code.insert(0, code)
            node_new.stack = []
        SEMANTIC_STACK.append(node_new)
    # newly added
    elif none_terminal == 'PPT_declaration_class':
        if expressions[0]['type'] == 'PPT_variable_declaration':
            node_new = Node()
            symbol = Symbol()
            symbol.place = get_new_temp()
            id = OP_STACK[-2]['data']
            symbol.name = id
            symbol.type = 'int'
            symbol.function = 'global'  # CURRENT_FUNCTION_SYMBOL.lable
            symbol.size = 4
            symbol.offset = CURRENT_OFFSET
            CURRENT_OFFSET += symbol.size
            # ! Error Handling Start
            tmpsymbol = find_symbol(symbol.name, 'global')
            if tmpsymbol != None and tmpsymbol.function == 'global':
                token = TOKENS[0]
                # ! handle multiple defination of variable: Start
                error_Handler_RedefinedSymbol(tmpsymbol.name, token)
            # ! Error Handling End
            else:
                update_symbol_table(symbol)
        node_new = SEMANTIC_STACK.pop(-1)
        node_new.name = 'PPT_declaration_class'
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'PPT_variable_declaration':
        node_new = Node()
        node_new.type = 'int'
        id = OP_STACK[-1]['data']
        node_new.id = id
        SEMANTIC_STACK.append(node_new)
    elif none_terminal == 'PPT_declaration':  # 关键的问题是注意到我这里面其实并没有书写我们的PPT_declaration之类的动作
        node_new = copy.deepcopy(SEMANTIC_STACK.pop(-1))
        node_new.name = 'PPT_declaration'
        SEMANTIC_STACK.append(node_new)  # 这个也就象是普通增加一个变量，啥名字都没有
    elif none_terminal == 'PPT_function_declaration':
        node_new = SEMANTIC_STACK.pop(-1)
        node_new.type = OP_STACK[-4]['type']
        # print("nodenewtype: ", node_new.type)
        # printNode(node_definition)
        node_definition = SEMANTIC_STACK.pop(-1)
        # ! Handle function_redefinition Start
        # tmpfunction = find_function_by_name(node_definition.data)
        # if tmpfunction is not None:
        #     print("tmpfunc ",tmpfunction.name)
        #     error_Handler_RedefinedFunctionNoLineNum(tmpfunction.name)
        #     FLAG=1
        #     return
        # ! Handle function_redefinition End
        # else:
        node_new.name = 'function_implement'
        code_temp = []
        code_temp.append((node_definition.data, ':', '_', '_'))
        for node in node_definition.stack:
            code_temp.append(
                ('pop', '_', 4 * node_definition.stack.index(node), node.place))
        if len(node_definition.stack) > 0:
            code_temp.append(('-', 'fp', 4 * len(node_definition.stack), 'fp'))
        for code in reversed(code_temp):
            node_new.code.insert(0, code)
        code_end = node_new.code[-1]
        if code_end[0][0] == 'l':
            lable = code_end[0]
            node_new.code.remove(code_end)
            for code in node_new.code:
                if code[3] == lable:
                    node_new.code.remove(code)
        SEMANTIC_STACK.append(node_new)
# stack_disp_top()
    return

#########################################################
# 前后端数据传递部分
#########################################################
# fcy 12-6 语义分析传数据部分 Start
# ~ ! 注意到LYM上面的四元式输出函数改了, 这个也需要进行相应的改动?


def getSemanticData():
    # fd=open(os.path.join(SOURCE_PATH,NAME_INTERMEDIATE_CODE), 'w')
    # INTERMEDIATE_CODE is a global variable
    global INTERMEDIATE_CODE
    # 需要重新更新
    try:
        INTERMEDIATE_CODE = SEMANTIC_STACK[0].code
    except:
        INTERMEDIATE_CODE=[('','','','')]
    INTERMEDIATE_CODE.insert(0, ('call', '_', '_', 'end'))
    INTERMEDIATE_CODE.insert(0, ('call', '_', '_', 'main'))
    write_my_intermediate_code()
    global SemanticData
    SemanticData = []  # 修改，避免重复append上一次的东西
    # SemanticData = []
    for code in INTERMEDIATE_CODE:
        # SemanticData.append('Fuckfuck')
        if code[0] == ':=':
            SemanticData.append('{}={}'.format(code[3], code[1]))
        elif code[1] == ':':
            # if code[0][0]=='f' or code[0]=='main':
            # SemanticData.append('\n')
            SemanticData.append('{}:'.format(code[0]))
        elif code[0] == 'call' or code[0] == 'push' or code[0] == 'pop' or code[0] == 'store' or code[0] == 'load' or code[0] == 'j':
            SemanticData.append('{}  {}'.format(code[0], code[3]))
        elif code[0] == 'j>':
            SemanticData.append('j>0 {} {}'.format(code[1], code[3]))
        elif code[0] == 'return':
            SemanticData.append('return')
        else:
            SemanticData.append('{}={}{}{}'.format(
                code[3], code[1], code[0], code[2]))
        # SemanticData.append('\n')
    return
    # fd.close()


def getSemantic():
    getSemanticData()
    global SemanticData
    return SemanticData


def getSemanticError():
    global ERROR_MSG
    return ERROR_MSG

# fcy 12-6 语义分析传数据部分 End


def get_tokens(mode, datastr):
    global ERROR_TOKEN
    global stackTB
    stackTB = []  # 这里刷新的时候要注意需要全部刷新一次
    renew_variables()
    global dfa
    global TOKENS
    read_grammer_from_json(os.path.join(SOURCE_PATH, NAME_GRAMMER_JSON))
    # read_grammer_from_plain(os.path.join(SOURCE_PATH,NAME_GRAMMER_PLAIN))
    generate_doted_productions()  # 这一步对应生成产生式的所有项目
    generate_first()  # 产生所有产生是的first集合
    dfa = DFA()
    generate_dfa()  # 在这个global DFA当中就有对应的DFA的这样的一个数据结构，对应的是项目集规范族下面的DFA集合
    generate_table()
    write_to_table()
    try:
        TOKENS = generate_tokens(os.path.join(
            SOURCE_PATH, NAME_SOURCE_CODE), mode, datastr)
        resToken = 0
    except:
        resToken = 1
        TOKENS = {}
    outTokens = copy.deepcopy(TOKENS)
    # 加到这里面来是为了需要重新跑后续的东西：
    res_ana = start_analyse()
    return outTokens, resToken, res_ana, ERROR_TOKEN


def generate_LR1_table():  # 生成LR(1)分析表
    x = []
    global dfa
    for i in range(len(dfa.state)):
        row = {}
        for j in range(len(TERMINAL_SYMBOL_GROUP)):
            row[TERMINAL_SYMBOL_GROUP[j]["type"]] = ACTION[i][j]
        for j in range(len(NONE_TERMINAL_SYMBOL_GROUP)):
            row[NONE_TERMINAL_SYMBOL_GROUP[j]] = GOTO[i][j]
        x.append(row)
    return x


def generate_stackTB():
    # def add_table_colum(operation, action, state):
    global RECORD_TABLE
    global CURRENT_STEP
    global stackTB
    CURRENT_STEP += 1
    op_stack_column = ""
    tokens_column = ""
    if len([x['type'] for x in OP_STACK]) > 5:
        op_stack_column = "...... "
    op_stack_column += " ".join([x['type'] for x in OP_STACK][-5:])
    tokens_column += " ".join([x['type'] for x in TOKENS][:5])
    if len([x['type'] for x in TOKENS]) > 5:
        tokens_column += " ......"
    state_stack_column = " ".join([x.name for x in STATE_STACK])
    row = [str(CURRENT_STEP), op_stack_column, tokens_column,
           operation, state_stack_column, action, state]
    obj = {
        "步骤": str(CURRENT_STEP),
        "当前栈": op_stack_column,
        "输入串": tokens_column,
        "动作": operation,
        "状态栈": state_stack_column,
        "ACTION": action,
        "GOTO": state
    }
    RECORD_TABLE.append(row)
    stackTB.append(obj)
    return


def getLR1():
    generate_LR1_table()
    global LR1
    return LR1


def getstack():
    global stackTB
    return stackTB

###############################################################


stackTB = []
read_grammer_from_json(os.path.join(SOURCE_PATH, NAME_GRAMMER_JSON))
generate_doted_productions()  # 这一步对应生成产生式的所有项目
generate_first()  # 产生所有产生是的first集合
dfa = DFA()
generate_dfa()  # 在这个global DFA当中就有对应的DFA的这样的一个数据结构，对应的是项目集规范族下面的DFA集合
generate_table()
write_to_table()
TOKENS = generate_tokens(os.path.join(SOURCE_PATH, NAME_SOURCE_CODE), 0, '')
start_analyse()
LR1 = generate_LR1_table()
# newly added
try:
    INTERMEDIATE_CODE = SEMANTIC_STACK[0].code
except:
    INTERMEDIATE_CODE=[('','','','')]
INTERMEDIATE_CODE.insert(0, ('call', '_', '_', 'end'))
INTERMEDIATE_CODE.insert(0, ('call', '_', '_', 'main'))
write_my_intermediate_code()
SemanticData = []
getSemanticData()
