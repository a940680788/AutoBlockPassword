import re
import subprocess
import time


#安全日志
secure = '/var/log/secure'
#黑名单文件
hostDeny = '/etc/hosts.deny'
#封禁阀值
password_error_num=5

#获取已存在的黑名单ip，变成字典
def getDent():
    #黑名单字典

    deniedDict = {}
    list = open(hostDeny).readlines()
    print(list)
    for ip in list:
        group = re.search(r'(\d+\.\d+\.\d+\.\d+)',ip)
        if group:
            print(group[1])
            deniedDict[group[1]] = '1'
            print(deniedDict)
    return deniedDict

#监控方法
def monitorLog(LogFile):
    #统计密码错误次数
    errorNumber={}
    #已经拉黑的ip
    ipDict=getDent()
    #读取安全日志
    popen = subprocess.Popen('tail -f '+LogFile,stdout=subprocess.PIPE,shell=True,stderr=subprocess.PIPE)
    #监控
    while True:
        time.sleep(0.5)
        line = popen.stdout.readline().strip()
        if line:
            group = re.search('Invalid user \w+ from (\d+\.\d+\.\d+\.\d)',str(line))
            #不存在的用户直接封ip
            if group and not ipDict.get(group[0]):
                subprocess.getoutput('echo \'all:{}\' >> {}'.format(group[1],hostDeny))
                ipDict[group[0]]='1'
                nowTime=time.strftime("%Y-%M-%d %H:%M:%S",time.localtime())
                print('{} 添加 ip:{} 进黑名单，原因无效用户名'.format(nowTime,group[1]))
                continue
            #用户名合法密码错误超过阀值
            group = re.search('Failed password for \w + from(\d+\.\d+\.\d+\.\d)',str(line))
            if group:
                ip = group[1]
                #统计ip错误次数
                if not errorNumber.get(ip):
                    errorNumber[ip]=1
                else:
                    errorNumber[ip]+=1
                #ip错误次数大于5
                if errorNumber[ip]>password_error_num and not ipDict.get(ip):
                    del errorNumber[ip]
                    subprocess.getoutput('echo \'all:{}\' >> {}'.format(ip,hostDeny))
                    ipDict[ip]='1'
                    nowTime=time.strftime("%Y-%M-%d %H:%M:%S",time.localtime())
                    print('{} 添加 ip:{} 进黑名单，原因密码错误次数超限'.format(nowTime,ip))

if __name__ == '__main__':
    monitorLog(secure)