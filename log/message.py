# -*- coding: utf-8 -*-
#coding:utf-8
class DEBUG:
    URLDISPATCH_DISPATCH = '分发消息!调用解析类%s, 解析方法%s'
    WORK_GETJOB = '线程%d获取任务%s'
    pass

class INFO:
    CUR_OS = '运行操作系统'
    WINDOWS = 'Windows'
    LINUX = 'Linux'

    SERVICE_MONITOR_START = '准备启动监控服务!'
    SERVICE_MONITOR_STARTING = '正在启动监控服务...'
    SERVICE_MONITOR_STARTTED = '监控服务已启动!'
    SERVICE_MONITOR_STOP= '准备停止监控服务!'
    SERVICE_MONITOR_STOPPING = '正在停止监控服务...'
    SERVICE_MONITOR_STOPPED = '监控服务已停止!'
    SERVICE_MONITOR_RUNNING = '监控服务监控中...'
    SERVICE_MONITOR_ENDING = '监控服务运行完毕!'

    URLDISPATCH_REG = '注册%s处理类成功!'
    URLDISPATCH_START = 'URL消息分发解析模块启动!'

    CLIENT_CLOSED = '客户端程序关闭!'

class WARN:

    URLDISPATCH_PARSERS_TYPE_ERR = '注册%s解析器失败!'
    URLDISPATCH_PARSERS_SUB_ERR = '%s解析类必须从ParserBase继承!'
    URLDISPATCH_MESSAGE_DISCARD = '消息丢弃!'
    URLDISPATCH_MESSAGE_FORMATERR = '消息格式不合法, 消息将被丢弃!'
    URLDISPATCH_MESSAGE_PARSERERR = '没有找到%s解析对象, 消息将被丢弃!'
    URLDISPATCH_MESSAGE_PARSEREXEERR = '执行解析脚本出错, 消息将被丢弃, 任务url:%s, 消息信息:s%, 异常信息:%s!'
    URLDISPATCH_ERROR = '解析过程出错, 任务url:%s, 错误信息:s%, 消息将被丢弃!'

    CLIENT_MESSAGE_FAILED = '任务分发处理失败,将此消息返回服务器重新分发,url:%s!'

    pass

class ERROR:
    IMPORT_ERROR='导入包失败'
    CLIENT_NEWFAILE = '实例化消息失败,消息将被丢弃,异常信息:%s,异常类型:%s'
    CLIENT_RETURNURLS_FAILE = '网站解析程序,返回解析结果无法返回服务器!返回内容:%s, 错误信息:%s, 异常类型:%s'
    CLIENT_CONNECT_FAILE = '连接服务器失败,可能是由于服务器没有启动或网络问题, %d秒后重试!'



class SERVICE:
    SERVICE_MONITOR = 'MonitorService'                                #服务名
    SERVICE_MONITOR_NAME = '分布式爬虫服务器监控服务'                 #服务显示名称
    SERVICE_MONITOR_DESCRIPTION = '监控分布式服务器运行情况'          #服务描述


