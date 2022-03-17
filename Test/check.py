import json

filenames = {"开发版公测":"DevelopmentPublicTest","开发版内测":"DevelopmentInternalTest","稳定版内测":"StableInternalTest"}

def check(task):
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
            print(task1)
            for opt1 in data1[Unknown]:print(opt1)
            print(task2)
            for opt2 in data2[Unknown]:print(opt2)
            print()
        try:
            if set(data1[Unknown]) == set(data2[Unknown]):
                Correct1.add(Unknown)
                with open(f"Test/data/Correct{filenames[task1]}.json", "w", encoding="utf-8") as w:json.dump(list(Correct1),fp=w,indent=2,ensure_ascii=False)
        except:pass

check("开发版内测")