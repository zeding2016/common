# -*- coding:utf-8 -*-
__author__ = 'zeding'
__mtime__ = '2017/10/9'

# 一些常用的方法

import asyncio
import time
from pathlib import Path
from pathlib import PurePath
import shutil
from logzero import setup_logger
import logging
from functools import wraps
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


# import StringIO
# ------------------------------------------------------------------------------
# Python2
# class MyClass( object ):
#     __metaclass__ = Singleton


# Python3
# class MyClass(metaclass=Singleton):
#    pass



def format_(f, n):
    if round( f ) == f:
        m = len( str( f ) ) - 1 - n
        if f / (10 ** m) == 0.0:
            return f
        else:
            return float( int( f ) / (10 ** m) * (10 ** m) )
    return round( f, n - len( str( int( f ) ) ) ) if len( str( f ) ) > n + 1 else f


class Singleton( type ):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super( Singleton, cls ).__call__( *args, **kwargs )
        return cls._instances[cls]


# ------------------------------------------------------------------------------
# class Singleton( object ):
#     _instance = None
#
#     def __new__(cls, *args, **kw):
#         if not cls._instance:
#             cls._instance = super( Singleton, cls ).__new__( cls, *args, **kw )
#         return cls._instance
#
#
# class MyClass( Singleton ):
#     a = 1
# ------------------------------------------------------------------------------

def singleton(cls):
    '''
    使用装饰器（decorator）动态地修改一个类或函数的功能，使其只能生成一个实例
    :param cls:
    :return:
    '''
    instances = {}
    
    @wraps( cls )
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls( *args, **kw )
        return instances[cls]
    
    return getinstance


class myLog( object ):
    '''日志模块的封装,该log是python3.0版本的'''
    
    def __init__(self, logName, path='.', clevel=logging.INFO):
        '''
    
        :param logName:  log的文件名
        :param path:  log路径
        :param clevel: log的等级
        '''
        self.logger = setup_logger( name=logName, logfile=path, level=clevel )
    
    def debug(self, message):
        self.logger.debug( message )
    
    def info(self, message):
        self.logger.info( message )
    
    def warn(self, message):
        self.logger.warn( message )
    
    def error(self, message):
        self.logger.error( message )
    
    def cri(self, message):
        self.logger.critical( message )




class myMail( object ):
    _to_list = ['dingze4321@sina.com', 'dingze647@pingan.com.cn']
    
    def __init__(self, subject):
        '''
        :param subject: 主题
        '''
        try:
            self._server = smtplib.SMTP()
            self._msg = MIMEMultipart()
        except Exception as e:
            print(e)
            return
        
        self.subject = subject
        self._mail_user = 'test_mifi@sina.com'  # 用户名
        self._mail_pass = 'abcd1234'  # 口令
    
    
    def __del__(self):
        try:
            self._server.close()
        except Exception as e:
            print( e )
       
    
    
    def setMail(self, content, att=None, subtype=u'html'):
        '''
        :param att:  附件 必须为列表的格式
        :param content:  内容
        :param subtype: 附件的格式
        :return:
        '''
        
        if att:
            assert type( att ) == list
            if len( att ) != 0:
                for i in att:
                    name = str( i ).split( r'/' )[-1]
                    att1 = MIMEText( open( i, 'rb' ).read(), 'base64', 'utf-8' )
                    att1["Content-Type"] = 'application/octet-stream'
                    att1["Content-Disposition"] = 'attachment; filename="attachment{}"'.format(
                        name )  # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
                    self._msg.attach( att1 )
        
        self._msg.attach( MIMEText( content, _subtype=subtype, _charset='utf-8' ) )
    
    
    
    def sendMail(self, sender='MiFi',rec=_to_list):
        ''''''
        self._msg['To'] = ";".join( rec )
        self._msg['Subject'] = self.subject  # 设置主题
        self._msg['From'] = self._mail_user
        # self._msg['To'] = Header('hello','utf-8')
        # self._msg['Subject'] = Header(self.subject,'utf-8')
        # self._msg['From'] = Header('测试','utf-8')
        try:
            self._server.connect( 'smtp.sina.com' )
            self._server.starttls()
            self._server.login( self._mail_user, self._mail_pass )
            self._server.sendmail( self._mail_user, self._to_list, self._msg.as_string() )
        
        except Exception as e:
            print( e )
            return False
        finally:
            self._server.close()




class myProject( object ):
    '''构建一个项目'''
    _path_s = Path().cwd()  # 当前目录
    
    #
    # def __new__(cls, *args, **kwargs):
    #     super(myProject,cls).__new__(cls)
    #
    
    def __init__(self, name='myDemo'):
        # 确保每次删除上一次的创建目录
        path_iter = self._path_s.iterdir()  # 遍历目录
        for path in path_iter:
            if str( path ).endswith( 'mk.txt' ):
                os.remove( str( path ) )
        self.name = name
        self.log = myLog( logName=__name__, path=str( self.__setLogName() ) )
    
    def __del__(self):
        self.log.info( ".........end........." )
    
    def __setLogName(self, name='mk'):
        _name = '{0}{1}.txt'.format( str( time.strftime( '%Y%m%d%H%M%S', time.localtime( time.time() ) ) ), name )
        return PurePath( self._path_s ) / _name
    
    def mkMyProject(self):
        '''
        :param name: 测试框架的名称
        :return:
        '''
        # self.log = self.setLog(
        #     logName=__name__, path=''
        # )
        global allFile
        self.log.info( ".........start making my Project........." )
        path_s = self._path_s
        
        p = PurePath( path_s ) / self.name  # 主入口
        # 测试框架结构
        # myDemo-
        #    |-Data，所有测试数据相关，包括测试环境，测试数据
        #    |
        #    |-Po 所有基础类
        #    |
        #    |-Public 所有公共的方法比如测试报告脚本
        #    |
        #    |-Result  测试结果
        #    |
        #    |-Log  测试log
        #    |
        #    |-Case  测试case
        #    |
        #    |-main 运行入口
        
        
        
        p_Data, p_Po, p_Public, p_Result, p_Log, p_Case, p_main = PurePath( path_s ) / self.name / 'Data', \
                                                                  PurePath( path_s ) / self.name / 'Po', \
                                                                  PurePath( path_s ) / self.name / 'Public', \
                                                                  PurePath( path_s ) / self.name / 'Result', \
                                                                  PurePath( path_s ) / self.name / 'Log', \
                                                                  PurePath( path_s ) / self.name / 'Case', \
                                                                  PurePath( path_s ) / self.name / 'main'
        
        allFile = [p_Data, p_Po, p_Public, p_Result, p_Log, p_Case, p_main]
        
        try:
            # 优先创建主文件
            # 如果文件夹存在，则删除对应的文件夹，重新创建
            if not Path( PurePath( p ) ).exists():
                Path( PurePath( p ) ).mkdir()
            
            else:
                self.log.warn( "正在递归删除文件夹" )
                
                shutil.rmtree( str( p ) )
                
                Path( PurePath( p ) ).mkdir()
            
            if Path( p ).exists():
                self.log.info( "创建主文件夹成功" )
            else:
                self.log.error( '创建主文件夹失败' )
            
            fileAll = []
            for i in allFile:
                fileAll.append( PurePath( i ) / '__init__.py' )
                Path( PurePath( i ) ).mkdir()
                self.log.info( '{}....success!!'.format( PurePath( i ) ) )
            
            if len( fileAll ) != 0:
                for j in fileAll:
                    # self.log.info( '开始创建:{}'.format( PurePath( j) ) )
                    Path( PurePath( j ) ).touch()
                    self.log.info( '{}....success!!'.format( PurePath( j ) ) )
            else:
                self.log.debug( "长度为0" )
            
            self.log.info( "..................success!!!............." )
        except Exception as e:
            self.log.error( e )
            self.log.error( "错误" )
    
    def __getLogPath(self, _name='main.txt'):
        '''return log's path'''
        # return PurePath( self.path_s ) / self.name / 'Log'/'log.txt'
        return PurePath( self._path_s ) / self.name / 'Log' / _name
    
    def setLog(self, logName):
        '''返回一个log实例'''
        self.log.info( "创建了log实例：{}".format( logName ) )
        return myLog( logName, path=str( self.__getLogPath( _name=logName ) ) )
    
    def getPath(self, path):
        '''return path for project'''
        if path not in ['Data', 'Po', 'Public', 'Result', 'Log', 'Case', 'main']:
            return None
        return PurePath( self._path_s ) / self.name / path


class myResultForEmail( object ):
    '''拼接为html格式的邮件'''
    
    def __init__(self, subject, startTime, endTime):
        '''
        :param subject: 报告的名称
        '''
        self.sub = subject
        self._moudles = []
        self._cases = []
        self._AllCases = []
        self._totalNum = 0
        self._passNum = 0
        self._failNum = 0
        self._errNum = 0
        self._totalTime = 0
        self.startTime, self.endTime = startTime, endTime
    
    def setAll(self, cases):
        '''把所有的case传入进来做分析,读取文件的形式
            demo：case=['testmoudle-testCase-status-time-details']
            如果status是pass则details为None
        '''
        self._cases = cases
    
    def getInfo(self, con):
        '''
        
        :param con: 1、module测试模块     2、cases 所有的测试用例  包含了  pass   fail    error   time  模块名称
        :return:
        '''
        if con == 1:
            return self._moudles
        if con == 2:
            return self._cases
    
    
    def _setDiv1(self):
      
        _div1 = u''' <!DOCTYPE html>
        <html xmlns="http://www.w3.org/1999/xhtml">
	    <head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width,initial-scale=1.0">
		
		<title></title>
	    <body style="padding:0">
                    <div id="1" style="text-align: center">
			        <h1 style="color: deeppink">{}</h1>
		            </div>
		        '''.format( self.sub )
        
        return _div1
    
    
    
    def _setTime(self):
        '''
        
        :param s: 开始时间
        :param e: 结束时间
        :return:
        '''
        _time = u'''
        <ul style="padding: 0;list-style: none;">
			<li>开始时间：{0}</li>
			<li>结束时间：{1}</li>
		</ul>
        '''.format( self.startTime, self.endTime )
        return _time
    
    def _setDiv2(self, p, f, e):
        '''
        
        :param p:  pass%
        :param f: fail%
        :param e: e%
        :return:
        '''
        
        _div2 = u'''
        <div >
			<div style="width:{}%;height: 15px;background: green ;display: inline-block;float: left;text-align: center;font-size: 10px;" >{}%</div>
			<div style="width:{}%;height: 15px;background: red ;display: inline-block;margin-left: 0;float: left;text-align: center;font-size: 10px" >{}%</div>
			<div style="width:{}%;height: 15px;background: grey ;display: inline-block;float: left;text-align: center;font-size: 10px" >{}%</div>
		</div>'''.format( p, p, f, f, e, e )
        
        return _div2
    
    def _setTable(self, body):
        '''
        
        :param _moudle:
        :param case:
        :param total:
        :return:
        '''
        _table = u'''
       
	    
        <table width="100%" border="1" cellspacing="0" class="report" style="border-collapse: collapse;text-align: center;">
        <tr class="testHeader">
				<th width="60%">测试moudle/测试case</th>
				<th>总数</th>
				<th>成功</th>
				<th>错误</th>
				<th>失败</th>
				<th>耗时</th>
		</tr>
		{}
        </table>
        </body>
                    </html>

        '''.format( body )
        return _table
    
    def _setTestMoudle(self, s, t, p, f, e, time):
        '''
        testModle
        :param t:
        :param p:
        :param f:
        :param e:
        :return:
        '''
        
        _testMoudle = u'''
        <tr class="testMoudle">
				<td>{0}</td>
				<td>{1}</td>
				<td>{2}</td>
				<td>{3}</td>
				<td>{4}</td>
				<td>{5}s</td>
				
		</tr>
        '''.format( s, t, p, f, e, time )
        self._moudles.append( s )
        return _testMoudle
    
    def _setTestCase(self, case, stat, d, t):
        '''
        :param case:
        :param stat:
        :param t:
        :return:
        '''
        _s = self._setCaseDetils( d )
        if stat == 'pass':
            _testCase = '''
                   <tr class="testCase">
                   <td>{0}</td>
                   <td colspan="4">{1}</td>
                   <td>{2}s</td>
                   </tr>
                   '''.format( case, stat, t )
        
        else:
            _a = '''
                <a href="#" style="color: red;text-decoration: none;" onclick="if (this.nextElementSibling.style.visibility =='hidden'){alert(1);this.nextElementSibling.style.visibility ='visible';this.nextElementSibling.style.display=''}else{this.nextElementSibling.style.visibility ='hidden';this.nextElementSibling.style.display='none'}">
               %s</a> %s
               ''' % (stat, _s)
            _testCase = '''
                   <tr class="testCase">
                   <td>{0}</td>
                   <td colspan="4">{1}</td>
                   <td>{2}</td>
                   </tr>
                   '''.format( case, _a, t )
        
        return _testCase
    
    def _setCaseDetils(self, details):
        _details = u'''<pre style="visibility:hidden;display: none;clear: both">{}</pre>'''.format( details )
        return _details
    
    def _setTotal(self, total, p, f, e, t):
        _total = u'''
        <tr class="end">
				<td>总结</td>
				<td>{}</td>
				<td>{}</td>
				<td>{}</td>
				<td>{}</td>
				<td >{}s</td>
		</tr>
		      
        '''.format( total, p, f, e, t )
        
        return _total
    
    def _setTotalReport(self):
        '''
        case=['testmoudle-testCase-status-time-details']
        _data={'testMoudle':[(case1,pass,time,details),(case2,fail,time,details).....]}
        :return:
        '''
        _data = {}
        # _result = {} #{'testMoudle'：[total,pass,fail,wrong]} 全部结果的显示 为int型
        # _totalReport =[]
        _one = None
        try:
            if self._cases:
                for i in self._cases:
                    
                    l = str( i ).split( "-" )
                    if l[0] not in _data.keys():
                        # 并初始化
                        _data[l[0]] = []
                    _data[l[0]].append( [l[1], l[2], l[3], l[4]] )
            
            else:
                print( "无相关case" )
        except Exception as e:
            print( e )
            pass
        
        _one = ""
        for i in _data.keys():
            _t, _p, _f, _e, _time = 0, 0, 0, 0, 0
            _TestCase, _TestMoudle = "", ""
            _t = len( _data[i] )
            self._totalNum += len( _data[i] )
            for k in _data[i]:
                
                # j是对应moudle的所有cases数目列表 case, stat, d, t
                #
                # print( k )
                # print( k[0], k[1], k[3], k[2] )
                _TestCase = _TestCase + self._setTestCase( k[0], k[1], k[3], k[2] )
                self._totalTime += int( k[2] )
                _time += int( k[2] )
                if k[1] == 'pass':
                    
                    _p += 1
                    self._passNum += 1
                elif k[1] == 'fail':
                    
                    _f += 1
                    self._failNum += 1
                elif k[1] == 'error':
                    
                    _e += 1
                    self._errNum += 1
            
            _TestMoudle = self._setTestMoudle( i, _t, _p, _f, _e, _time )
            
            _one += (_TestMoudle + _TestCase)
        
        _one = _one + self._setTotal( self._totalNum, self._passNum, self._failNum, self._errNum, self._totalTime )
        
        # 拼接报告的body
        return self._setDiv1() + self._setTime() + self._setDiv2(
            (100 * format_( (self._passNum / self._totalNum), 5 )),
            (100 * format_( (self._failNum / self._totalNum), 5 )),
            (100 * format_( (self._errNum / self._totalNum), 5 )) ) \
               + self._setTable( _one )
    
    
    def infoReport(self):
        
        return self._setTotalReport()
    
    
    






# s = time.asctime( time.localtime( time.time() ) )
#
# e = time.asctime( time.localtime( time.time() ) )
#
# a = myResultForEmail(subject="hello2017",startTime=str(s),endTime=str(e))
# # #
#
#
# case = ['testmoudle1-testCase1.1-pass-11-None', 'testmoudle1-testCase1.2-pass-12-None',
#         'testmoudle1-testCase1.3-error-13-wrong',
#         'testmoudle2-testCase2.1-fail-14-asdfafagjakajfjjajdadajjgnaa',
#         'testmoudle3-testCase3.1-fail-14-asdfafagjakaeeejfjjajdadajjgnaa',
#         'testmoudle3-testCase3.2-fail-14-asdfafagjakrrajfjjajdadajjgnaa',
#         'testmoudle4-testCase4.1-fail-14-asdfafagjakyuajfjjajdadajjgnaa'
#         ]
#
#
#
# print(a.infoReport())


# finally:
#     if _data:
#         self._moudles = _data.keys()
#         for i in _data.keys():
#             for j in _data[i]:
#                 for k in j:
#                     if k[]
#
# self._passNum = 0
# self._failNum = 0
# self._errNum = 0
#

# a = myMail( subject="just a demo" )
# a.setMail( content=con )
# a.sendMail()
#


# print(float(123.456))

#
# class sendResult(myMail):
#     '''
#     表头
#
#     '''
#     def __init__(self,subject,Time):
#         super(sendResult,self).__init__(subject)
#         self.Time = Time
#
#     def setContent(self):
