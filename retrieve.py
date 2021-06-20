import os

import pandas as pd

from spider import get_soup


def retrieve(reverse_polish):
    # 工作区管理表
    _control_ = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    # 工作区
    _workspace_ = [set(), set(), set(), set(), set(), set(), set()]
    # 导入数据
    _data_ = pd.read_csv('data.csv', sep='\t', names=['NO', 'DATE', 'TITLE', 'WEBSITE'])
    # 优先级标志
    _prior_ = 1
    # 初始化工作区标志号
    j1 = j2 = j3 = -1

    item_no = 0
    for item in reverse_polish:
        if item == '+' or item == "*" or item == '-':
            for j in range(0, 6):
                # 选取优先级最大的两个工作区，和一个空工作区
                if _control_[j][0] == 1 and _control_[j][1] == _prior_ - 1:
                    j1 = j
                elif _control_[j][0] == 1 and _control_[j][1] == _prior_ - 2:
                    j2 = j
                elif _control_[j][0] == 0 and j3 == -1:
                    j3 = j
                # 选取完成后进行布尔运算操作
                if j1 != -1 and j2 != -1 and j3 != -1:
                    if item == '+':
                        _workspace_[j3] = _workspace_[j1].union(_workspace_[j2])
                    elif item == '*':
                        _workspace_[j3] = _workspace_[j1].intersection(_workspace_[j2])
                    elif item == '-':
                        _workspace_[j3] = _workspace_[j1].difference_update(_workspace_[j2])
                    # 以下判断是为了防止集合运算结果为空集，导致后续集合运算报错
                    if _workspace_[j3] is None:
                        _workspace_[j3] = set()
                    # 完成布尔运算后，设置工作区管理表、初始化标志、清理不需要的工作表空间，设置优先级
                    _control_[j1][0] = _control_[j2][0] = 0
                    _control_[j3][0] = 1
                    _prior_ = _prior_ - 1
                    _control_[j3][1] = _prior_ - 1
                    _workspace_[j1] = _workspace_[j2] = set()
                    j1 = j2 = j3 = -1
                    break
        else:
            # 对每个关键词进行检索
            for j in range(0, 6):
                # 找到一个空的工作区空间，将检索结果存入该工作区空间
                if _control_[j][0] == 0:
                    for i in range(0, len(_data_)):
                        if item in _data_['TITLE'][i]:
                            _workspace_[j].add(i)
                    _control_[j][0] = 1
                    _control_[j][1] = _prior_
                    _prior_ += 1
                    break

        item_no += 1

    # 将存有结果的工作区空间内的数据导出
    retrieve_result = set()
    for _set_ in _workspace_:
        if _set_ != set():
            retrieve_result = list(_set_)
    # 分页输出，每页十个结果
    if retrieve_result is not None and retrieve_result != set():
        print('共 ' + str(len(retrieve_result)) + ' 个结果')
        result_page_num = int(len(retrieve_result) / 10) + 1
        for result_page in range(0, result_page_num):
            print('第 ' + str(result_page + 1) + ' 页/共 ' + str(result_page_num) + ' 页')
            for count in range(result_page * 10, min(len(retrieve_result), result_page * 10 + 10)):
                print(str(count) + '\t' + _data_["TITLE"][retrieve_result[count]])
                print(_data_["WEBSITE"][retrieve_result[count]])
            print('-' * 50)
            a = input("输入数字0，1，2，3，4，5，6，7，8，9查看对应页面内容\n输入q返回检索界面，输入其它任意字符进入下一页")
            while str.isdigit(a):
                try:
                    print('--------' + _data_["TITLE"][retrieve_result[result_page * 10 + int(a)]] + '--------')
                    print(get_soup(_data_["WEBSITE"][retrieve_result[result_page * 10 + int(a)]]).find('div',
                                                                                                       class_="v_news_content").text.strip())
                except IndexError:
                    print('输入错误，不存在该结果。')
                print('-' * 50)
                a = input("输入数字0，1，2，3，4，5，6，7，8，9查看对应页面内容\n输入q返回检索界面，输入其它任意字符进入下一页")
            if a == 'q':
                break
    else:
        print('无结果')
