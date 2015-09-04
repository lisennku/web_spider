# -*- coding:utf-8 -*- 
# update: 1.去掉了与书籍相关字符串左右的空格  

'''
针对豆瓣读书中“新书速递”（URL：http://book.douban.com/latest?icn=index-latestbook-all）进行简单的爬虫，并生成TXT文件，
纪录书名、作者以及短评
简单的实现，仍然需要对代码进行优化，现存问题是由于网页源代码中含有过多的换行符（'\n'），由此产生的正则表达式结果也会有影响，
需要去解决
'''
import re
import requests

def get_source(url):
    info = requests.get(url)
    return info.text


def get_item(url_data):
    item = re.findall('<div class="detail-frame">(.*?)</div>',url_data, re.S)
    return item


def each_item(each):
    L = {}
    L['book'] = re.search('<h2>(.*?)</h2>', each, re.S).group(1)
    L['info'] = re.search('<p class="color-gray">(.*?)</p>', each, re.S).group(1)
    L['description'] = re.search('<p>(.*?)</p>', each, re.S).group(1)
    return L


def save_info(book):
    f = open("booklist.txt",'a')
    for i in book:
        x1 = 'book: ' + ''.join(i['book'].split('\n')[1:-1]).strip() + '\n'
        x1 = x1.encode('utf-8')
        x2 = 'info: ' + ''.join(i['info'].split('\n')[1:-1]).strip() + '\n'
        x2 = x2.encode('utf-8')
        x3 = 'desc: ' + ''.join(i['description'].split('\n')[1:-1]).strip() + '\n'
        x3 = x3.encode('utf-8')
        # print type(x1)
        # print type(x2)
        # print type(x3)
        f.writelines(x1+'\n')
        f.writelines(x2+'\n')
        f.writelines(x3+'\n\n')
    f.close()


def print_list(book):
    for i in book:
        print 'book: ' ,
        for s in i['book'].split('\n')[1:-1]:
            print s,
        print '\n'
        print 'info: ' ,
        for s in i['info'].split('\n')[1:-1]:
            print s,
        print '\n'
        print 'desc: ' ,
        for s in i['description'].split('\n')[1:-1]:
            print s,
        print '\n'

url = "http://book.douban.com/latest?icn=index-latestbook-all"
bookinfo = []

source = get_source(url)
data = get_item(source)
for p in data:
    book_detail = each_item(p)
    # print book_detail['book']
    bookinfo.append(book_detail)
save_info(bookinfo)
print_list(bookinfo)
# print bookinfo[1]['book'].
# print bookinfo[1]['description'].split('\n')
# print bookinfo[1]['info'].split('\n')
