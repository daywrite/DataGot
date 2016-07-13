from common.base import *
from txt.txt import *
from regex.regex import *
from util.TextRe import *

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
from log.categorylog import *
from bean.urlbean import *
import requests, re, math, _thread, threading, urllib, string
from bs4 import BeautifulSoup, Tag, NavigableString
from time import sleep, ctime

lock = _thread.allocate_lock()


class myThread(threading.Thread):
    def __init__(self, nloop):
        super(myThread, self).__init__()
        self.nloop = nloop

    def run(self):
        print('start loop', threading.current_thread(), 'at:', ctime())
        for i in self.nloop:
            print(i)
            try:
                resultlist = []
                result = requests.get(i, headers=URL_REQUEST_headers, timeout=60)
                if result.status_code == requests.codes.ok:
                    soup = BeautifulSoup(result.content.decode('gbk'), 'html.parser')
                    content = soup.findAll('a')

                    for item in content:
                        regex_href_result = regexhelper(re.compile(r'href="([^"]*)"')).regexbyrule(str(item))
                        if regexhelper(re.compile(r'ProjectCode')).regexcontainstr(regex_href_result):
                            resultlist.append(regex_href_result)

                    resultlist = list(set(resultlist))

                    for item in resultlist:
                        lock.acquire()
                        f = open('D:\\gxd\\huizhouyushou\\one.txt', 'a')
                        f.write('http://113.106.199.148/web/' + item.replace('amp;', ''))
                        f.write('\n')
                        f.close()
                        lock.release()
            except Exception as e:
                print('error:' + e)


class myThreadbuild(threading.Thread):
    def __init__(self, nloop):
        super(myThreadbuild, self).__init__()
        self.nloop = nloop

    def run(self):
        print('start loop', threading.current_thread(), 'at:', ctime())
        for i in self.nloop:
            try:
                print(i)
                resultlist = []
                result = requests.get(urllib.parse.quote(i.encode('gbk'), safe=string.printable),
                                      headers=URL_REQUEST_headers, timeout=60)
                if result.status_code == requests.codes.ok:
                    soup = BeautifulSoup(result.content.decode('gbk'), 'html.parser')

                    lrcommon = {}

                    fieldtext = soup.find('div', class_="Salestable")
                    for j in HuiZhou_Loop_Metas:
                        lrcommon[j] = TextRe.textcom(fieldtext, j + '：', 'td')

                    lrcommon['来源链接'] = i

                    reStr = txthelper.joinStr(HuiZhou_Data_Metas, lrcommon, '\t')
                    lock.acquire()
                    f = open('D:\\gxd\\huizhouyushou\\build.txt', 'a')
                    f.write(reStr)
                    f.write('\n')
                    f.close()
                    lock.release()

                    # 项目楼栋信息
                    try:
                        trall = soup.findAll('tr', class_='Searchboxx')
                        for tr in trall:
                            lrbuild = []
                            for td in tr.findAll('td'):
                                if td.find('p'):
                                    lrbuild.append(HuiZhou_Base_Url + td.find('a')['href'].strip())
                                else:
                                    lrbuild.append(TextRe.replace(td.text))

                            lrbuild.append(i)
                            # 写入文本
                            lock.acquire()
                            f = open('D:\\gxd\\huizhouyushou\\build2.txt', 'a',encoding='utf-8')
                            f.write('\t'.join(lrbuild))
                            f.write('\n')
                            f.close()
                            lock.release()
                    except Exception as e:
                        print('error-1:' + str(e))
                        pass

            except Exception as e:
                print('error-2:' + str(e))
                continue

class myThreadunit(threading.Thread):
    def __init__(self, nloop):
        super(myThreadunit, self).__init__()
        self.nloop = nloop

    def run(self):


        print('start loop', threading.current_thread(), 'at:', ctime())
        ret=[]
        for i in self.nloop:
            try:
                print(i)
                resultlist = []
                result = requests.get(urllib.parse.quote(i.encode('gbk'), safe=string.printable),
                                      headers=URL_REQUEST_headers, timeout=60)
                if result.status_code == requests.codes.ok:
                    soup = BeautifulSoup(result.content.decode('gbk'), 'html.parser')

                    lrcommon = []

                    # 项目基本信息
                    table = soup.find('table', class_="tablelw")
                    for tr in table.findAll('tr')[0:2]:
                        for td in tr.findAll('td'):
                            lrcommon.append(TextRe.replace(td.text))

                    lrcommon.append(i)

                    lock.acquire()
                    f = open('D:\\gxd\\huizhouyushou\\unit.txt', 'a',encoding='utf-8')
                    f.write('\t'.join(lrcommon))
                    f.write('\n')
                    f.close()
                    lock.release()

                    # 项目单元信息
                    trall = soup.findAll('tr', class_="a1")
                    floorcount = ''
                    for tr in trall:
                        for td in tr.findAll('td')[0:6]:

                            div = td.findAll('div')
                            if len(div) == 1:
                                if div[0].text.strip() == '':
                                    floorcount = ''
                                else:
                                    floorcount = div[0].text
                            else:
                                lrUnit = []
                                lrUnit.append(TextRe.replace(floorcount))
                                lrUnit.append(TextRe.replace(div[0].text))
                                urlcount = re.compile('(\d+,\d+)').findall(str(div[1]))[0]
                                lrUnit.append(
                                    (HuiZhou_Base_Url + 'House.jsp?id={0}&lcStr={1}').format(urlcount.split(',')[0],
                                                                                             urlcount.split(',')[1]))

                                lrUnit.append(i)

                                ret.append('\t'.join(lrUnit))
            except Exception as e:
                print('error-2:' + str(e))
                continue
        try:
           lock.acquire()
           f = open('D:\\gxd\\huizhouyushou\\unit2.txt', 'a',encoding='utf-8')
           for k in ret:
               f.write(k)
               f.write('\n')
           f.close()
           lock.release()
        except Exception as e:
           print('error-1:' + str(e))
           lock.release()
class myThreadhouse(threading.Thread):
    def __init__(self, nloop):
        super(myThreadhouse, self).__init__()
        self.nloop = nloop

    def run(self):
       print('start loop', threading.current_thread(), 'at:', ctime())
       ret=[]
       for i in self.nloop:
           try:
               print(i)
               resultlist = []

               result = requests.get(urllib.parse.quote(i.encode('gbk'), safe=string.printable),
                                     headers=URL_REQUEST_headers, timeout=60)
               if result.status_code == requests.codes.ok:
                   soup = BeautifulSoup(result.content.decode('gbk'), 'html.parser')

                   lrcommon = {}

                   # 项目基本信息
                   fieldtext = soup.find('div', class_="Salestable")
                   for j in HuiZhou_Houst_Loop_Metas:
                       lrcommon[j] = TextRe.textcom(fieldtext, j + '：', 'td')

                   lrcommon["来源链接"] =i

                   reStr = txthelper.joinStr(HuiZhou_Houst_Data_Metas, lrcommon, '\t')

                   ret.append(reStr)
                   # try:
                   #     lock.acquire()
                   #     f = open('D:\\gxd\\huizhouyushou\\house.txt', 'a',encoding='utf-8')
                   #     f.write(reStr)
                   #     f.write('\n')
                   #     f.close()
                   #     lock.release()
                   # except Exception as e:
                   #     print('error-1:' + str(e))
                   #     lock.release()
           except Exception as e:
                print('error-2:' + str(e))
                continue

       try:
           lock.acquire()
           f = open('D:\\gxd\\huizhou\\house.txt', 'a',encoding='utf-8')
           for k in ret:
               f.write(k)
               f.write('\n')

           f.close()
           lock.release()
       except Exception as e:
           print('error-1:' + str(e))
           lock.release()
class huizhouurl(ParserBase):
    htmlwrite = HtmlFile()

    def __init__(self):
        super(huizhouurl, self).__init__()

    # 解析Url
    def getoneurl(self, urlbase, name, mylog):
        mylog.info(urlbase.url)

        try:
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
                    t = txthelper("D:\\gxd\\huizhou\\", name, txtType.a.name)
                    t.write(HuiZhou_Base_Url + item)

                t.close()
        except Exception as e:
            mylog.info(e)

    # 解析二级url
    def gettwourl(self, urlbase, name, mylog):

        mylog.info(urlbase.url)
        try:
            result = requests.get(urlbase.url, headers=URL_REQUEST_headers, timeout=60)
            if result.status_code == requests.codes.ok:
                soup = BeautifulSoup(result.content.decode('gbk'), 'html.parser')

                lrcommon = {}

                # 项目基本信息
                fieldtext = soup.find('div', id="Searchform")
                for i in HuiZhou_Loop_Metas:
                    lrcommon[i] = TextRe.textcom(fieldtext, i + '：', 'td')

                lrcommon['来源链接'] = urlbase.url

                reStr = txthelper.joinStr(HuiZhou_Data_Metas, lrcommon, '\t')
                f = txthelper('D:\\gxd\\huizhou\\', name + '.txt', 'a')
                f.writealine(reStr)
                f.close()

                # 项目楼栋信息
                try:
                    trall = soup.findAll('tr', class_='Searchboxx')
                    for tr in trall:
                        lrbuild = []
                        for td in tr.findAll('td'):
                            if td.find('p'):
                                lrbuild.append(HuiZhou_Base_Url + td.find('a')['href'].strip())
                            else:
                                lrbuild.append(TextRe.replace(td.text))

                        lrbuild.append(urlbase.url)
                        # 写入文本
                        f = txthelper('D:\\gxd\\huizhou\\', name + '2.txt', 'a')
                        f.writealine('\t'.join(lrbuild))
                        f.close()
                except:
                    pass
        except Exception as e:
            mylog.info(e)

    # 解析三级url
    def getthreeurl(self, urlbase, name, mylog):
        mylog.info(urlbase.url)

        try:
            result = requests.get(urlbase.url, headers=URL_REQUEST_headers, timeout=60)
            if result.status_code == requests.codes.ok:
                soup = BeautifulSoup(result.content.decode('gbk'), 'html.parser')

                lrcommon = []

                # 项目基本信息
                table = soup.find('table', class_="tablelw")
                for tr in table.findAll('tr')[0:2]:
                    for td in tr.findAll('td'):
                        lrcommon.append(TextRe.replace(td.text))

                lrcommon.append(urlbase.url)

                f = txthelper('D:\\gxd\\huizhou\\', name + '.txt', 'a')
                f.writealine('\t'.join(lrcommon))
                f.close()

                # 项目单元信息
                trall = soup.findAll('tr', class_="a1")
                floorcount = ''
                for tr in trall:
                    for td in tr.findAll('td'):
                        lrUnit = []
                        div = td.findAll('div')
                        if len(div) == 1:
                            if div[0].text.strip() == '':
                                pass
                            else:
                                floorcount = div[0].text
                        else:
                            lrUnit.append(TextRe.replace(floorcount))
                            lrUnit.append(TextRe.replace(div[0].text))
                            urlcount = re.compile('(\d+,\d+)').findall(str(div[1]))[0]
                            lrUnit.append(
                                (HuiZhou_Base_Url + 'House.jsp?id={0}&lcStr={1}').format(urlcount.split(',')[0],
                                                                                         urlcount.split(',')[1]))

                            lrUnit.append(urlbase.url)

                            # 写入文本
                            f = txthelper('D:\\gxd\\huizhou\\', name + '2.txt', 'a')
                            f.writealine('\t'.join(lrUnit))
                            f.close()
        except Exception as e:
            mylog.info(e)

    # 解析四级url-房屋信息
    def getfour(self, urlbase, name, mylog):
        # 实例化当前日志
        mylog.info(urlbase.url)

        # 请求信息
        try:
            result = requests.get(urlbase.url, headers=URL_REQUEST_headers, timeout=60)
            if result.status_code == requests.codes.ok:
                soup = BeautifulSoup(result.content.decode('gbk'), 'html.parser')

                lrcommon = {}

                # 项目基本信息
                fieldtext = soup.find('div', class_="Salestable")
                for i in HuiZhou_Houst_Loop_Metas:
                    lrcommon[i] = TextRe.textcom(fieldtext, i + '：', 'td')

                lrcommon["来源链接"] = urlbase.url

                reStr = txthelper.joinStr(HuiZhou_Houst_Data_Metas, lrcommon, '\t')
                f = txthelper('D:\\gxd\\huizhou\\', name + '.txt', 'a')
                f.writealine(reStr)
                f.close()

        except Exception as e:
            mylog.info(e)

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


def now():
    return ctime()


if __name__ == '__main__':
    # r=urllib.parse.quote(u'http://113.106.199.148/web/realestate_presale.jsp?licenceCode=惠市房预许(2010)009号&ProjectCode=2009001470'.encode('gbk'),safe=string.printable)
    # r='•'.encode('utf8').decode('utf-8')
    # 线程数
    linecount = 8
    # 线程集合
    linegroup = []
    # 线程池
    thpool = []
    # 数据
    data = []

    # (1)
    # for i in range(1, 27):
    #     data.append('http://113.106.199.148/web/presale.jsp?page=' + str(i) + '&code=&projectname=&compname=&address=')
    # (2)
    # f = open('D:\\gxd\\huizhouyushou\\one.txt', 'r')
    # while True:
    #     line = f.readline().strip('\n')
    #     if line:
    #
    #         print(line)
    #         data.append(line)
    #     else:
    #         break
    # f.close()
    # (3)
    # f = open('D:\\gxd\\huizhouyushou\\build2.txt', 'r',encoding='utf-8')
    # while True:
    #     line = f.readline().strip('\n')
    #     if line:
    #         print(line.split('\t')[5])
    #         data.append(line.split('\t')[5])
    #     else:
    #         break
    # f.close()

    # (4)
    f = open('D:\\gxd\\huizhou\\20160713091215_unit2.txt', 'r',encoding='utf-8')
    while True:
        line = f.readline().strip('\n')
        if line:
            data.append(line.split('\t')[2])
        else:
            break
    f.close()

    totalcount = len(data)
    step = math.ceil(totalcount / linecount)

    for i in range(linecount):
        beginvalue = step * (i)
        endvalue = beginvalue + step
        lr = {}
        lr["begin"] = beginvalue
        if (i == linecount - 1):
            lr["end"] = len(data)
        else:
            lr["end"] = endvalue
        linegroup.append(lr)

    for i in linegroup:
        thpool.append(myThreadhouse(data[int(i["begin"]):int(i["end"])]))
    for th in thpool:
        th.start()
    for th in thpool:
        th.join()
    print('all Done at:' + now())

    # hz = huizhouurl()

    # mylog = clog('huizhouyushou', 'getoneurl', '').getclog()
    # txtname=TimeRe.gettime()+'_one.txt'
    # for i in range(1, 27):
    #     ub = UrlBean('http://113.106.199.148/web/presale.jsp?page=' + str(i) + '&code=&projectname=&compname=&address=','huizhou#getoneurl')
    #     hz.getoneurl(ub,txtname,mylog)

    # mylog = clog('huizhou', 'getbuild', '').getclog()
    # txtname=TimeRe.gettime()+'_build'
    # f = open('D:\\gxd\\huizhou\\20160705142059_one.txt', 'r')
    # while True:
    #     line = f.readline().strip('\n')
    #     if line:
    #         ub = UrlBean(line, 'huizhou#getoneurl')
    #         hz.gettwourl(ub,txtname,mylog)
    #     else:
    #         break
    #
    # f.close()

    # mylog = clog('huizhou', 'getunit', '').getclog()
    # txtname=TimeRe.gettime()+'_unit'
    # f = open('D:\\gxd\\huizhou\\20160705152914_build2.txt', 'r',encoding='utf8')
    # while True:
    #     line = f.readline()
    #     if line:
    #         ub = UrlBean(line.split('\t')[5], 'huizhou#getoneurl')
    #         hz.getthreeurl(ub,txtname,mylog)
    #     else:
    #         break
    # f.close()

    # mylog = clog('huizhou', 'gethouse', '').getclog()
    # txtname=TimeRe.gettime()+'_house'
    # f = open('D:\\gxd\\huizhou\\20160706093944_unit2.txt', 'r',encoding='utf8')
    # while True:
    #     line = f.readline()
    #     if line:
    #        ub = UrlBean(line.split('\t')[2], 'huizhou#getoneurl')
    #        hz.getfour(ub,txtname,mylog)
    #     else:
    #         break
    #
    # f.close()
