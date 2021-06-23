import pandas as pd

from spider import get_soup, spider_module


def retrieve(reverse_polish):
    # 工作区管理表
    _control_ = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    # 工作区
    _workspace_ = [set(), set(), set(), set(), set(), set(), set()]
    # 导入数据
    try:
        _data_ = pd.read_csv('data.csv', sep='\t', names=['NO', 'DATE', 'TITLE', 'WEBSITE'])
    except FileNotFoundError:
        print("\n数据不存在，尝试获取数据。")
        spider_module()

    # 优先级标志
    _prior_ = 1
    # 初始化工作区标志号
    j1 = j2 = j3 = -1

    for item in reverse_polish:
        if item == '+' or item == "*" or item == '-':
            for j in range(0, 6):
                # 选取优先级最大的两个工作区，和一个空工作区
                if _control_[j][0] == 1 and _control_[j][1] == _prior_ - 2:
                    j1 = j
                elif _control_[j][0] == 1 and _control_[j][1] == _prior_ - 1:
                    j2 = j
                elif _control_[j][0] == 0 and j3 == -1:
                    j3 = j
                # 选取完成后进行布尔运算操作
                if j1 != -1 and j2 != -1 and j3 != -1:
                    if item == '+':
                        _workspace_[j3] = _workspace_[j1] | _workspace_[j2]
                    elif item == '*':
                        _workspace_[j3] = _workspace_[j1] & _workspace_[j2]
                    elif item == '-':
                        _workspace_[j3] = _workspace_[j1] - _workspace_[j2]
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
                        if item in _data_['TITLE'][i] or item in _data_['DATE'][i]:
                            _workspace_[j].add(i)
                    _control_[j][0] = 1
                    _control_[j][1] = _prior_
                    _prior_ += 1
                    break

        if _prior_ == 7:
            print("工作区溢出，程序终止。")
            exit(-2)

    # 将存有结果的工作区空间内的数据导出
    n = 10
    for j in range(0, 6):
        if _workspace_[j] != set() and _control_[j][0] == 1:
            _workspace_[6] = list(_workspace_[j])
    # 分页输出，每页十个结果
    if _workspace_[6] is not None and _workspace_[6] != set():
        print('\n' + '-' * 50 + '\n共 ' + str(len(_workspace_[6])) + ' 个结果')
        # 统计页数
        result_page_num = int(len(_workspace_[6]) / n) + 1
        for result_page in range(0, result_page_num):
            print('第 ' + str(result_page + 1) + ' 页/共 ' + str(result_page_num) + ' 页')
            for count in range(result_page * n, min(len(_workspace_[6]), result_page * n + n)):
                print(str(count) + '\t' + _data_["DATE"][_workspace_[6][count]] + '\t' + _data_["TITLE"][
                    _workspace_[6][count]])
                print(_data_["WEBSITE"][_workspace_[6][count]])
            a = input('-' * 50 + "\n输入数字0，1，2，3，4，5，6，7，8，9查看对应页面内容\n输入q返回检索界面，输入其它任意字符进入下一页")[0]
            while str.isdigit(a):
                try:
                    print('--------' + _data_["TITLE"][
                        _workspace_[6][result_page * n + int(a)]] + '--------\n' + get_soup(
                        _data_["WEBSITE"][_workspace_[6][result_page * n + int(a)]]).find('div',
                                                                                          class_="v_news_content").text.strip())
                except IndexError:
                    print('输入错误，不存在该结果。')
                    break
                a = input('-' * 50 + "\n输入数字0，1，2，3，4，5，6，7，8，9查看对应页面内容\n输入q返回检索界面，输入其它任意字符进入下一页")[0]
            if a == 'q':
                break
    else:
        print('\n' + '-' * 50 + '\n无结果')
