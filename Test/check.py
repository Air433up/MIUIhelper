import json

filenames = {"开发版公测":"DevelopmentPublicTest","开发版内测":"DevelopmentInternalTest","稳定版内测":"StableInternalTest"}

def check(task):
    print(task+"---------")
    with open(f"Test/data/Correct{filenames[task]}.json", "r", encoding="utf-8") as r:Correct = set(json.load(r))
    with open(f"Test/data/{filenames[task]}.json", "r", encoding="utf-8") as r:data:dict = json.load(r)
    for question in data:
        if question not in Correct:
            print(question)
            for opt in data[question]:print(opt)
            print()
    print("Unknown above questions.")
    print(f"Data:{len(data)}")
    print(f"Correct:{len(Correct)}")

def contrast(task1,task2):
    with open(f"Test/data/Correct{filenames[task1]}.json", "r", encoding="utf-8") as r:Correct1 = set(json.load(r))
    with open(f"Test/data/{filenames[task1]}.json", "r", encoding="utf-8") as r:data1:dict = json.load(r)
    Unknown1 = []
    for question1 in data1:
        if question1 not in Correct1: Unknown1.append(question1)

    with open(f"Test/data/Correct{filenames[task2]}.json", "r", encoding="utf-8") as r:Correct2 = set(json.load(r))
    with open(f"Test/data/{filenames[task2]}.json", "r", encoding="utf-8") as r:data2:dict = json.load(r)

    for Unknown in Unknown1:
        if Unknown in Correct2:
            print(Unknown)
            print(task1+"---------")
            for opt1 in data1[Unknown]:print(opt1)
            print(task2+"---------")
            for opt2 in data2[Unknown]:print(opt2)
            print()
            try:
                if set(data1[Unknown]) == set(data2[Unknown]):
                    Correct1.add(Unknown)
                    with open(f"Test/data/Correct{filenames[task1]}.json", "w", encoding="utf-8") as w:json.dump(list(Correct1),fp=w,indent=2,ensure_ascii=False)
                    continue
            except:pass
            try:
                if set(data1[Unknown]).issubset(set(data2[Unknown])):
                    judge = input("是否合并两题选项？Yes:1,No:0：")
                    if judge == "1":
                        Correct1.add(Unknown)
                        data1[Unknown] = data2[Unknown]
                        with open(f"Test/data/Correct{filenames[task1]}.json", "w", encoding="utf-8") as w:json.dump(list(Correct1),fp=w,indent=2,ensure_ascii=False)
                        with open(f"Test/data/{filenames[task1]}.json", "w", encoding="utf-8") as w:json.dump(data1,fp=w,indent=2,ensure_ascii=False)
                elif set(data2[Unknown]).issubset(set(data1[Unknown])):
                    judge = input("是否合并两题选项？Yes:1,No:0：")
                    if judge == "1":
                        Correct2.add(Unknown)
                        data2[Unknown] = data1[Unknown]
                        with open(f"Test/data/Correct{filenames[task2]}.json", "w", encoding="utf-8") as w:json.dump(list(Correct2),fp=w,indent=2,ensure_ascii=False)
                        with open(f"Test/data/{filenames[task2]}.json", "w", encoding="utf-8") as w:json.dump(data2,fp=w,indent=2,ensure_ascii=False)
            except:pass

def accuracy(tasks = filenames):
    if type(tasks) == str:tasks = [tasks]
    DataNum = 0
    CorrectNum = 0
    for task in tasks:
        with open(f"Test/data/Correct{filenames[task]}.json", "r", encoding="utf-8") as r:Correct = set(json.load(r))
        with open(f"Test/data/{filenames[task]}.json", "r", encoding="utf-8") as r:data:dict = json.load(r)
        DataNum = DataNum + len(data)
        CorrectNum = CorrectNum + len(Correct)
    if tasks == filenames:
        print(f"综合正确率为 {(CorrectNum/DataNum)*100:.2f}%")
    else:
        print(f"{tasks} 的综合正确率为 {(CorrectNum/DataNum)*100:.2f}%")

# check("开发版公测")
# check("开发版内测")
# check("稳定版内测")

contrast("开发版公测","开发版内测")

accuracy("开发版公测")
accuracy("开发版内测")
accuracy("稳定版内测")
accuracy()