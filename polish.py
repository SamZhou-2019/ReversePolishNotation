# 计算树的高度，为计算方便，只计算左子树
def tree_height(_tmp_):
    height = 0
    if isinstance(_tmp_, list):
        _tmpL_ = _tmp_[1]
        height = 1
        # 嵌套列表，每多一层高度加一
        while isinstance(_tmpL_, list):
            height += 1
            _tmpL_ = _tmpL_[1]
    return height


def post_order(tree):
    if isinstance(tree, list):
        if isinstance(tree[1], list):
            post_order(tree[1])
        else:
            print(tree[1], end=' ')
        if isinstance(tree[2], list):
            post_order(tree[2])
        else:
            print(tree[2], end=' ')
        print(tree[0], end=' ')
    else:
        print(tree)


def polish(_list_):
    _tmp_ = ['', '', '']
    for i in range(0, len(_list_)):
        if _list_[i] in ['+', '-', '*']:
            _tmp_[0] = _list_[i]
            # 左子树标志，因为在下面的for循环中是倒着遍历，因此从右子树开始添加
            isleft = False
            l_height = r_height = 0
            for j in range(i - 1, -1, -1):
                # 条件；不是空，左子树标志，左子树为空
                if _list_[j] is not None and isleft and _tmp_[1] == '':
                    l_height = tree_height(_list_[j])
                    _tmp_[1] = _list_[j]
                    _list_[j] = None
                    isleft = False
                    continue
                # 条件；不是空，左子树标志，右子树为空
                elif _list_[j] is not None and not isleft and _tmp_[2] == '':
                    r_height = tree_height(_list_[j])
                    _tmp_[2] = _list_[j]
                    _list_[j] = None
                    isleft = True
                    continue
                # 右子树复杂度大于左子树，则交换两个子树
            if l_height < r_height and _tmp_[1] != '' and _tmp_[1] != '':
                _swap_ = _tmp_[1]
                _tmp_[1] = _tmp_[2]
                _tmp_[2] = _swap_
            _list_[i] = _tmp_
            _tmp_ = ['', '', '']

    _tree_ = _list_[-1]
    post_order(_tree_)
