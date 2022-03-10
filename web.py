import json
import random,requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

prefs = {'profile.managed_default_content_settings.images': 2}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument("--no-sandbox")
chrome_options.add_experimental_option('prefs',prefs)

wait_time = 10 
answer_time = 5

def Answer(account, password):

    correctGitee = requests.get(url="https://gitee.com/azurstar/MIUIhelper/raw/main/data/correctCopy.json").text
    correctGitee = json.loads(correctGitee) #不定期在gitee上更新数据

    with open("data/correct.json", "r", encoding="utf-8") as r:
        crrect = json.load(r)
        
    crrect = dict(crrect, **correctGitee)

    with open("data/keywords.json", "r", encoding="utf-8") as r:
        keywords = json.load(r)

    MIUI = webdriver.Chrome(options=chrome_options)
    MIUI.get(url="https://web-alpha.vip.miui.com/page/info/mio/mio/internalTest")
    WebDriverWait(MIUI, wait_time).until(EC.visibility_of_element_located((By.LINK_TEXT, "密码登录"))).click()
    WebDriverWait(MIUI, wait_time).until(EC.visibility_of_element_located((By.NAME, "account"))).send_keys(account)
    WebDriverWait(MIUI, wait_time).until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys(password)
    WebDriverWait(MIUI, wait_time).until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-checkbox"))).click()
    WebDriverWait(MIUI, wait_time).until(EC.visibility_of_element_located((By.TAG_NAME, "button"))).click()
    print(f"\n{account}登录成功！")

    WebDriverWait(MIUI, wait_time).until(EC.visibility_of_element_located((By.TAG_NAME, "section")))  # 等待进入界面
    print("已进入答题页面！")
    try:WebDriverWait(MIUI, wait_time).until(EC.visibility_of_element_located((By.CLASS_NAME, "DailyQuestions_start__2h7_C"))).click()
    except:pass
    print("准备开始答题...")
    for ty in range(5):
        print("\r尝试次数:",ty+1,end="",flush=True)
        try:
            try:WebDriverWait(MIUI, answer_time).until(EC.visibility_of_element_located((By.CLASS_NAME, "DailyQuestions_start__2h7_C"))).click()
            except:pass
            question = WebDriverWait(MIUI, answer_time).until(EC.visibility_of_element_located((By.CLASS_NAME, "DailyQuestions_title__3WufQ"))).text
            options = WebDriverWait(MIUI, answer_time).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "DailyQuestions_option__WTHY5")))

            print("\n",question,end="")
            t = 0
            for option in options:
                t+=1
                optionText = option.text
                try:Cquestion = crrect[question]
                except:Cquestion = None
                if optionText == Cquestion:
                    option.click()
                    print("--"+optionText)
                elif optionText in keywords:
                    option.click()
                    print("--"+optionText)
                elif t >= 4:
                    r = random.choice(options)
                    r.click()
                    print("--"+r.text+"--无法判断,已随机选择!")
            
        except:
            MIUI.refresh()

def GetList(account, password):

    Lst = webdriver.Chrome(options=chrome_options)
    Lst.get(url="https://api.vip.miui.com/api/alpha/daily/list")
    lst = Lst.find_element(by=By.TAG_NAME, value="pre").text
    lst = json.loads(lst)

    def login(Lst: webdriver.Chrome, account, password):
        Lst.get(url=lst["loginUrl"])
        WebDriverWait(Lst, wait_time).until(EC.visibility_of_element_located((By.LINK_TEXT, "密码登录"))).click()
        WebDriverWait(Lst, wait_time).until(EC.visibility_of_element_located((By.NAME, "account"))).send_keys(account)
        WebDriverWait(Lst, wait_time).until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys(password)
        WebDriverWait(Lst, wait_time).until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-checkbox"))).click()
        WebDriverWait(Lst, wait_time).until(EC.visibility_of_element_located((By.TAG_NAME, "button"))).click()
        r = WebDriverWait(Lst, wait_time).until(EC.visibility_of_element_located((By.TAG_NAME, "pre"))).text
        r = json.loads(r)
        return r

    if lst["code"] != 200:
        lst = login(Lst, account, password)

    return lst["entity"]["list"]
