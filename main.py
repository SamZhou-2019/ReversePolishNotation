from reverse import reverse
from spider import spider_module

if __name__ == '__main__':
    if input("是否初始化信息？(Y/其它任意键)") == "Y":
        spider_module()

    str_re = ' '
    while True:
        str_re = input('-' * 50 + "\n请输入检索式（若要退出，请输入井号”#“）：\n")
        if str_re == "#":
            exit(1)
        reverse(str_re)
