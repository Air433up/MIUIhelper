import json
from web import Answer, GetList
from update import update,finish,record

with open("data/accounts.json", "r", encoding="utf-8") as r:
    accounts = json.load(r)

for Account in accounts:
    correct = {}
    update()
    if finish(Account["account"]): 
        print("\n"+Account["account"]+"已完成，跳过执行...")
        continue
    answer = Answer(account=Account["account"], password=Account["password"])
    if answer == False: continue
    print("\n正在收集题目数据...")
    lst = GetList(account=Account["account"], password=Account["password"])
    for qu in lst:
        correctSelect = qu["correctSelect"]
        question = qu["question"]
        options = qu["options"]
        for option in options:
            if option["optionId"] == correctSelect:
                Roption = option["text"]
        correct[question] = Roption
    with open("data/correct.json", "r", encoding="utf-8") as r:data = json.load(r)
    data = dict(correct, **data)
    with open("data/correct.json", "w", encoding="utf-8") as w:
        json.dump(data, fp=w, indent=2)
        record(Account["account"])
        print("数据收集完成！")
    print("开始尝试寻找其他账号...")
print("\n结束！")
exit()