# GitHub: https://github.com/azurstar/MIUIhelper

from Test.test import Test
import json
def main():
    taskname = {
        "10001":"开发版公测",
        "10002":"开发版内测",
        "10003":"稳定版内测"
    }
    with open("Test/data/accounts.json","r",encoding="utf-8") as r:accounts = json.load(r)
    for Account in accounts:
        account = Account["account"]
        password = Account["password"]
        tasks = Account["tasks"]
        for task in tasks:
            try:
                t = Test()
                t.account = account
                t.password = password
                t.planId = task
                t.run()
            except:
                print(f"{account}的{taskname[str(task)]}开始失败...")
        print(f"{account}任务结束!",end="\n\n")

if __name__ == '__main__':main()
# 10001 开发版公测
# 10002 开发版内测
# 10003 稳定版内测
# planIds = [10001,10002,10003]