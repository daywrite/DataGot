from common.base import *


class txthelper:
    def __init__(self, path=os.path.dirname(os.getcwd()), type=txtType.w.name, encode='utf8'):
        self.path = path
        self.type = type
        self.encode = encode

    def write(self, strline):
        txtFile = open(self.path, self.type, encoding=self.encode)
        txtFile.write(strline)
        txtFile.write('\n')
        txtFile.close()

    def writealine(self, strline):
        txtFile = open(self.path, self.type, encoding=self.encode)
        txtFile.write(strline)
        txtFile.write('\n')
        txtFile.close()

    @staticmethod
    def joinStr(metadatas, datas, charStr):
        reStr = charStr.join(datas[meta] for meta in metadatas)
        return reStr


if __name__ == '__main__':
    m = ['楼层', '朝向']
    d = {'楼层': '2', '朝向': '南北', '面积': '88'}

    reStr = txthelper.joinStr(m, d, '\t')
    f = txthelper('D:\\gxd\\test.txt', 'a')
    f.writealine(reStr)
    f.writealine(reStr)
