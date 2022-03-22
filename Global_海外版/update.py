import time
import json

info_format = {
  "date": time.strftime("%Y-%m-%d"),
  "finished": []
}

def update():
    try:
        with open("data/history.json","r") as r:info = json.load(r)
    except:info = info_format
    now_date = time.strftime("%Y-%m-%d")
    read_date = info["date"]
    if read_date != now_date:
        info["date"] = now_date
        info["finished"] = []
    with open("data/history.json","w") as w:json.dump(info,fp=w,indent=2)

def finish(account)->bool:
    update()
    try:
        with open("data/history.json","r") as r:info = json.load(r)
    except:info = info_format
    if account in info["finished"]:
        return True
    else:
        return False

def record(account):
    update()
    try:
        with open("data/history.json","r") as r:info = json.load(r)
    except:info = info_format
    finished:list = info["finished"]
    finished.append(account)
    info["finished"] = finished
    with open("data/history.json","w") as w:json.dump(info,fp=w,indent=2)