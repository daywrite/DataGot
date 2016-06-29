#单例测试导入路径
if __name__ == '__main__':
    import sys, os
    parent_path = os.path.dirname(os.getcwd())
    sys.path.append(parent_path)

import os, time, gzip
from log.logger import *
LOG=logging.getLogger()
LOG.handlers[0].setLevel(logging.INFO)
LOG.handlers[1].setLevel(logging.DEBUG)

class HtmlFile(object):
    __rootpath = os.path.split(os.path.realpath(__file__))[0].split(':')[0] + ':\\gxd\\html'
    def __init__(self):
        pass

    def init(self, str=None):
        pass

    def save(self, website, htmlname, htmltext, autocommit=True):
        fname = htmlname.split('?')[0].split('/')[-1] if htmlname and '?' in htmlname else htmlname.split('/')[-1]
        filepath ='\\'.join([self.__rootpath, website, time.strftime('%Y-%m-%d', time.localtime())])
        if not os.path.exists(filepath):
            os.makedirs(filepath, exist_ok=True)
        try:
            # with open('%s\\%s' % (filepath, fname), 'w', encoding='utf8') as f :
            #     f.write(htmltext)
            g = gzip.GzipFile(mode="wb", compresslevel=9, fileobj=open('%s\\%s' % (filepath, fname+'.gz'), 'wb'))
            g.write(htmltext.encode('utf8'))
            g.close()
        except Exception as e:
            LOG.error('写HTML失败!文件名%s,错误信息:%s', '\\'.join([filepath,htmlname]), str(e))
        #if autocommit :
        #    self.__con.commit()

    def comm(self):
        pass

    def close(self):
        pass

if __name__ == '__main__':
    HtmlFile().save('www58com\\二手房\\北京', '24316612556215x.shtml', 'text')