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


class lianyungang(ParserBase):
    # 解析Url
    def getoneurl(self, urlbase, name, mylog):
        mylog.info(urlbase.url)

        try:
            # 输出集合
            resultlist = []
            result = requests.get(urllib.parse.quote(urlbase.url.encode('gbk'), safe=string.printable),
                                  headers=URL_REQUEST_headers, timeout=60)
            if result.status_code == requests.codes.ok:
                soup = BeautifulSoup(result.content.decode('gbk'), 'html.parser')
                div = soup.find('div', id='ctl00_CPH_M_sm_sBox_data')
                content = div.findAll('a')

                for item in content:
                    regex_href_result = regexhelper(re.compile(r'href="([^"]*)"')).regexbyrule(str(item))
                    if regexhelper(re.compile(r'homes_id')).regexcontainstr(regex_href_result):
                        resultlist.append(regex_href_result)

                resultlist = list(set(resultlist))

                for item in resultlist:
                    t = txthelper("D:\\gxd\\lianyungang\\", name, txtType.a.name)
                    t.write(LianYunGang_Base_Url + item)

                t.close()
        except Exception as e:
            mylog.info(e)

            # 小区属性


class getcommunity(threading.Thread):
    def __init__(self, url, mylog):
        super(getcommunity, self).__init__()
        self.url = url
        self.mylog = mylog

    def run(self):
        print('start loop', threading.current_thread(), 'at:', ctime())
        resultFirst = [];
        resultSecond = [];

        for i in self.url:
            try:
                result = requests.get(urllib.parse.quote(i.encode('gbk'), safe=string.printable),
                                      headers=URL_REQUEST_headers, timeout=60)
                if result.status_code == requests.codes.ok:
                    soup = BeautifulSoup(result.content.decode('gbk'), 'html.parser')

                    lrcommon = {}

                    fieldtext = soup.find('div', id="ctl00_CPH_M_sm_spfBox3")
                    for j in LianYunGang_Com_Loop_Metas:
                        lrcommon[j] = TextRe.textcom(fieldtext, j + ':', 'td')

                    lrcommon['来源链接'] = i
                    reFirst = txthelper.joinStr(LianYunGang_Com_Data_Metas, lrcommon, '\t')
                    resultFirst.append(reFirst)

                    # 楼栋
                    try:
                        buildText = soup.find('div', id="ctl00_CPH_M_sm_spfBox3")
                        trall = soup.findAll('tr', class_='hobuild')
                        for tr in trall:
                            lrbuild = []
                            for td in tr.findAll('td'):
                                if td.find('strong'):
                                    lrbuild.append(LianYunGang_Base_Url + td.find('a')['href'].strip())
                                else:
                                    lrbuild.append(TextRe.replace(td.text))

                            lrbuild.append(i)

                            reSecond = '\t'.join(lrbuild)
                            resultSecond.append(reSecond)

                    except Exception as e:
                        lock.acquire()
                        self.mylog.info(i)
                        self.mylog.info('error-2:' + str(e))
                        lock.release()
                        continue

            except Exception as e:
                lock.acquire()
                self.mylog.info(i)
                self.mylog.info('error-1:' + str(e))
                lock.release()
                continue

        try:
            lock.acquire()
            f = open('D:\\gxd\\lianyungang\\build.txt', 'a', encoding='utf-8')
            for k in resultFirst:
                f.write(k)
                f.write('\n')
            f.close()
            f = open('D:\\gxd\\lianyungang\\build2.txt', 'a', encoding='utf-8')
            for kk in resultSecond:
                f.write(kk)
                f.write('\n')
            f.close()
            lock.release()
        except Exception as e:
            print('error-write:' + str(e))
            lock.release()


class getunit(threading.Thread):
    def __init__(self, url, mylog):
        super(getunit, self).__init__()
        self.url = url
        self.mylog = mylog

    def run(self):
        print('start loop', threading.current_thread(), 'at:', ctime())
        resultFirst = [];

        for i in self.url:
            try:
                result = requests.get(urllib.parse.quote(i.replace('\ufeff','').encode('gbk'), safe=string.printable),
                                      headers=URL_REQUEST_headers, timeout=120)
                if result.status_code == requests.codes.ok:
                    soup = BeautifulSoup(result.content.decode('gbk'), 'html.parser')

                    divtext = soup.find('div', id='building')
                    lid = divtext['lid'].strip()
                    ltype = divtext['ltype'].strip()

                    div_tabalt_top = divtext.find('div', class_='tabalt_top').ul.li.text

                    trall = divtext.findAll('tr')
                    unit = []
                    unittd = trall[0].findAll('td')
                    for u in unittd[1:len(unittd)]:
                        unit.append(u.text)

                    for tr in trall[1:len(trall)]:
                        td = tr.findAll('td')
                        floor = td[0].div.text

                        unitint = -1
                        for td in td[1:len(td)]:
                            unitint = unitint + 1
                            divroom = td.findAll('div', class_='cssRoom')
                            for r in divroom:
                                lrunit = []
                                unitname = unit[unitint]
                                name = r.text
                                hid = r['hid'].strip()

                                lrunit.append(TextRe.replace(i))
                                lrunit.append(TextRe.replace(lid))
                                lrunit.append(TextRe.replace(ltype))
                                lrunit.append(TextRe.replace(div_tabalt_top))
                                lrunit.append(TextRe.replace(unitname))
                                lrunit.append(TextRe.replace(floor))
                                lrunit.append(TextRe.replace(name))
                                lrunit.append(TextRe.replace(hid))

                                # resultFirst.append('\t'.join(lrunit))
                                try:
                                    lock.acquire()
                                    f = open('D:\\gxd\\lianyungang\\unit.txt', 'a',encoding='utf-8')
                                    f.write('\t'.join(lrunit))
                                    f.write('\n')
                                    f.close()
                                    lock.release()
                                except Exception as e:
                                    lock.release()

            except Exception as e:
                lock.acquire()
                print(str(e))
                self.mylog.info(i)
                self.mylog.info('error-1:' + str(e))
                lock.release()
                continue
        # try:
        #    lock.acquire()
        #    f = open('D:\\gxd\\lianyungang\\unit.txt', 'a',encoding='utf-8')
        #    for k in resultFirst:
        #        f.write(k)
        #        f.write('\n')
        #    f.close()
        #    lock.release()
        # except Exception as e:
        #       lock.release()

if __name__ == '__main__':

    hz = lianyungang()

    # 线程数
    linecount = 1
    # 线程集合
    linegroup = []
    # 线程池
    thpool = []
    # 数据
    data = []

    # mylog = clog('lianyungang', 'getoneurl', '').getclog()
    # txtname = TimeRe.gettime() + '_one.txt'

    # for i in range(1, 50):
    #     ub = UrlBean(
    #         'http://www.lygfdc.com/WebSite/Search/Default.aspx?type=spf&city=&price=&wuye=&stat=&key=请输入楼盘名称或开发商&page=' + str(
    #             i),
    #         'huizhou#getoneurl')
    #     hz.getoneurl(ub, txtname, mylog)

    # mylog = clog('lianyungang', 'getcommunity', '').getclog()
    # f = open('D:\\gxd\\lianyungang\\20160713165326_one.txt', 'r', encoding='utf-8')
    # while True:
    #     line = f.readline().strip('\n')
    #     if line:
    #         data.append(line)
    #     else:
    #         break
    # f.close()

    mylog = clog('lianyungang', 'getunit', '').getclog()
    f = open('D:\\gxd\\lianyungang\\build2.txt', 'r', encoding='utf-8')
    while True:
        line = f.readline().strip('\n')
        if line:
            data.append(line.split('\t')[0])
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
        thpool.append(getunit(data[int(i["begin"]):int(i["end"])], mylog))
    for th in thpool:
        th.start()
    for th in thpool:
        th.join()
    print('all Done at:' + ctime())
