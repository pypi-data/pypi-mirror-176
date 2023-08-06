#import logging
import os
#import logging.handlers
import datetime
import importlib
import re
logging=importlib.import_module("logging")
logging.handlers=importlib.import_module("logging.handlers")

try:
    host_ip=os.popen("curl ifconfig.me").read()
except Exception as err:
    host_ip=""
try:
    mid=str(os.popen("head -1 /proc/self/cgroup|cut -d/ -f3|cut -c8-19").read()).replace("\n","")
except Exception as ex:
    print(ex.args)
    mid = ""

#----------脱敏开始
def ppat(pat1,data,num=1):
    if(int(num)==1):
        rst=re.compile(pat1,re.S).findall(data)
        if(len(rst)>0):
            rst=rst[0]
        else:
            rst=""
    else:
        rst=re.compile(pat1,re.S).findall(data)
        if(len(rst)>0):
            rst=rst
        else:
            rst=[]
    return rst
def encode(data):
    new_data = "***"+data[-4:]
    return new_data
def data_desensitization(info):
    pat_rules=['\d{17}',#身份证
               r'1(?:3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8\d|9\d)\d{8}',#手机号
               '\d{3}-\d{7}',#电话号
               '\w{1}@.*?\..{3}',#邮箱
               '\d{16}',#银行卡号1
               '\d{19}',#银行卡号2
               #'\d{4}-\d{2}-\d{2}',#出生年月1
               #'\d{8}',#出生年月2
               ]
    for pat in pat_rules:
        pat_rst=ppat(pat,info,0)
        for line in pat_rst:
            info=info.replace(line,encode(line))
    return info
#----------脱敏完成

class WeLog():
    first_signal=[]
    init_config={"path":"","filename_pre":"","filename_suffix":""}
    date_info={"ori":""}
    def __init__(self):
        self.log=logging
    def init_log(self,path,filename):
        self.log=importlib.reload(self.log)
        if os.path.exists(path):
            mode = 'a'
        else:
            mode = 'w'
        self.log.basicConfig(
            level=self.log.INFO, 
            format="host_ip:"+str(host_ip)+'  mid:'+str(mid)+'  '+'%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', 
            filename=path,
            filemode=mode, 
        )
        return self.log

    def init(self,path,filename):
        self.init_config["path"]=path
        self.init_config["filename_pre"]=filename.split(".log")[0]
        self.init_config["filename_suffix"]=filename.split(".")[-1]
        #fullpath = os.path.join(path, filename)
        #log = init_log(fullpath,filename)
        #return log

    def whether_init_log(self,ori_date):
        cur_date=str(datetime.datetime.now()).split(" ")[0]
        ###cur_date=str(datetime.datetime.now()).replace(" ","").replace(":","")
        ###print(cur_date)
        if(ori_date==cur_date):
            #同一天，不切
            return False
        else:
            #不同一天，切
            return True
    def whether_first_running(self):
        if('first_signal' in self.first_signal):
            return False
        else:
            self.first_signal.append("first_signal")
            return True

    def info(self,content):
        try:
            try:
                #脱敏
                content=data_desensitization(content)
                print(content)
            except Exception as err:
                print(err)
            if(self.init_config["path"]==""):
                print("请先配置log文件信息")
                return 
            if("log" != self.init_config["filename_suffix"]):
                print("日志文件必须以log结尾，请重新配置正确")
                return 
            if(self.whether_first_running()):
                #首次运行
                ###print("首次运行")
                cur_date=str(datetime.datetime.now()).split(" ")[0]
                ###cur_date=str(datetime.datetime.now()).replace(" ","").replace(":","")
                self.date_info={"ori":cur_date}
                filename=self.init_config["filename_pre"]+"_"+cur_date+".log"
                fullpath = os.path.join(self.init_config["path"], filename)
                self.log = self.init_log(fullpath,filename)
            else:
                #非首次运行
                ###print("非首次运行")
                if(self.whether_init_log(self.date_info["ori"])):
                    #跨天，重新初始化
                    cur_date=str(datetime.datetime.now()).split(" ")[0]
                    ###cur_date=str(datetime.datetime.now()).replace(" ","").replace(":","")
                    self.date_info={"ori":cur_date}
                    filename=self.init_config["filename_pre"]+"_"+cur_date+".log"
                    ###print(filename)
                    fullpath = os.path.join(self.init_config["path"], filename)
                    self.log = self.init_log(fullpath,filename)
            self.log.info(content)
        except Exception as err:
            print(err)

def instance():
    return WeLog()
