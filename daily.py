# GitHub: https://github.com/azurstar/MIUIhelper

import login,json
from Daily.daily import Daily
from Daily.history import update,finish,record
def main():
    with open("Daily/data/accounts.json","r") as r:accounts = json.load(r)
    for Account in accounts:
        update()
        if finish(Account["account"]): 
            print("\n"+Account["account"]+"已完成，跳过执行...")
            continue
        account = Account["account"]
        password = Account["password"]
        try:
            WebCookie = login.Web(account=account,password=password)
            print(f"\n{account}登录成功！")
        except:
            print(f"\n{account}登录失败...")
            continue
        try:PhoneCookie = login.Phone(account=account,password=password)
        except:PhoneCookie = None
        task = Daily()
        task.WebCookie = WebCookie
        task.PhoneCookie = PhoneCookie
        task.run()
        record(Account["account"])
    print("\n\t结束!")
if __name__ == '__main__':main()
