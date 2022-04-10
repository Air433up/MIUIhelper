# GitHub: https://github.com/azurstar/MIUIhelper

import base64
import binascii
import json
import requests,hashlib

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
