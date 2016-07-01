from common.base import *
from txt.txt import *
from regex.regex import *

# 自运行时调用该程序块
if __name__ == '__main__':
    import os, sys

    pypath = os.getcwd()
    returnpath = os.path.dirname(pypath)
    sys.path.append(returnpath)

# import时调用改程序块
if __name__ == 'huizhou':
    print('import时调用改程序块')

from web.webbase import ParserBase
from serializ.htmlfile import *
from log.logger import *
from bean.urlbean import *
import datetime

LOG = logging.getLogger()
LOG.handlers[0].setLevel(logging.INFO)
LOG.handlers[1].setLevel(logging.INFO)

import requests, re
from bs4 import BeautifulSoup, Tag, NavigableString


class myException(Exception): pass


class huizhouurl(ParserBase):
    htmlwrite = HtmlFile()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive"
    }

    def __init__(self):
        super(huizhouurl, self).__init__()

    # 解析Url
    def getoneurl(self, urlbase):
        print(urlbase.url)
        # 输出集合
        resultlist = []
        result = requests.get(urlbase.url, headers=URL_REQUEST_headers, timeout=60)
        if result.status_code == requests.codes.ok:
            soup = BeautifulSoup(result.content.decode('gbk'), 'html.parser')
            content = soup.findAll('a')

            for item in content:
                regex_href_result = regexhelper(re.compile(r'href="([^"]*)"')).regexbyrule(str(item))
                if regexhelper(re.compile(r'ProjectCode')).regexcontainstr(regex_href_result):
                    resultlist.append(regex_href_result)

            resultlist = list(set(resultlist))

            for item in resultlist:
                t = txthelper("D:\\gxd\\one.txt", txtType.a.name)
                t.write(item)

        print('执行完毕')

    # 解析详细页面信息
    def getitem(self, urlbase):
        t1 = time.time()
        result = requests.get(urlbase.url, headers=URL_REQUEST_headers, timeout=(3.05, 1.5))
        if (result.status_code != requests.codes.ok):
            LOG.warning('www58com %s 返回状态:%s', result.request.url, result.status_code)
            raise myException('%s 返回状态:%s' % (result.request.url, result.status_code))
        if "</html>" not in result.text.lower():
            LOG.warning('www58com %s 页面下载不全!', result.request.url)
            raise myException('%s %s, 页面下载不全!' % (result.request.url, result.text[-10:]))
        t2 = time.time()
        LOG.info('处理%s耗时:%.4f %.4f' % (result.url, t2 - t1, result.elapsed.microseconds / 1000000))

        # 存储页面信息
        t1 = time.time()
        self.htmlwrite.save('%s\\%s\\%s' % (self.__class__.__name__, '二手房', urlbase.param), result.url, result.text)
        t2 = time.time()

        t1 = time.time()
        reText = result.text
        soup = BeautifulSoup(result.content.decode('utf8'), 'html.parser')

        # 页面不存在就直接退出
        if soup.find(text=re.compile('你要找的页面不在这个星球上')) \
                and soup.find(text=re.compile('该页面可能被删除、转移或暂时不可用')):
            LOG.warning('此页面已不存在!%s', urlbase.url)
            return
        mainPart = soup.find('div', class_='mainTitle')

        lr = {}
        filed = ''

        try:
            filed = URL_REQUEST_Enum_Metas.省.name
            lr[filed] = mainPart.div.text
        except Exception as e:
            lr[filed] = ''

        # 写入文本
        t = txthelper("D:\\gxd\\test.txt", txtType.a.name)
        t.writealine(txthelper.joinStr(URL_REQUEST_BASE_Metas, lr, '\t'))


if __name__ == '__main__':
    hz = huizhouurl()

    for i in range(1, 43):
        ub = UrlBean('http://113.106.199.148/web/nowonsale.jsp?page=' + str(i) + '&projectname=&compname=&address=',
                     'huizhou#getoneurl')
        hz.getoneurl(ub)
