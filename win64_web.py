# -*- coding: UTF-8 -*-
# Version: v2.4
# auth: dayuya
# time: 2023/05/24
import os
import re
import json
import requests
from time import sleep
import psutil
import platform
from dotenv import load_dotenv
import subprocess
import psutil
load_dotenv()
import zipfile
def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        print('This is not zip')
        
path = os.path.split(os.path.realpath(__file__))[0]
log_path = os.path.join(path, "natapp_web_log.txt")
app_path = os.path.join(path, "natapp.exe")

def update():
    # 检查更新
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
                with open(path_t + ".tmp", 'wb') as f:
                    f.write(response.content)
                # 用新代码替换当前脚本
                os.replace(path_t + ".tmp", path_t)
                print('Source code downloaded successfully.')
    except requests.exceptions.RequestException as e:
        pass

# 判断系统架构
def check_os():
    if platform.system() == 'Windows':
        if platform.machine() in ['x86', 'x86_64', 'AMD64', 'amd64']:
            print('64 位 Windows 系统:' + platform.machine())
            cpu = "amd64"
        elif platform.machine() in ['AMD', 'AMD32']:
            print('64 位 Windows 系统:' + platform.machine())
            cpu = "386"
        else:
            print('Windows 系统:' + platform.machine())
            cpu = platform.machine()
        download_natapp(cpu)
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
    commond = app_path + " -authtoken=" + authtoken + " -loglevel=INFO -log=" + log_path
    if process_check():
        pushplus_bot("natap穿透通知", "web穿透地址：" + url_g)
        print("穿透程序已在运行...：%s" % url_g)
        return
    if os.path.exists(log_path):
        os.system("type nul > " + log_path)
    # 根据进程名判断进程是否存在
    if any(p.name() == 'natapp.exe' for p in psutil.process_iter()):
        os.system("taskkill /im natapp.exe /f 2>nul")

    print("正在启动内网穿透...")
    os.system(f"start /B {commond} >NUL 2>NUL")
    sleep(2)
    if process_check():
        pushplus_bot("natapp穿透通知", "web穿透地址：" + url_g)
        print("启动内网穿透成功！：%s" % url_g)
    else:
        print("启动内网穿透失败...")

# 下载主程序
def download_natapp(cpu):
    if not os.path.exists("natapp.exe"):
        print(cpu)
        res = requests.get(
            f"https://cdn.natapp.cn/assets/downloads/clients/2_3_9/natapp_windows_{cpu}_2_3_9.zip?version=20230407")
        with open("natapp.zip", "wb") as f:
            f.write(res.content)
            print("下载完成")
        # dst_dir 目标文件夹
        name = "natapp.zip"  # 在这里修改需要解压的文件夹
        unzip_file(zip_src="./" + name, dst_dir="./")
        os.remove("./" + name)  # 删除原始zip文件

# 获取穿透url
def get_url():
    try:
        with open(log_path, encoding='utf-8') as f:
            log_content = f.read()
        reg = r"http://\S+"
        for i in re.findall(reg, log_content):
            if 'natappfree' in i:
                res = requests.get(i).text
                # 使用集合来存储可能出现的错误信息，提高查找效率
                errors = {"Web服务错误", "此端口尚未提供Web服务", "无法连接到", "not found"}
                # 使用any函数来判断res中是否包含任意一个错误信息，简化逻辑判断
                if any(error in res for error in errors):
                    # 使用next函数来查找名为natapp.exe的进程，如果找不到则返回None
                    process = next((p for p in psutil.process_iter() if p.name() == "natapp.exe"), None)
                    # 如果找到了进程，则杀死它，并重定向错误输出到nul
                    if process:
                        subprocess.run(["taskkill", "/im", "natapp.exe", "/f"], stderr=subprocess.DEVNULL)
                    return None
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
    version = 2.4
    start = True
    try:
        authtoken = os.environ['natapp_authtoken_web']
    except:
        authtoken = ""
    try:
        PUSH_PLUS_TOKEN = os.environ['PUSH_PLUS_TOKEN']
    except:
        PUSH_PLUS_TOKEN = ""
    if len(authtoken) == 0:
        start = False
        print("请添加环境变量：natapp_authtoken_web")
    if len(PUSH_PLUS_TOKEN) == 0:
        print("未开启通知 请添加环境变量:PUSH_PLUS_TOKEN")
    update()
    check_os()
    if start:
        go()
