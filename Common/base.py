# 导入公共模块
import os, sys, time
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

# url请求基本元素
URL_REQUEST_headers = {'Accept': '*/*',
                       'Accept-Encoding': 'gzip, deflate',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36 LBBROWSER',
                       'Connection': 'keep-alive'}

URL_REQUEST_Metas = ('省', '城市', '行政区', '区域', '街道路', '路牌号',
                     '小区名', '小区别名',
                     '楼栋名', '楼栋别名','楼栋街牌号',
                     '单元名', '单元别名', '单元街牌号',
                     '楼层名', '楼层别名',
                     '房间名', '房间别名', '房间街牌号',
                     '小区坐标中心点坐标', '小区边界坐标', '楼栋坐标', '单元坐标',
                     '数据来源', '开发商',
                     '总建筑面积', '占地面积',
                     '房屋所有权证号', '总户数', '车位数量', '绿化率', '容积率', '总栋数',
                     '土地使用权证号', '发证日期', '地上层数', '地下层数', '建筑高度', '规划用途', '户型','建筑面积', '套内面积', '公摊面积',
                     '按建面单价', '按套内面单价', '总价', '朝向',
                     '小区id', '小区评估系数', '小区评估参数', '竣工年限', '楼盘案例均价',
                     '楼栋id', '建筑结构', '房号', '建筑类别', '房屋结构', '房屋户评估系数', '扩展信息', 'STR_ORDER')

URL_REQUEST_Enum_Metas = Enum('URL_REQUEST_Enum_Metas', '省 城市 行政区')

URL_REQUEST_BASE_Metas=[URL_REQUEST_Enum_Metas.省.name]