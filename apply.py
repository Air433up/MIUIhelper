# GitHub: https://github.com/azurstar/MIUIhelper

import time
from Apply.apply import Apply
import login
import json,os

log_path = "ApplyLog.txt"

def log(value="\n"):
    f = open(log_path,"a+",encoding="utf-8")
    print(value)
    print(value,file=f)
    f.close()

def main():
    print("GitHub: https://github.com/azurstar/MIUIhelper")
    input("是否已在accounts.json填入账号和申请机型, 回车确认...")
    planIds = ["10001","10002","10003"]
    with open("Apply/data/accounts.json","r",encoding="utf-8") as r: accounts = json.load(r)
    for Account in accounts:
        account = Account["account"]
        password = Account["password"]
        try:
            WebCookie = login.Web(account=account,password=password)
            log(f"\n{account}登录成功!")
        except:
            log(f"\n{account}登录失败...")
            continue
        Devices = Account["devices"]
        for planId in planIds:
            devices = Devices[planId]
            if devices == []:continue
            a = Apply()
            a.WebCookie = WebCookie
            a.planId = planId
            for device in devices:
                a.device = device
                try:a.run()
                except:print(f"未知原因导致{device}申请失败...")

def available():
    with open("Apply/data/accounts.json","r",encoding="utf-8") as r: accounts = json.load(r)
    Account = accounts[0]
    account = Account["account"]
    password = Account["password"]
    taskname = {
        "10001":"开发版公测",
        "10002":"开发版内测",
        "10003":"稳定版内测"
    }
    planIds = ["10001","10002","10003"]# ["10001","10002","10003"]
    try:
        with open("Apply/data/available.json","r",encoding="utf-8") as r:Devices = json.load(r)
        Devices["10001"]
    except:
        Devices = {
            "10001":[],
            "10002":[],
            "10003":[]
        }

    try:WebCookie = login.Web(account=account,password=password)
    except:
        log("登录失败,无法检测可用设备,有以下解决方法...")
        log("1.在Apply/data/accounts.json的第一栏填入账号密码")
        log("2.在浏览器登录小米社区,通过验证码校验")
        exit()
    with open("Apply/data/devices.json","r",encoding="utf-8") as r: devices = json.load(r)
    for planId in planIds:
        tt = 0
        try:startcode = Devices[planId][-1]
        except:startcode = "代号名称"
        log()
        for device in devices:
            if startcode == device["code"]:tt+=1
            if tt == 0:continue
            a = Apply()
            a.WebCookie = WebCookie
            a.device = device["code"]
            if device["code"] in Devices[planId]:continue
            a.planId = planId
            a.Sign()
            applyInfo = a.applyInfo
            time.sleep(1)
            if applyInfo["devices"] != []:
                Devices[planId].append(device["code"])
                print(f'{taskname[planId]} {device["name"]} 可用!')
                with open("Apply/data/available.json","w",encoding="utf-8") as w:json.dump(Devices,fp=w,ensure_ascii=False,indent=2)
                continue
            print(f'{taskname[planId]} {device["name"]} 不可用!')

def ChoiceDevice():
    with open("Apply/data/devices.json","r",encoding="utf-8") as r: devices = json.load(r)
    with open("Apply/data/available.json","r",encoding="utf-8") as r:Devices = json.load(r)
    taskname = {
        "10001":"开发版公测",
        "10002":"开发版内测",
        "10003":"稳定版内测"
    }
    planIds = ["10001","10002","10003"]
    print("\n选择需要申请的内测...")
    for planId in planIds:
        print(f"{planIds.index(planId)}.{taskname[planId]}")
    planIdindex = str(input("请输入选项索引:"))
    print("\n寻找可用设备...")
    uplanId = planIds[int(planIdindex)]
    usableDevices:list = Devices[uplanId]
    t = 0
    print("\n以下是可用设备:")
    for usableDevice in usableDevices:
        column = 0
        DeviceName:str
        for deviceInfo in devices:
            if usableDevice == deviceInfo["code"]:
                DeviceName = deviceInfo["name"]
                if t < column:
                    print(f"{usableDevices.index(usableDevice)}.{DeviceName}",end="\t\t")
                    t += 1
                else:
                    t = 0
                    print()
                    print(f"{usableDevices.index(usableDevice)}.{DeviceName}",end="\t\t")

    print("\n多选请用空格分隔...")
    choicedeviceindexes = str(input("请输入选项索引:"))
    choicedeviceindexes = choicedeviceindexes.split()
    ChoiceDevices = []
    for choicedeviceindex in choicedeviceindexes:
        choicedeviceindex = int(choicedeviceindex)
        ChoiceDevices.append(usableDevices[choicedeviceindex])
    print("将以下内容复制到Apply/data/accounts.json的devices处即可...",end="\n\n")
    log(f'"{uplanId}":{json.dumps(ChoiceDevices)}')

def single():
    os.system("clear")
    while True:
        print("GitHub: https://github.com/azurstar/MIUIhelper",end="\n\n")
        account = input("请输入账号:")
        password = input("请输入密码:")
        try:
            WebCookie = login.Web(account=account,password=password)
            log(f"\n{account}登录成功!")
            break
        except:
            log(f"\n{account}登录失败...")
            os.system("clear")
            print("登录失败, 请重新登录! ")
    def p():
        os.system("clear")
        with open("Apply/data/devices.json","r",encoding="utf-8") as r: devices = json.load(r)
        with open("Apply/data/available.json","r",encoding="utf-8") as r:Devices = json.load(r)
        taskname = {
            "10001":"开发版公测",
            "10002":"开发版内测",
            "10003":"稳定版内测"
        }
        planIds = ["10001","10002","10003"]
        print("GitHub: https://github.com/azurstar/MIUIhelper",end="\n\n")
        print("\n选择需要申请的内测...")
        for planId in planIds:
            print(f"{planIds.index(planId)}.{taskname[planId]}")
        planIdindex = str(input("请输入选项索引:"))
        print("\n寻找可用设备...")
        uplanId = planIds[int(planIdindex)]
        usableDevices:list = Devices[uplanId]
        t = 0
        os.system("clear")
        print("GitHub: https://github.com/azurstar/MIUIhelper",end="\n\n")
        print("\n以下是可用设备:")
        for usableDevice in usableDevices:
            column = 0
            DeviceName:str
            for deviceInfo in devices:
                if usableDevice == deviceInfo["code"]:
                    DeviceName = deviceInfo["name"]
                    if t < column:
                        print(f"{usableDevices.index(usableDevice)}.{DeviceName}",end="\t\t")
                        t += 1
                    else:
                        t = 0
                        print()
                        print(f"{usableDevices.index(usableDevice)}.{DeviceName}",end="\t\t")

        print("\n多选请用空格分隔...")
        choicedeviceindexes = str(input("请输入选项索引:"))
        os.system("clear")
        choicedeviceindexes = choicedeviceindexes.split()
        ChoiceDevices = []
        for choicedeviceindex in choicedeviceindexes:
            choicedeviceindex = int(choicedeviceindex)
            ChoiceDevices.append(usableDevices[choicedeviceindex])
        a = Apply()
        a.WebCookie = WebCookie
        a.planId = planId
        log("开始申请...")
        for device in ChoiceDevices:
            a.device = device
            try:a.run()
            except:log(f"未知原因导致{device}申请失败...")

    while True:
        p()
        input("\n返回 选择内测类型...")

def run():
    print("GitHub: https://github.com/azurstar/MIUIhelper",end="\n\n")
    tasks = {
        "单一账号申请":single,
        "批量申请":main,
        "检测可用设备":available,
        "选择申请设备":ChoiceDevice
    }
    tasknames = ["单一账号申请","批量申请","选择申请设备","检测可用设备"]
    print("选择你的操作...\n")
    for taskname in tasknames:
        print(f'{tasknames.index(taskname)}.{taskname}')
    index = input("\n请输入选项索引:")
    os.system("clear")
    tasks[tasknames[int(index)]]()
    input("回车退出...")

if __name__ == '__main__':run()