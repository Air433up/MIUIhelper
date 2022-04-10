# GitHub: https://github.com/azurstar/MIUIhelper

import json,time, hashlib,requests,random
from requests_toolbelt.multipart.encoder import MultipartEncoder

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
        with open("Daily/data/correct.json", "r", encoding="utf-8") as r:data = json.load(r)
        data = dict(correct, **data)
        with open("Daily/data/correct.json", "w", encoding="utf-8") as w:json.dump(data, fp=w,ensure_ascii=False,indent=2)
    
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
        with open("Daily/data/correct.json", "r", encoding="utf-8") as r: correct = json.load(r)
        with open("Daily/data/keywords.json", "r", encoding="utf-8") as r:keywords = json.load(r)
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

        