# GitHub: https://github.com/azurstar/MIUIhelper

import requests,json,hashlib,urllib,base64,binascii

class Test:
    def __init__(self) -> None:
        pass

    account:str or int
    password:str or int
    planId:str or int
    surveyId:str or int

    def Web(self):
        account = self.account
        password = self.password
        md5 = hashlib.md5()
        md5.update(password.encode())
        Hash = md5.hexdigest()
        url = "https://account.xiaomi.com/pass/serviceLoginAuth2"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
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
        self.WebCookie = requests.utils.dict_from_cookiejar(sts.cookies)

    def Phone(self):
        account = self.account
        password = self.password
        md5 = hashlib.md5()
        md5.update(password.encode())
        Hash = md5.hexdigest()
        url = "https://account.xiaomi.com/pass/serviceLoginAuth2"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.0; MI NOTE Pro MIUI/V9.2.3.0.NXHCNEK) APP/xiaomi.vipaccount APPV/220301 MK/TUkgTk9URSBQcm8= PassportSDK/3.7.8 passport-ui/3.7.8",
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

        sts = requests.get(url=nurl,allow_redirects=False)
        rc = requests.utils.dict_from_cookiejar(sts.cookies)
        self.WebCookie = dict(self.WebCookie,**rc)

    def surveyInfo(self):
        url = f"https://api-alpha.vip.miui.com/api/alpha/survey/url?planId={self.planId}&bankId=undefined&surveyId=undefined&pathname=/mio/answerResult&version=dev.20001&miui_version=undefined&android_version=undefined&oaid=false&device=&restrict_imei=&miui_big_version=&model=&androidVersion=undefined&miuiBigVersion="
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        }
        res = requests.get(url=url,headers=headers,cookies=self.WebCookie)
        ret:str = json.loads(res.text)["entity"]["url"]
        self.surveyinfo = ret.replace("?noShare=true","").replace("?noShare=false","").replace("https://m.beehive.miui.com/","")
        return ret.replace("?noShare=true","").replace("?noShare=false","").replace("https://m.beehive.miui.com/","")

    def location(self):
        url = "https://m.beehive.miui.com/api/location"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        }
        data = {
            "surveyInfo": self.surveyinfo,
            "userId": "",
            "appname": ""
        }
        res = requests.post(url=url,headers=headers,data=data,cookies=self.WebCookie)
        RES = json.loads(res.text)
        self.surveyId = RES["data"]["survey"]["id"]
        rc = requests.utils.dict_from_cookiejar(res.cookies)
        self.WebCookie = dict(self.WebCookie,**rc)

    def passport(self):
        url = f"https://m.beehive.miui.com/api/passport?from=https%3A%2F%2Fm.beehive.miui.com%2F{self.surveyinfo}%2Fdesktop%2Fhome%3FloginBack%3D1"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        }
        res = requests.get(url=url,headers=headers,allow_redirects=False,cookies=self.WebCookie)
        Location = res.headers["Location"]
        res = requests.get(url=Location,headers=headers,allow_redirects=False,cookies=self.WebCookie)
        Location = res.headers["Location"]
        return Location
    
    def notificationUrl(self):
        pass # 验证码(先挖坑)

    def serviceLoginAuth2(self):
        account = self.account
        password = self.password
        md5 = hashlib.md5()
        md5.update(password.encode())
        Hash = md5.hexdigest()

        Location = self.passport()
        up = urllib.parse.urlparse(Location).query
        upp = urllib.parse.parse_qs(up)

        qs = upp["qs"][0]
        _sign = upp["_sign"][0]
        callback = upp["callback"][0]

        url = "https://account.xiaomi.com/pass/serviceLoginAuth2"
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.0; MI NOTE Pro MIUI/V9.2.3.0.NXHCNEK) APP/xiaomi.vipaccount APPV/220301 MK/TUkgTk9URSBQcm8= PassportSDK/3.7.8 passport-ui/3.7.8"
        }
        data = {
            "bizDeviceType": "",
            "needTheme": "false",
            "theme": "",
            "showActiveX": "false",
            "serviceParam": '{"checkSafePhone":false,"checkSafeAddress":false,"lsrp_score":0.0}',
            "callback": callback,
            "qs": qs,
            "sid": "miuibeehive",
            "_sign": _sign,
            "user": account,
            "cc": "+86",
            "hash": Hash.upper(),
            "_json": "true",
            "policyName": "miaccount",
            "captCode": ""
        }
        res = requests.post(url=url,headers=headers,data=data)
        location = json.loads(res.text.replace("&&&START&&&",""))["location"]
        if location == "":
            notificationUrl = json.loads(res.text.replace("&&&START&&&",""))["notificationUrl"]
            # 验证码(挖坑...)
            return

        sts = requests.get(url=location,allow_redirects=False)
        p = requests.get(url=sts.headers["Location"],headers=headers,cookies=sts.cookies,allow_redirects=False)
        c1 = requests.utils.dict_from_cookiejar(sts.cookies)
        c2 = requests.utils.dict_from_cookiejar(p.cookies)
        cs = dict(c1,**c2)
        self.WebCookie = dict(self.WebCookie,**cs)
    
    def start(self):
        url = "https://m.beehive.miui.com/api/start"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        }
        data = {
            "surveyId": self.surveyId,
            "channel": "",
            "deviceInfo": ""
        }
        res = requests.post(url=url,headers=headers,data=data,cookies=self.WebCookie,allow_redirects=False)

    def currSubject(self):
        url = "https://m.beehive.miui.com/api/currSubject"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        }
        data = {
            "surveyId": self.surveyId,
            "channel": "",
            "deviceInfo": ""
        }
        res = requests.post(url=url,headers=headers,data=data,cookies=self.WebCookie)
        resdata = json.loads(res.text)["data"]
        return resdata

    def commitAnswer(self,questionId,chooseId):
        types = {
            "10001":"1",
            "10002":"1",
            "10003":"2"
        }# planId: type
        url = "https://m.beehive.miui.com/api/commitAnswer"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        }
        data = {
            "surveyId": self.surveyId,
            "channel": "",
            "questionId": questionId,
            "type": types[str(self.planId)],
            "respondent": "",
            "result": '{"choose":'+str(chooseId)+',"other":""}',
            "sign": "",
            "finish": "0",
        }
        res = requests.post(url=url,headers=headers,data=data,cookies=self.WebCookie)
    
    def survey(self):
        url = "https://api-alpha.vip.miui.com/api/alpha/survey"
        params = {
            "planId": self.planId,
            "pathname": "/mio/systemTestDetails",
            "version": "dev.20001",
            "miui_version": "undefined",
            "android_version": "undefined",
            "oaid": "false",
            "device": "",
            "restrict_imei": "",
            "miui_big_version": "",
            "model": "",
            "androidVersion": "undefined",
            "miuiBigVersion": ""
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        }
        res = requests.get(url=url,params=params,headers=headers,cookies=self.WebCookie)
        return json.loads(res.text)["entity"]["score"]

    def answerResult(self):
        bankIds = {
            "10001":"10204",
            "10002":"10230",
            "10003":"10245"
        }# planId: bankId
        url = "https://api.vip.miui.com/api/alpha/survey/scored"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        }
        params = {
            "planId": "undefined",
            "bankId": bankIds[str(self.planId)],
            "surveyId": self.surveyId,
            "pathname": "/mio/answerResult",
            "version": "dev.1144"
        }
        res = requests.get(url=url,params=params,headers=headers,cookies=self.WebCookie,allow_redirects=False)
    
    def DelStr(self,s:str):
        DelList = ['<span style="color:rgb(55, 60, 67)">','</span>','<span >']
        for Delz in DelList:
            s = s.replace(Delz,"")
        return s.strip()

    def run(self):
        taskname = {
            "10001":"开发版公测",
            "10002":"开发版内测",
            "10003":"稳定版内测"
        }
        self.Web()
        try:self.Phone()
        except:pass
        self.surveyInfo()
        self.location()
        self.serviceLoginAuth2()
        self.start()
        print(f"\n{self.account}开始{taskname[str(self.planId)]}答题")
        with open(f"Test/data/{self.planId}.json","r",encoding="utf-8") as r:Correct = json.load(r)
        resdata = self.currSubject()
        while resdata['index'] <= resdata["count"]:
            resdata = self.currSubject()
            if resdata["status"] != 0:break
            question = self.DelStr(resdata["content"])
            questionId = resdata["questionId"]
            chooseId = []
            trytime = 0
            choice:list = resdata["choice"]
            try:CorrectOptions = Correct[question]
            except:CorrectOptions = []
            print(f"\n{resdata['index']}.{question}")
            for c in choice:
                content = self.DelStr(c["content"])
                if content in CorrectOptions:
                    trytime += 1
                    chooseId.append(c["id"])
                    print(content)
            if trytime == 0:
                for c in choice:
                    content = self.DelStr(c["content"])
                    print(f"{choice.index(c)}:{content}")
                indexes = str(input("未发现收录答案,请输入选项索引:"))
                for i in indexes:
                    l = choice[int(i)]
                    chooseId.append(l["id"])
                    CorrectOptions.append(self.DelStr(l["content"]))
                Correct[question] = CorrectOptions
                with open(f"Test/data/{self.planId}.json","w",encoding="utf-8") as w:json.dump(Correct, fp=w,ensure_ascii=False,indent=2)
            self.commitAnswer(questionId=questionId,chooseId=chooseId)
        self.answerResult()
        score = self.survey()
        print(f"\n{self.account}{taskname[str(self.planId)]}得分{score}...")

# 10001 开发版公测
# 10002 开发版内测
# 10003 稳定版内测