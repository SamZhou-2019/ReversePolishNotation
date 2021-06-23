# 逆波兰实现程序
import re

from polish import polish
from retrieve import retrieve


def reverse(str_retrieve):
    if not re.match('[\w\+\-\*\(\)（）]+', str_retrieve):
        print("检索式不符合规范，请重新输入。")
        return -1
    # 各种符号的优先级，以字典形式录入
    charstack = {"(": 1, "-": 4, "*": 3, "+": 2, ")": 1, "": 0}
    # 字符串处理，将各个关键词分隔开，形成关键词列表
    str_retrieve = str(str_retrieve)
    # 由于括号左右总会与一个运算符（+、-、*）相邻，因此对关键词分割不影响，可直接删去
    _keywords_ = str_retrieve
    for bracket in ['(', ')', '（', '）']:
        _keywords_ = _keywords_.replace(bracket, '')
    # 剩余字符串按照+、-、*三个运算符进行分割·，形成关键词列表
    _keywords_ = re.split('[\+\-\*]', _keywords_)
    # 关键词序号初始化
    keyword_no = 0
    # 算符栈，为防止空栈导致错误，在栈中初始化一个空字符串
    _char_ = ['']
    # 逆波兰结果输出列表
    _result_ = []
    # 用于判断是关键词还是算符
    isChar = True

    # 将检索式字符串看作列表，按字符进行扫描
    for str_no in range(0, len(str_retrieve)):
        # 左括号：直接入栈
        if str_retrieve[str_no] in ['(', '（']:
            isChar = True
            _char_.append('(')
        # +-*：需判断当前扫描的算符与算符栈栈顶算符的优先级
        elif str_retrieve[str_no] in ['+', '-', '*']:
            isChar = True
            while charstack[_char_[-1]] >= charstack[str_retrieve[str_no]]:
                _result_.append(_char_.pop())
            _char_.append(str_retrieve[str_no])
        # 右括号：算符栈中的算符依次出栈，直至到达左括号
        elif str_retrieve[str_no] in [')', '）']:
            isChar = True
            while _char_[-1] != '(':
                _result_.append(_char_.pop())
            _char_.pop()
        # 关键词：扫描到关键词的第一个字符时，将关键词列表中存储的该词直接加入到结果列表中
        else:
            if isChar:
                isChar = False
                _result_.append(_keywords_[keyword_no])
                keyword_no += 1
    # 将算符栈中剩余的算符输出到结果列表中
    while _char_:
        _result_.append(_char_.pop())
    # 最后，将结果列表转化为字符串，并返回
    result = ''
    for item in _result_[:-1]:
        result = result + item + ' '

    print('原检索式：', str_retrieve)
    print('逆波兰表达式：', result)
    print('准波兰表达式：', end=' ')
    polish(_result_[:-1])

    retrieve(_result_[:-1])
