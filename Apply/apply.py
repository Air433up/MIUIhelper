# GitHub: https://github.com/azurstar/MIUIhelper

import requests,json,hashlib,time,random
from requests_toolbelt.multipart.encoder import MultipartEncoder

log_path = "ApplyLog.txt"

def log(value="\n"):
    f = open(log_path,"a+",encoding="utf-8")
    print(value)
    print(value,file=f)
    f.close()


class Apply:
    def __init__(self) -> None:
        pass
    projectTypes = {
        10001:1,    # 10001 开发版公测
        10002:0,    # 10002 开发版内测
        10003:2     # 10003 稳定版内测
    }
    planId:str or int
    WebCookie:dict
    device:str

    def Sign(self):
        url = "https://api-alpha.vip.miui.com/api/alpha/miui/sign"
        params = {
            "projectType": self.projectTypes[int(self.planId)], # 开发版内测 0 , 开发版公测 1 , 稳定版内测 2
            "pathname": "/mio/systemTestApply",
            "version": "dev.20001",
            "miui_version": "undefined",
            "android_version": "undefined",
            "oaid": "false",
            "device": self.device,
            "restrict_imei": "",
            "miui_big_version": "",
            "model": "黄金版 Iphone 13 Pro Max", # 假装B格拉满
            "androidVersion": "undefined",
            "miuiBigVersion": ""
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        }
        res = requests.get(url=url,params=params,headers=headers,cookies=self.WebCookie)
        self.applyInfo = json.loads(res.text)["entity"]
        self.userId = self.applyInfo["userId"]

    def Signature(self):
        self.ts = int(time.time())
        msg = f"{self.userId}-{self.planId}-{self.ts}-f0e666e08a3c786a87f617fe0f37cfd0"
        md5 = hashlib.md5()
        md5.update(msg.encode())
        self.signature = md5.hexdigest()

    def RandomPhoneNum(self):return random.randint(10000000000,20000000000)

    def get_matched(self):
        conditions = self.applyInfo["conditions"]
        matchedList = []
        matched = ""
        for condition in conditions:
            matchedList.append(condition["content"])

        for condition in conditions:
            index = int(condition["index"])-1
            content = condition["content"]
            matchedList[index] = content
        for msg in matchedList:
            matched += f"{msg}|"
        self.matched = matched[:-1]

    def getdata(self):
        fields = {
            "contact":(None,str(self.RandomPhoneNum())),
            "supplement":(None,""),
            "isAcceptProtocol":(None,"true"),
            "device":(None,self.device),
            "planId":(None,str(self.applyInfo["devices"][0]["planId"])),
            "matched":(None,self.matched),
            "projectType":(None,str(self.projectTypes[int(self.planId)])),
            "ts":(None,str(self.ts)),
            "signature":(None,self.signature),
            "miui_vip_a_ph":(None,self.WebCookie["miui_vip_a_ph"]),
            "miui_vip_a_slh":(None,self.WebCookie["miui_vip_a_slh"]),
            "miui_vip_a_serviceToken":(None,self.WebCookie["miui_vip_a_serviceToken"])
        }
        data = MultipartEncoder(fields=fields,boundary="----WebKitFormBoundaryZkkMlfDoYxkRFhlC")
        return data

    def signup(self):
        url = "https://api-alpha.vip.miui.com/api/alpha/miui/signup"
        params = {
            "ref": "vipAccountShortcut",
            "pathname": "/mio/systemTestApply",
            "version": "dev.220326",
            "miui_version": "V13.0.3.0.SJSCNXM",
            "android_version": "12",
            "oaid": "",
            "device": self.device,
            "restrict_imei": "",
            "miui_big_version": "V130",
            "model": "黄金版 Iphone 13 Pro Max",
            "androidVersion": "12",
            "miuiBigVersion": "V130",
            "cUserId": self.WebCookie["cUserId"],
            "miui_vip_a_ph": self.WebCookie["miui_vip_a_ph"],
            "miui_vip_a_slh": self.WebCookie["miui_vip_a_slh"],
            "miui_vip_a_serviceToken": self.WebCookie["miui_vip_a_serviceToken"]
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            "Cache-Control": "no-cache",
            "Accept": "application/json",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryZkkMlfDoYxkRFhlC"
        }
        data = self.getdata()
        res = requests.post(url=url,params=params,headers=headers,data=data,cookies=self.WebCookie)
        message = json.loads(res.text)["message"]
        taskname = {
            "10001":"开发版公测",
            "10002":"开发版内测",
            "10003":"稳定版内测"
        }
        log(f'申请 {taskname[str(self.planId)]} {self.applyInfo["devices"][0]["name"]}: {message}')

    def run(self):
        self.Sign()
        self.Signature()
        self.get_matched()
        self.signup()