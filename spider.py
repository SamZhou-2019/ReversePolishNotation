import os
import re
import time

from bs4 import BeautifulSoup
import requests

global start_time
global item_no
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/54.0.2840.99 Safari/537.36'}


def get_soup(url):
    # 获取超文本
    try:
        url_html = requests.get(url, headers=headers)
    except:
        print("获取数据发生错误，请检查网络连接。")
        exit(-5)
    url_html.encoding = 'utf8'
    # 解析网页
    _soup_ = BeautifulSoup(url_html.text, 'lxml')
    return _soup_


# 爬取页面上的主要链接，一共十三个
def lines(_soup_):
    global item_no
    for a in range(0, 13):
        id_ = "line_u10_" + str(a)
        finds = _soup_.find('li', id=id_)
        # 对链接进行处理
        if '..' in finds.a['href'].strip():
            website = 'https://jwc.xidian.edu.cn/' + finds.a['href'].strip().replace('../', '')
        elif 'http' not in finds.a['href'].strip():
            website = 'https://jwc.xidian.edu.cn/' + re.findall("info.*", finds.a['href'].strip())[0]
        else:
            website = finds.a['href'].strip()
        with open('data.csv', 'a+', encoding='utf8') as f:
            f.write(str(item_no) + '\t' + finds.a.div.span.text + '\t' + finds.a[
                'title'].strip() + '\t' + website + '\n')
        # 链接编号，简化组织与检索
        item_no += 1


def spider(web):
    global start_time
    url = 'https://jwc.xidian.edu.cn/' + web + '.htm'
    soup = get_soup(url)
    lines(soup)
    # 获取总页码
    pageNum = soup.find('tr', valign="middle")
    pageNum = int(re.findall('[0-9]*$', pageNum.td.text.strip())[0])

    for page in range(pageNum - 1, 0, -1):
        print('\r正在收集教务处网站信息  %.2f KB  %.2f s' % (
            float(os.stat('data.csv').st_size / 1024), float(time.time() - start_time)), end='')
        url = 'https://jwc.xidian.edu.cn/' + web + '/' + str(page) + '.htm'
        soup = get_soup(url)
        lines(soup)


def spider_module():
    if os.path.exists('data.csv'):
        os.remove('data.csv')
    global item_no
    item_no = 0
    global start_time
    start_time = time.time()
    print('开始收集教务处网站信息')
    _list_ = ['tzgg', 'jxxx', 'jxyj', 'sjjx', 'zljk']
    for item in _list_:
        spider(item)
    end_time = time.time()
    print("\r收集完成，数据大小为 %.2f KB，用时 %.2f s" % (float(os.stat('data.csv').st_size / 1024), float(end_time - start_time)))
