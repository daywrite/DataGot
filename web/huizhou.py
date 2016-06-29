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
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36 LBBROWSER',
               'Connection': 'keep-alive'}
    htmlwrite = HtmlFile()

    def __init__(self):
        super(huizhouurl, self).__init__()

    # 解析详细页面信息
    def getitem(self, urlbase):
        t1 = time.time()
        result = requests.get(urlbase.url, headers=self.headers, timeout=(3.05, 1.5))

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

        try:
            # 获得标题
            print('题名', mainPart.div.text)
            lr['题名'] = mainPart.div.text
        except Exception as e:
            lr['题名'] = ''

        t2 = time.time()
        LOG.info('解析页面耗时:%f' % (t2 - t1))


if __name__ == '__main__':
    hz = huizhouurl()

    hz.getitem(UrlBean('http://huizhou.58.com/ershoufang/25864472115792x.shtml', 'wwwfangcom#getitem', param='北京',
                       order='1234'))
