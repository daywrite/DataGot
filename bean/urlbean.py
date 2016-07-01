# 定义服务器和客户端之间传递信息
class UrlBase(object):
    SPLIT = '#'  # 消息格式    类名#方法名

    def __init__(self, url, message, key=None, order='', trytimes=0):
        # 类型数据
        self.__classname = self.__class__.__name__
        self.url = url
        self.message = message
        self.key = key
        self.order = order
        self.trytimes = trytimes

    def getmessage(self):
        return self.message

    def getmessagekey(self):
        return self.message.split(self.SPLIT)[0]

    def setkey(self, filter):
        if hasattr(filter, '__call__'):
            self.key = filter(self.url)
        else:
            self.key = filter

    # def __hash__(self):
    #     return self.key.__hash__()
    #
    # def __eq__(self, other):
    #     if other and isinstance(other, self.__class__):
    #         if self.key is None or other.key is None:
    #             return False
    #         if self.key and other.key and type(self.key)==type(other.key):
    #             return self.key == other.key
    #     return False

    def __lt__(self, other):
        if other and isinstance(other, self.__class__):
            if self.order is None or other.order is None:
                return True
            if self.order and other.order and type(self.order) == type(other.order):
                try:  # 尝试按数字类型进行比较提升效率
                    return int(self.order) < int(other.order)
                except Exception as e:
                    pass
                return self.order < other.order
        return True


class UrlBean(UrlBase):
    def __init__(self, url, message, param=None, headers=None, cookies=None, *args, **kwargs):
        super(UrlBean, self).__init__(url, message, *args, **kwargs)
        self.param = param
        self.headers = headers
        self.cookies = cookies

if __name__ == '__main__':
    # 测试类
    s = set()

    u1 = UrlBase('1', 2)
    u1.setkey(lambda x: True)

    u2 = UrlBase('1', 2)
    u2.setkey(lambda x: 1)

    u3 = UrlBase('1', 2)
    # u3.setkey(True)

    u4 = UrlBase('1', 2)
    # u4.setkey(1)
    s.add(u1)
    s.add(u2)
    s.add(u3)
    s.add(u4)
    print(len(s))
    print(u2 in s)
    print(u1 in s)
    print(u3 == u4)
    # s = set()
    # l = set(l)
    # lnew = l.difference(s)
    # s.update(lnew)
    UrlBase('/', 'getpages', param=1, headers=3, order=2)
