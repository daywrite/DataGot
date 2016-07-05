import time
from datetime import *


class TimeRe:
    @staticmethod
    def gettime(type='%Y%m%d%H%M%S'):
        now = datetime.now()
        return now.strftime(type)


if __name__ == '__main__':
    print(TimeRe.gettime())
