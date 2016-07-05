# 2016-7-5
# bearbad
# 不同类别日志扩展

import os
from log.logger import *
from util.TimeRe import *


class clog():
    def __init__(self, name, type, logger, ltype=logging.DEBUG):
        self.name = name
        self.type = type
        self.logger = logging.getLogger(logger)

        path = logpath + '\\' + name
        if not os.path.exists(path):
            os.makedirs(path)

        fh = logging.FileHandler(path+ '\\' + TimeRe.gettime() + '_' + type + '_log.txt','a')
        fh.setFormatter(logging.Formatter('%(asctime)s:%(name)s-->%(levelname)s %(message)s'))
        fh.setLevel(ltype)
        self.logger.addHandler(fh)

    def getclog(self):
        return self.logger
