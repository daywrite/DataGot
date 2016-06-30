from common.base import *
from enum import Enum

# w     以写方式打开，
# a     以追加模式打开 (从 EOF 开始, 必要时创建新文件)
# r+     以读写模式打开
# w+     以读写模式打开 (参见 w )
# a+     以读写模式打开 (参见 a )
# rb     以二进制读模式打开
# wb     以二进制写模式打开 (参见 w )
# ab     以二进制追加模式打开 (参见 a )
# rb+    以二进制读写模式打开 (参见 r+ )
# wb+    以二进制读写模式打开 (参见 w+ )
# ab+    以二进制读写模式打开 (参见 a+ )
txtType = Enum('txtType', 'w a r+ w+ a+ rb wb ab rb+ wb+ ab+')


class txthelper:

    def __init__(self, path=os.path.dirname(os.getcwd()), type=txtType.w.name):
        self.path = path
        self.type = type

    def write(self,strline):
        txtFile=open(self.path, self.type)
        txtFile.write(strline)
        txtFile.close()

    def writealine(self,strline):
        txtFile= open(self.path, self.type)
        txtFile.write(strline)
        txtFile.write('\n')
        txtFile.close()

    @staticmethod
    def joinStr(metadatas, datas, charStr):
        reStr = charStr.join(datas[meta] for meta in metadatas)
        return reStr

if __name__ == '__main__':
    m=['楼层','朝向']
    d={'楼层':'2','朝向':'南北','面积':'88'}

    reStr=txthelper.joinStr(m,d,'\t')
    f=txthelper('D:\\gxd\\test.txt','a')
    f.writealine(reStr)
    f.writealine(reStr)






