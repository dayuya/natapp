# -*- coding: UTF-8 -*-
# Version: v1.1
# auth: dayuya
# time: 2023/05/24
import os
import re
import sys
import json
import requests
from time import sleep

path = os.path.split(os.path.realpath(__file__))[0]
log_path = os.path.join(path, "natapp_web_log.txt")
app_path = os.path.join(path, "natapp")

url_pattern = re.compile(r"http://\S+")
errors = {"Web服务错误", "此端口尚未提供Web服务", "无法连接到", "not found","<title>Web"}
# 检查更新
def update(version):
    print("当前运行的脚本版本：" + str(version))
    try:
        r1 = requests.get("https://ghproxy.com/https://raw.githubusercontent.com/dayuya/natapp/main/linux64_web.py").text
        r2 = re.findall(re.compile("version = \d.\d"), r1)[0].split("=")[1].strip()
        if float(r2) > version:
            print("发现新版本：" + r2)
            print("正在自动更新脚本...")
            os.system("killall natapp")
            os.system("ql raw https://ghproxy.com/https://raw.githubusercontent.com/dayuya/natapp/main/linux64_web.py &")
    except:
        pass

# 判断CPU架构
def check_os():
    r = os.popen('uname -m').read()
    if 'aarch64' in r or 'arm' in r:
        cpu = 'arm'
    elif 'x86_64' in r or 'x64' in r:
        cpu = 'amd64'
    else:
        print('穿透失败：不支持当前架构！')
        return
    print('获取CPU架构：' + r.replace('\n', ''))
    download_natapp(cpu)

# 下载主程序
def download_natapp(cpu):
    if not os.path.exists("natapp"):
        print("正在下载程序")
        res = requests.get("https://cdn.natapp.cn/assets/downloads/clients/2_3_9/natapp_linux_" + cpu + "/natapp")
        with open("natapp", "wb") as f:
            f.write(res.content)
        os.system("chmod +x natapp")

# 获取穿透url
def get_url():
    try:
        global url_g
        with open(log_path, encoding='utf-8') as f:
            log_content = f.read()
        for i in url_pattern.findall(log_content):
            if 'natappfree' in i:
#                 res = requests.get(i).text
#                 if any(error in res for error in errors):
#                     print(1)
#                     return None
                url_g = i
                return i 
    except Exception as e:
        print(e)
        return None


# 执行程序
def go():
    print("# 执行程序")
    commond = app_path + " -authtoken=" + authtoken + " -loglevel=INFO -log=" + log_path
    if get_url() is None:
        os.system("rm -f " + log_path)
        os.system("touch " + log_path)
        os.system("killall natapp")
        print("正在启动内网穿透...")
        os.system(commond)
        sleep(5)
        if get_url():
            print("启动内网穿透成功！：%s" % url_g)
            pushplus_bot("natapp穿透通知", "web穿透地址：" + url_g)
            
        else:
            print("启动内网穿透失败...")
    else:
        print("穿透程序已在运行...：%s" % url_g)
        pushplus_bot("natap穿透通知", "web穿透地址：" + url_g)
        


# push推送
def pushplus_bot(title, content):
    try:
        if not PUSH_PLUS_TOKEN:
            print("PUSHPLUS服务的token未设置！！\n取消推送！")
            return
        print("PUSHPLUS服务启动！")
        url = 'http://www.pushplus.plus/send'
        data = {
            "token": PUSH_PLUS_TOKEN,
            "title": title,
            "content": content
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=url, data=body, headers=headers).json()
        if response['code'] == 200:
            print('推送成功！')
        else:
            print('推送失败！')
    except Exception as e:
        print(e)

def check_env_var(var_name, message):
    value = os.environ.get(var_name, '')
    if not value:
        print(message)
    return value

if __name__ == '__main__':
    version = 1.1
    start = True
    authtoken = check_env_var('natapp_authtoken_web', "请添加环境变量：natapp_authtoken_web")
    PUSH_PLUS_TOKEN = check_env_var('PUSH_PLUS_TOKEN', "未开启通知 请添加环境变量:PUSH_PLUS_TOKEN")
    if not authtoken:
        start = False
    update(version)
    check_os()
    go()
