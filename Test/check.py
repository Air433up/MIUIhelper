import json

def check(task):
    filenames = {"开发版公测":"DevelopmentPublicTest","开发版内测":"DevelopmentInternalTest","稳定版内测":"StableInternalTest"}
    with open(f"Test/data/Correct{filenames[task]}.json", "r", encoding="utf-8") as r:Correct = set(json.load(r))
    with open(f"Test/data/{filenames[task]}.json", "r", encoding="utf-8") as r:data:dict = json.load(r)
    for question in data:
        if question not in Correct:
            print(question)
            for opt in data[question]:print(opt)
            print()
    print(f"Data:{len(data)}")
    print(f"Correct:{len(Correct)}")

check("开发版公测")