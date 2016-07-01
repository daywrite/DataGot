from common.base import *


class regexhelper:
    def __init__(self, rule):
        self.rule = rule

    # 某个规则
    # group[]
    def regexbyrule(self, s):
        return self.rule.search(s).group(1)

    # 包含某个字符串
    # true/false
    def regexcontainstr(self,s):
        return self.rule.search(s)
