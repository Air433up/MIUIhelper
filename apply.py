# GitHub: https://github.com/azurstar/MIUIhelper

import time
from Apply.apply import Apply
import login
import json

def main():
    planIds = ["10001","10002","10003"]
    with open("Apply/data/accounts.json","r",encoding="utf-8") as r: accounts = json.load(r)
    for Account in accounts:
        account = Account["account"]
        password = Account["password"]
        try:
            WebCookie = login.Web(account=account,password=password)
            print(f"\n{account}登录成功!")
        except:
            print(f"\n{account}登录失败...")
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
        print("登录失败,无法检测可用设备,有以下解决方法...")
        print("1.在Apply/data/accounts.json的第一栏填入账号密码")
        print("2.在浏览器登录小米社区,通过验证码校验")
        exit()
    with open("Apply/data/devices.json","r",encoding="utf-8") as r: devices = json.load(r)
    for planId in planIds:
        tt = 0
        try:startcode = Devices[planId][-1]
        except:startcode = "代号名称"
        print()
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
        column = 1
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
    print("\n多选请用空格分隔...")
    choicedeviceindexes = str(input("请输入选项索引:"))
    choicedeviceindexes = choicedeviceindexes.split()
    ChoiceDevices = []
    for choicedeviceindex in choicedeviceindexes:
        choicedeviceindex = int(choicedeviceindex)
        ChoiceDevices.append(usableDevices[choicedeviceindex])
    print("将以下内容复制到Apply/data/accounts.json的devices处即可...",end="\n\n")
    print(f'"{uplanId}":{json.dumps(ChoiceDevices)}')

def run():
    tasks = {
        "开始申请":main,
        "检测可用设备":available,
        "选择申请设备":ChoiceDevice
    }
    tasknames = ["开始申请","选择申请设备","检测可用设备"]
    print("\n选择你的操作...\n")
    for taskname in tasknames:
        print(f'{tasknames.index(taskname)}.{taskname}')
    index = input("\n请输入选项索引:")
    tasks[tasknames[int(index)]]()

if __name__ == '__main__':run()