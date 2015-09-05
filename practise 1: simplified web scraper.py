#coding: utf-8
# update: 1.去掉了与书籍相关字符串左右的空格  
# update: 2.采用了OOP的方式进行统计
# next design： 利用各个书籍的链接去统计详细信息，并分别写入文件中

'''
针对豆瓣读书中“新书速递”（URL：http://book.douban.com/latest?icn=index-latestbook-all）进行简单的爬虫，并生成TXT文件，
纪录书名、作者以及短评
简单的实现，仍然需要对代码进行优化，现存问题是由于网页源代码中含有过多的换行符（'\n'），由此产生的正则表达式结果也会有影响，
需要去解决
'''
#coding: utf-8
import requests
import re


class DoubanBook(object):
    def __init__(self):
        print u'多读书，读好书：）'


    # 获取豆瓣读书推荐类表的HTML内容
    def get_html(self, url):
        html = requests.get(url)
        return html.text


    # 获取各个图书的html语言块
    def get_html_book_block(self, source):
        item = re.findall('<div class="detail-frame">(.*?)</li>',source, re.S)
        print item
        return item


    # 通过正则表达式获取相应的字段值
    def get_each(self, each):
        L = {}
        L['book'] = re.search('<h2>(.*?)</h2>', each, re.S).group(1)
        L['info'] = re.search('<p class="color-gray">(.*?)</p>', each, re.S).group(1)
        L['description'] = re.search('<p>(.*?)</p>', each, re.S).group(1)
        L['link'] = re.findall('<a href="(http://book.douban.com/subject/[0-9]*/)">', each, re.S)
        print L['link']
        return L


    def save_info(self, info):
        f = open("bookinfo.txt",'a')
        for i in info:
            x1 = 'book: ' + ''.join(i['book'].split('\n')[1:-1]).strip() + '\n'
            x1 = x1.encode('utf-8')
            x2 = 'info: ' + ''.join(i['info'].split('\n')[1:-1]).strip() + '\n'
            x2 = x2.encode('utf-8')
            x3 = 'desc: ' + ''.join(i['description'].split('\n')[1:-1]).strip() + '\n'
            x3 = x3.encode('utf-8')
            x4 = 'link: ' + ''.join(i['link']) + '\n'
            x4 = x4.encode('utf-8')
        # print type(x1)
        # print type(x2)
        # print type(x3)
            f.writelines(x1+'\n')
            f.writelines(x2+'\n')
            f.writelines(x3+'\n')
            f.writelines(x4+'\n\n')
        f.close()


bd = DoubanBook()
bookinfo = []
url = "http://book.douban.com/latest?icn=index-latestbook-all"
content = bd.get_html(url)
block = bd.get_html_book_block(content)
for every in block:
    i = bd.get_each(every)
    bookinfo.append(i)
save = bd.save_info(bookinfo)
