#coding: utf-8
# update: 1.去掉了与书籍相关字符串左右的空格  
# update: 2.采用了OOP的方式进行统计
# update：3 利用各个书籍的链接去统计详细信息，并分别写入文件中

'''
针对豆瓣读书中“新书速递”（URL：http://book.douban.com/latest?icn=index-latestbook-all）进行简单的爬虫，并生成TXT文件，
纪录书名、作者以及短评
简单的实现，仍然需要对代码进行优化，现存问题是由于网页源代码中含有过多的换行符（'\n'），由此产生的正则表达式结果也会有影响，
需要去解决
'''
# coding: utf-8
import re
import requests
import os
import time

class Douban(object):
    def __init__(self):
        print u'这次是详细的喽~~~'

    #获取网页源代码，添加header防止服务器禁止访问,cookie添加成自己的就可以
    def get_html(self, url):
        header = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            #'cookie':
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
            'Host': 'book.douban.com',
            'Upgrade-Insecure-Requests': '1'
        }
        response = requests.get(url, headers=header)
        return response.text

    # 通过正则表达式获取各个图书的超链接
    def get_detailed_url(self, html):
        link = []
        l = re.findall('(http://book.douban.com/subject/[0-9]{8})', html, re.S)
        print len(l)
        for i in l:
            i = i.encode('utf-8') #获取的原始字符串为Unicode编码
            link.append(i)
        print len(link)
        return link

    # 或取图书的信息
    def get_book_detail(self, book_url):
        book_info = {}
        book_html = requests.get(book_url)
        book_info['Title'] = re.search('<span property="v:itemreviewed">(.*?)</span>', book_html.text, re.S).group(1)
        People = re.findall('<a class="" href="/search/.*?">(.*?)</a>', book_html.text, re.S)
        book_info['Author'] = People[0]
        book_info['Translator'] = People[1:]
        return book_info

    # 将图书信息单独保存为TXT文件
    def save_info(self, book_info):
        filename = book_info['Title'] + '.txt'
        f = open(filename, 'w')
        f.writelines(('title:' + ''.join(book_info['Title']) +'\n').encode('utf-8'))
        f.writelines(('author' + ''.join(book_info['Author']) + '\n').encode('utf-8'))
        f.writelines(('tanslator' + ''.join(book_info['Translator']) + '\n').encode('utf-8'))
        f.close()
os.chdir('C:\Users\zhangla\PycharmProjects\PydoubanFM\dbbook')
db = Douban()
url = "http://book.douban.com/latest?icn=index-latestbook-all"
html = db.get_html(url)
link = db.get_detailed_url(html)

for item in link:
    print "now system is processing ",
    print item
    each = db.get_book_detail(item)
    db.save_info(each)
    time.sleep(1)
