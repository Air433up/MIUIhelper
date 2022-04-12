# GitHub: https://github.com/azurstar/MIUIhelper

import base64
import binascii
import json,time, hashlib,requests,random
from requests_toolbelt.multipart.encoder import MultipartEncoder

info_format = {
  "date": time.strftime("%Y-%m-%d"),
  "finished": []
}

def update():
    try:
        with open("history.json","r") as r:info = json.load(r)
    except:info = info_format
    now_date = time.strftime("%Y-%m-%d")
    read_date = info["date"]
    if read_date != now_date:
        info["date"] = now_date
        info["finished"] = []
    with open("history.json","w") as w:json.dump(info,fp=w,indent=2)

def finish(account)->bool:
    update()
    try:
        with open("history.json","r") as r:info = json.load(r)
    except:info = info_format
    if account in info["finished"]:
        return True
    else:
        return False

def record(account):
    update()
    try:
        with open("history.json","r") as r:info = json.load(r)
    except:info = info_format
    finished:list = info["finished"]
    finished.append(account)
    info["finished"] = finished
    with open("history.json","w") as w:json.dump(info,fp=w,indent=2)

class Daily:
    def __init__(self) -> None:
        pass

    WebCookie:str or dict
    PhoneCookie:str or dict

    def md5(self,text= str) -> str:
        md5 = hashlib.md5()
        md5.update(text.encode())
        return md5.hexdigest()

    def List(self):
        url = "https://api-alpha.vip.miui.com/api/alpha/daily/list"
        params = {
            "pathname":"/mio/internalTest",
            "version":"dev.220301"
        }
        headers = {
            "Host": "api-alpha.vip.miui.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 12; zh-cn; M2007J1SC Build/RKQ1.200826.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.116 Mobile Safari/537.36 XiaoMi/MiuiBrowser/15.7.22 app/vipaccount",
            "Accept": "*/*",
            "Origin": "https://web-alpha.vip.miui.com",
            "X-Requested-With": "com.xiaomi.vipaccount",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://web-alpha.vip.miui.com/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        questions = requests.get(url=url,params=params,headers=headers,cookies=self.WebCookie).text
        questions = json.loads(questions)
        return questions
    
    def CorrectQuestion(self):
        correct = {}
        lst = self.List()["entity"]["list"]
        for qu in lst:
            correctSelect = qu["correctSelect"]
            question = qu["question"]
            options = qu["options"]
            for option in options:
                if option["optionId"] == correctSelect:
                    Roption = option["text"]
            correct[question] = Roption
        with open("correct.json", "r", encoding="utf-8") as r:data = json.load(r)
        data = dict(correct, **data)
        with open("correct.json", "w", encoding="utf-8") as w:json.dump(data, fp=w,ensure_ascii=False,indent=2)
    
    def UserInfo(self):
        url = "https://api-alpha.vip.miui.com/api/community/post/userInfo?pathname=/mio/internalTest&version=dev.1144"
        headers = {
            "Host": "api-alpha.vip.miui.com",
            "Connection": "keep-alive",
            "DNT": "1",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            "sec-ch-ua-platform": "Windows",
            "Accept": "*/*",
            "Origin": "https://web-alpha.vip.miui.com",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://web-alpha.vip.miui.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        info = requests.get(url=url,headers=headers,cookies=self.WebCookie).text
        return json.loads(info)

    def Answer(self,questionId,optionId):
        url = "https://api-alpha.vip.miui.com/api/alpha/daily/answer"
        params = {
            "pathname":"/mio/internalTest",
            "version":"dev.1144",
            "miui_vip_a_ph":self.WebCookie["miui_vip_a_ph"],
            "miui_vip_slh":self.WebCookie["miui_vip_a_slh"]
        }
        ts = int(time.time()*1000) 
        userId = self.UserInfo()["entity"]["userId"]
        sign = self.md5(f"{ts}7d4ac01840424b258b786c094d7ec330")
        signature = self.md5(f"{userId}-{questionId}-{ts}7d4ac01840424b258b786c094d7ec330")
        headers = {
            "Host": "api-alpha.vip.miui.com",
            "Connection": "keep-alive",
            "Accept": "application/json",
            "DNT": "1",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarygUHrXAoQKJgqBA4x",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            "sec-ch-ua-platform": "Windows",
            "Origin": "https://web-alpha.vip.miui.com",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://web-alpha.vip.miui.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        fields = {
            "id": (None,str(questionId)),
            "optionId": (None,str(optionId)),
            "ts": (None,str(ts)),
            "sign": (None,sign),
            "signature": (None,signature),
            "miui_vip_a_ph":(None,self.WebCookie["miui_vip_a_ph"]),
            "miui_vip_a_slh":(None,self.WebCookie["miui_vip_a_slh"])
        }
        data = MultipartEncoder(fields=fields,boundary="----WebKitFormBoundarygUHrXAoQKJgqBA4x")
        answer = requests.post(url=url,params=params,headers=headers,data=data,cookies=self.WebCookie).text
        return json.loads(answer)
    
    def homepage(self):
        url = "https://api.vip.miui.com/mtop/planet/vip/home/discover"
        headers = {
            "Host": "api.vip.miui.com",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 12; zh-cn; M2007J1SC Build/RKQ1.200826.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.116 Mobile Safari/537.36 XiaoMi/MiuiBrowser/15.7.22 app/vipaccount",
            "Accept": "*/*",
            "Origin": "https://web.vip.miui.com",
            "X-Requested-With": "com.xiaomi.vipaccount",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://web.vip.miui.com/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        requests.get(url=url,headers=headers,cookies=self.PhoneCookie).text
        print("打开APP...")

    def run(self):
        try:
            if self.PhoneCookie != None:
                self.homepage()
        except:pass
        if self.WebCookie == "":return
        with open("correct.json", "r", encoding="utf-8") as r: correct = json.load(r)
        with open("keywords.json", "r", encoding="utf-8") as r:keywords = json.load(r)
        List = self.List()["entity"]["list"]
        for lst in List:
            id = lst["id"]
            question = lst["question"]
            try:correctOption = correct[question]
            except:correctOption = None
            trytime = 0
            print("\n",question,end="")
            for option in lst["options"]:
                trytime += 1
                if option["text"] == correctOption:
                    message = self.Answer(questionId=id,optionId=option["optionId"])
                    print("--"+option["text"])
                    break
                elif option["text"] in keywords:
                    message = self.Answer(questionId=id,optionId=option["optionId"])
                    print("--"+option["text"])
                    break
                if trytime >= len(lst["options"]):
                    r = random.choice(lst["options"])
                    RT = r["text"]
                    message = self.Answer(questionId=id,optionId=r["optionId"])
                    print(f"--{RT}--无法判断,已随机选择!",end="")
                    break
            print(f"\t{message['message']}")
        self.CorrectQuestion()

def Web(account,password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    Hash = md5.hexdigest()
    
    url = "https://account.xiaomi.com/pass/serviceLoginAuth2"
    headers = {
        "Host": "account.xiaomi.com",
        "Connection": "keep-alive",
        "DNT": "1",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://account.xiaomi.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://account.xiaomi.com/fe/service/login/password?_loginType=TICKET&sid=miui_vip_a&qs=%253F_loginType%253DTICKET%2526callback%253Dhttp%25253A%25252F%25252Fapi-alpha.vip.miui.com%25252Fsts%25253Fsign%25253DXSSUUsGxyi%2525252BjsU5qjFd%2525252FSU3rGV0%2525253D%252526followup%25253Dhttps%2525253A%2525252F%2525252Fapi-alpha.vip.miui.com%2525252Fpage%2525252Flogin%2525253FdestUrl%2525253Dhttps%252525253A%252525252F%252525252Fweb-alpha.vip.miui.com%252525252Fpage%252525252Finfo%252525252Fmio%252525252Fmio%252525252FinternalTest%2526sid%253Dmiui_vip_a&callback=http%3A%2F%2Fapi-alpha.vip.miui.com%2Fsts%3Fsign%3DXSSUUsGxyi%252BjsU5qjFd%252FSU3rGV0%253D%26followup%3Dhttps%253A%252F%252Fapi-alpha.vip.miui.com%252Fpage%252Flogin%253FdestUrl%253Dhttps%25253A%25252F%25252Fweb-alpha.vip.miui.com%25252Fpage%25252Finfo%25252Fmio%25252Fmio%25252FinternalTest&_sign=NAdvmOkKh%2BZuP0L%2B30KdA%2FkJqm0%3D&serviceParam=%7B%22checkSafePhone%22%3Afalse%2C%22checkSafeAddress%22%3Afalse%2C%22lsrp_score%22%3A0.0%7D&showActiveX=false&theme=&needTheme=false&bizDeviceType=&_locale=zh_CN",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "deviceId=wb_51ac1d27-0c18-46f9-a8b7-abf4205aac8e; pass_ua=web; uLocale=zh_CN"
    }
    data = {
        "bizDeviceType": "",
        "needTheme": "false",
        "theme":"",
        "showActiveX": "false",
        "serviceParam": '{"checkSafePhone":false,"checkSafeAddress":false,"lsrp_score":0.0}',
        "callback": "http://api-alpha.vip.miui.com/sts?sign=XSSUUsGxyi%2BjsU5qjFd%2FSU3rGV0%3D&followup=https%3A%2F%2Fapi-alpha.vip.miui.com%2Fpage%2Flogin%3FdestUrl%3Dhttps%253A%252F%252Fweb-alpha.vip.miui.com%252Fpage%252Finfo%252Fmio%252Fmio%252FinternalTest",
        "qs": "%3F_loginType%3DTICKET%26callback%3Dhttp%253A%252F%252Fapi-alpha.vip.miui.com%252Fsts%253Fsign%253DXSSUUsGxyi%25252BjsU5qjFd%25252FSU3rGV0%25253D%2526followup%253Dhttps%25253A%25252F%25252Fapi-alpha.vip.miui.com%25252Fpage%25252Flogin%25253FdestUrl%25253Dhttps%2525253A%2525252F%2525252Fweb-alpha.vip.miui.com%2525252Fpage%2525252Finfo%2525252Fmio%2525252Fmio%2525252FinternalTest%26sid%3Dmiui_vip_a",
        "sid": "miui_vip_a",
        "user": str(account),
        "cc": "+86",
        "hash": Hash.upper(),
        "_json": "true",
        "policyName": "miaccount",
        "captCode": ""
    }
    Auth = requests.post(url=url,headers=headers,data=data).text.replace("&&&START&&&","")
    Auth = json.loads(Auth)
    nurl = Auth["location"]
    sts = requests.get(url=nurl,allow_redirects=False)
    return requests.utils.dict_from_cookiejar(sts.cookies)

def Phone(account,password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    Hash = md5.hexdigest()
    url = "https://account.xiaomi.com/pass/serviceLoginAuth2"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; M2007J17C Build/SKQ1.211006.001) APP/xiaomi.vipaccount APPV/220301 MK/UmVkbWkgTm90ZSA5IFBybw== PassportSDK/3.7.8 passport-ui/3.7.8",
        "Cookie": "deviceId=X0jMu7b0w-jcne-S; pass_o=2d25bb648d023d7f; sdkVersion=accountsdk-2020.01.09",
        "Host": "account.xiaomi.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    data = {
        "cc":"+86",
        "qs":"%3F_json%3Dtrue%26sid%3Dmiui_vip%26_locale%3Dzh_CN",
        "callback":"https://api.vip.miui.com/sts",
        "_json":"true",
        "user":account,
        "hash":Hash.upper(),
        "sid":"miui_vip",
        "_sign":"ZJxpm3Q5cu0qDOMkKdWYRPeCwps%3D",
        "_locale":"zh_CN"
    }
    Auth = requests.post(url=url,headers=headers,data=data).text.replace("&&&START&&&","")
    Auth = json.loads(Auth)
    ssecurity = Auth["ssecurity"]
    nonce = Auth["nonce"]
    sha1 = hashlib.sha1()
    Str = "nonce="+str(nonce)+"&"+ssecurity
    sha1.update(Str.encode("utf-8"))
    clientSign = base64.encodebytes(binascii.a2b_hex(sha1.hexdigest().encode("utf-8"))).decode(encoding="utf-8").strip()
    nurl = Auth["location"]+"&_userIdNeedEncrypt=true&clientSign="+clientSign

    sts = requests.get(url=nurl)
    return requests.utils.dict_from_cookiejar(sts.cookies)


def main():
    with open("accounts.json","r") as r:accounts = json.load(r)
    for Account in accounts:
        update()
        if finish(Account["account"]): 
            print("\n"+Account["account"]+"已完成，跳过执行...")
            continue
        account = Account["account"]
        password = Account["password"]
        try:
            WebCookie = Web(account=account,password=password)
            print(f"\n{account}登录成功！")
        except:
            print(f"\n{account}登录失败...")
            continue
        try:PhoneCookie = Phone(account=account,password=password)
        except:PhoneCookie = None
        task = Daily()
        task.WebCookie = WebCookie
        task.PhoneCookie = PhoneCookie
        task.run()
        record(Account["account"])
    print("\n\t结束!")

def init():
    try:     
        with open("accounts.json","r",encoding="utf-8") as r:json.load(r)
        with open("correct.json","r",encoding="utf-8") as r:json.load(r)
        with open("keywords.json","r",encoding="utf-8") as r:json.load(r)
    except:
        accounts = [
        {
            "account": "18xxxxxx91",
            "password": "xxxxxx"
        },
        {
            "account": "15xxxxxx31",
            "password": "xxxxxx"
        },
        {
            "account": "16xxxxxx54",
            "password": "xxxxxx"
        },
        {
            "account": "18xxxxxx39",
            "password": "xxxxxx"
        }
        ]
        correct = {
        "硬件检测模式怎么进入？": "连击内核版本",
        "线刷需要手机进入什么模式？": "FastBoot",
        "下面哪些是MIUI13的特色功能": "以上都是",
        "手机硬件坏了怎么办？": "联系小米售后",
        "MIUI的官网是什么": "www.miui.com",
        "发现泄漏内测APP，应该怎么做？": "保留证据反馈申诉处理圈",
        "备份有以下哪种方式？": "这些都是",
        "小爱同学默认唤醒词是？": "小爱同学",
        "通常情况下开发版公测更新频率是？": "一周1次",
        "社区内存在偷渡包和偷渡教程帖子，遇到了会怎么办?": "反馈到申诉处理圈并举报该违规行为",
        "在需要尽可能保留数据的情况下，线刷的刷机流程应该是?": "先备份数据，解锁BL再刷机",
        "小米MIUI首个内测版推出的时间是？": "2010年8月16日",
        "MIUI13和哪款手机同一时间发布？": "小米12",
        "小米成立于哪一年？": "2010年",
        "小米公司成立的日期是?": "2010年4月6日",
        "通常说的MIUI开发版公测是（）色星期（）?": "橙，五",
        "小米语音助手名称是？": "小爱同学",
        "震动效果和什么有关?": "马达",
        "MIUI桌面智能助理功能，又叫做___？": "负一屏",
        "APP闪退又被称作？": "FC",
        "下列刷机工具中，属于官方提供的工具是？": "MiFlash",
        "手机出厂时，默认会是哪个版本？": "稳定版",
        "如何在我的设备内进入开发者模式？": "连击MIUI版本号",
        "哪种行为可能会涉及灌水？": "重复发布空洞无任何意义的帖子",
        "下列选项中，哪个是正确的": "橙色星期五",
        "小米在哪个城市成立？": "北京",
        "拨号界面输入什么代码可抓取日志相关信息？": "*#*#284#*#*",
        "下列选项哪个是随MIUI13一起发布的字体？": "MI Sans",
        "哪项不是MIUI13发布会的亮点？": "全新MIUI笔记",
        "下列选项中，哪个是正确抓log的方法": "在拨号盘输入*#*#284#*#*",
        "如果应用软件出现bug问题该如何反馈？": "向应用开发者和小米社区及时、理性反馈",
        "新功能更新最快的版本是？": "开发版内测",
        "有人私信发广告，应该怎么做？": "保留证据反馈给官方",
        "开发版公测一般在周几更新？": "周五",
        "每年米粉节的日期是？": "4月6日",
        "小米做的第一款产品是什么？": "MIUI系统",
        "遇到贩卖内测账号，应该怎么做？": "保留证据并举报至申诉处理圈",
        "MIUI系统更新又被称作？": "OTA"
        }
        keywords = [
            "橙，五",
            "橙色星期五"
        ]
        with open("accounts.json","w",encoding="utf-8") as w:json.dump(accounts,fp=w,ensure_ascii=False,indent=2)
        with open("correct.json","w",encoding="utf-8") as w:json.dump(correct,fp=w,ensure_ascii=False,indent=2)
        with open("keywords.json","w",encoding="utf-8") as w:json.dump(keywords,fp=w,ensure_ascii=False,indent=2)
        print("文件生成完毕...")
        print("请在accounts.json中, 填写账号和密码")
        print("若出现登录失败, 可能是账号在非常用设备上登录, 会需要验证码, 使用该设备自行前去验证https://web-alpha.vip.miui.com/page/info/mio/mio/internalTest")
        print("\n出现问题可以来这里提交Issues")
        print("GitHub: https://github.com/azurstar/MIUIhelper")
        exit()

if __name__ == '__main__':
    update()
    init()
    main()
