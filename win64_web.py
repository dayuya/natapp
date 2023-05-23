
# -*- coding: UTF-8 -*-
# Version: v2.1
# auth: dayuya
# time: 2023/05/23
import os
import re
import json
import requests
from time import sleep
import psutil
import platform
from dotenv import load_dotenv
load_dotenv()

path = os.path.split(os.path.realpath(__file__))[0]
log_path = os.path.join(path,"natapp_web_log.txt")
app_path = os.path.join(path,"natapp.exe")
def update():
    #检查更新
    try:
        print("当前运行的脚本版本：" + str(version))
        r1 = requests.get("https://ghproxy.com/https://raw.githubusercontent.com/dayuya/natapp/main/win64_web.py").text
        r2 = re.findall(re.compile("version = \d.\d"), r1)[0].split("=")[1].strip()
        if float(r2) > version:
            print("发现新版本：" + r2)
            print("正在自动更新脚本...")
            if 'natapp.exe' in (p.name() for p in psutil.process_iter()):
                os.system("taskkill /im natapp.exe /f ")
            if os.path.exists(log_path):
                os.system("type nul > " + log_path)
            response = requests.get(
                "https://ghproxy.com/https://raw.githubusercontent.com/dayuya/natapp/main/win64_web.py")
            path_t = os.path.abspath(__file__)
            if response.status_code == 200:
                with open(path_t+".tmp", 'wb') as f:
                    f.write(response.content)
                # 用新代码替换当前脚本
                os.replace(path_t + ".tmp", path_t)
                print('Source code downloaded successfully.')
    except requests.exceptions.RequestException as e:
        pass

# 判断系统架构
def check_os():
    if platform.system() == 'Windows':
        print('当前系统为 Windows')
        if platform.machine() == 'x86':
            print('32 位 Windows 系统:'+platform.machine())
        elif platform.machine() == 'x86_64':
            print('64 位 Windows 系统:'+platform.machine())
        elif platform.machine() == 'AMD64':
            print('64 位 Windows 系统:' + platform.machine())
        else:
            print('Windows 系统:' + platform.machine())
    else:
        print('非 Windows 系统')

def process_check():
    print("正在检测穿透状态...")
    global url_g
    url_g = get_url()
    if url_g is not None:
        return True
    return False

# 执行程序
def go():
    commond = app_path + " -authtoken="+authtoken+" -loglevel=INFO -log=" + log_path
    if process_check():
        pushplus_bot("natap穿透通知", "web穿透地址：" + url_g)
        print("穿透程序已在运行...：%s" % url_g)
        return
    if os.path.exists(log_path):
        os.system("type nul > " + log_path)
    # 根据进程名判断进程是否存在
    if 'natapp.exe' in (p.name() for p in psutil.process_iter()):
        os.system("taskkill /im natapp.exe /f 2>nul")
    print("正在启动内网穿透...")
    os.system(f"start /B {commond} >NUL 2>NUL")
    sleep(5)
    if process_check():
        pushplus_bot("natapp穿透通知", "web穿透地址：" + url_g)
        print("启动内网穿透成功！：%s" % url_g)
    else:
        print("启动内网穿透失败...")

# 获取穿透url
def get_url():
    try:

        with open(log_path, encoding='utf-8') as f:
            log_content = f.read()
        reg = r"http://\S+"
        for i in re.findall(reg, log_content):
            if 'natappfree' in i:
                return i
    except:
        return None


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

if __name__ == '__main__':
    version = 2.1
    start=True
    try:
        authtoken = os.environ['natapp_authtoken_web']
    except:
        authtoken = ""
    try:
        PUSH_PLUS_TOKEN = os.environ['PUSH_PLUS_TOKEN']
    except:
        PUSH_PLUS_TOKEN = ""
    if len(authtoken)==0:
        start=False
        print("请添加环境变量：natapp_authtoken_web")
    if len(PUSH_PLUS_TOKEN)==0:
        print("未开启通知")
    update()
    #check_os()  检测架构去下载对应程序
    #下载对应程序
    #检测程序
    if start:  
        go()    



