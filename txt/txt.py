from common.base import *


class txthelper:
    def __init__(self, path=os.path.dirname(os.getcwd()),name='content.txt', type=txtType.w.name, encode='utf8'):
        self.path = path
        self.type = type
        self.encode = encode

        if not os.path.exists(path):
            os.makedirs(path)
        self.txt=open(self.path+name, self.type, encoding=self.encode)

    def open(self):
        return self.txt

    def write(self, strline):
        txtFile = self.txt
        txtFile.write(strline)
        txtFile.write('\n')

    def writealine(self, strline):
        txtFile = self.txt
        txtFile.write(strline)
        txtFile.write('\n')

    def close(self):
        self.txt.close()

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
    f.close()
