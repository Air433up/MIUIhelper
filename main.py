import json
from web import Answer, GetList

with open("data/accounts.json", "r", encoding="utf-8") as r:
    accounts = json.load(r)

correct = {}
for Account in accounts:
    Answer(account=Account["account"], password=Account["password"])
    lst = GetList(account=Account["account"], password=Account["password"])
    for qu in lst:
        correctSelect = qu["correctSelect"]
        question = qu["question"]
        options = qu["options"]
        for option in options:
            if option["optionId"] == correctSelect:
                Roption = option["text"]
        correct[question] = Roption
        print("正在收集题目数据...")
    with open("data/correct.json", "r", encoding="utf-8") as r:data = json.load(r)
    data = dict(correct, **data)
    with open("data/correct.json", "w", encoding="utf-8") as w:
        json.dump(data, fp=w, indent=2)
