# GitHub: https://github.com/azurstar/MIUIhelper

import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def browser():
    prefs = {'profile.managed_default_content_settings.images': 2}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option('prefs',prefs)
    return webdriver.Chrome(executable_path="chromedriver",options=chrome_options)
wait_time = 5
MIUI = browser()
MIUI.get(url="https://miuiver.com/xiaomi-device-codename/")
a = WebDriverWait(MIUI, wait_time).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "tr")))
devices = []
for i in a:
    msg:str = i.text
    device = {}
    lst = msg.split()
    device_code = lst[-2]
    date = lst[-1]
    device_code_index = lst.index(device_code)
    device_name = ""
    for s in range(device_code_index):
        message = lst[s]+" "
        device_name += message
    device_name = device_name.strip()
    device["name"] = device_name
    device["code"] = device_code
    device["date"] = date
    devices.append(device)
    print(device_name)
with open("Apply/devices.json","w",encoding="utf-8") as w:json.dump(devices,fp=w,ensure_ascii=False,indent=2)

