import json
from web import internalTest

with open("internalTest/Collct/data/accounts.json", "r", encoding="utf-8") as r:accounts = json.load(r)

for Account in accounts:
    internalTest(account=Account["account"], password=Account["password"],tasks=Account["tasks"])