import json
import random,requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def Answer(account, password):

    correctGitee = requests.get(url="https://gitee.com/azurstar/MIUIhelper/raw/main/data/correctCopy.json").text
    correctGitee = json.loads(correctGitee) #不定期在gitee上更新数据

    with open("data/correct.json", "r", encoding="utf-8") as r:
        crrect = json.load(r)
    crrect = dict(crrect, **correctGitee)

    with open("data/keywords.json", "r", encoding="utf-8") as r:
        keywords = json.load(r)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    MIUI = webdriver.Chrome(options=chrome_options)
    MIUI.get(url="https://web-alpha.vip.miui.com/page/info/mio/mio/internalTest")
    WebDriverWait(MIUI, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "密码登录"))).click()
    WebDriverWait(MIUI, 10).until(EC.visibility_of_element_located((By.NAME, "account"))).send_keys(account)
    WebDriverWait(MIUI, 10).until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys(password)
    WebDriverWait(MIUI, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-checkbox"))).click()
    WebDriverWait(MIUI, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "button"))).click()
    print("登录成功！")

    WebDriverWait(MIUI, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "section"))
    )  # 等待进入界面
    print("已进入答题页面！")
    try:
        WebDriverWait(MIUI, 10).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "DailyQuestions_start__2h7_C")
            )
        ).click()
    except:
        pass
    print("准备开始答题...")
    q = 0
    while True:
        try:
            q += 1
            if q >= 10:return
            MIUI.refresh()
            question = WebDriverWait(MIUI, 4).until(EC.visibility_of_element_located((By.CLASS_NAME, "DailyQuestions_title__3WufQ"))).text
            options = WebDriverWait(MIUI, 4).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "DailyQuestions_option__WTHY5")))

            print(question)
            t = 0
            for option in options:
                t+=1
                optionText = option.text
                try:Cquestion = crrect[question]
                except:Cquestion = None
                if optionText == Cquestion:
                    option.click()
                elif optionText in keywords:
                    option.click()
                elif t >= 4:
                    random.choice(options).click()
            
        except:
            MIUI.refresh()
            continue


def GetList(account, password):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    Lst = webdriver.Chrome(options=chrome_options)
    Lst.get(url="https://api.vip.miui.com/api/alpha/daily/list")
    lst = Lst.find_element(by=By.TAG_NAME, value="pre").text
    lst = json.loads(lst)

    def login(Lst: webdriver.Chrome, account, password):
        Lst.get(url=lst["loginUrl"])
        WebDriverWait(Lst, 10).until(
            EC.visibility_of_element_located((By.LINK_TEXT, "密码登录"))
        ).click()
        WebDriverWait(Lst, 10).until(
            EC.visibility_of_element_located((By.NAME, "account"))
        ).send_keys(account)
        WebDriverWait(Lst, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        ).send_keys(password)
        WebDriverWait(Lst, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "ant-checkbox"))
        ).click()
        WebDriverWait(Lst, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "button"))
        ).click()
        r = WebDriverWait(Lst, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "pre"))).text
        r = json.loads(r)
        return r

    if lst["code"] != 200:
        lst = login(Lst, account, password)

    return lst["entity"]["list"]
