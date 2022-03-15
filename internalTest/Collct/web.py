import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def browser():
    prefs = {'profile.managed_default_content_settings.images': 2}
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_experimental_option('prefs',prefs)
    return webdriver.Chrome(executable_path="./chromedriver",options=chrome_options)

wait_time = 10

def internalTest(account, password,tasks):
    for task in tasks:
        Test = browser()
        Test.get(url="https://web-alpha.vip.miui.com/page/info/mio/mio/internalTest")
        WebDriverWait(Test, wait_time).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/div/div[2]/div/div/div[2]/div/div[2]/div[3]/div[1]/form/div[1]/div[4]/div[2]/a"))).click()  # 点击密码登录
        WebDriverWait(Test, wait_time).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/div/div[2]/div/div/div[2]/div/div[2]/div[3]/div[1]/form/div[1]/div[1]/div[2]/div/div/div/div/input"))).send_keys(account) # 输入账号
        WebDriverWait(Test, wait_time).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/div/div[2]/div/div/div[2]/div/div[2]/div[3]/div[1]/form/div[1]/div[2]/div/div[1]/div/input"))).send_keys(password) # 输入密码
        WebDriverWait(Test, wait_time).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/div/div[2]/div/div/div[2]/div/div[2]/div[3]/div[1]/form/div[1]/div[3]/label/span[1]"))).click() # 勾选协议
        WebDriverWait(Test, wait_time).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/div/div[2]/div/div/div[2]/div/div[2]/div[3]/div[1]/form/div[1]/button"))).click() # 点击登录
        try:
            WebDriverWait(Test, wait_time).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/div[3]/div[2]"))) # 判断是否打开
            print(f"\n{account}登录成功！")
        except:
            print(f"\n{account}登录失败...")
            return False

        UserAgent = "Dalvik/2.1.0 (Linux; U; Android 7.0; MI NOTE Pro MIUI/V9.2.3.0.NXHCNEK) APP/xiaomi.vipaccount APPV/220301 MK/TUkgTk9URSBQcm8= PassportSDK/3.7.8 passport-ui/3.7.8"
        Test.execute_cdp_cmd("Emulation.setUserAgentOverride", {"userAgent": UserAgent})
        WebDriverWait(Test, wait_time).until(EC.visibility_of_element_located((By.CLASS_NAME, "TestCenter_find-more__1Fe8J"))).click() # 点击展开
        TestOptions = WebDriverWait(Test, wait_time).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "TestCenter_text__SUpLA")))
        for TestOption in TestOptions:
            try:
                if TestOption.text == task:
                    TestOption.click()
            except:pass
        WebDriverWait(Test, wait_time).until(EC.visibility_of_element_located((By.ID, "root")))
        WebDriverWait(Test, wait_time).until(EC.visibility_of_element_located((By.CLASS_NAME, "SystemTestDetails_rightIcon__1E11Q"))).click() # 点击答题
        try:WebDriverWait(Test, wait_time).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div[1]/div[2]/div"))).click() # 点击同意协议
        except:pass
        print(f"进入{task}答题页面...")
        for t in range(100):
            try:
                scores = WebDriverWait(Test, 2).until(EC.visibility_of_element_located((By.CLASS_NAME, "AnswerPage_num__QpO1_"))).text
                print(f"\n{task}答题--本次得分:{scores}")
                break
            except:pass
            try:
                print(f"\r尝试次数:{t+1}",end="",flush=True)
                question = WebDriverWait(Test, wait_time).until(EC.visibility_of_element_located((By.CLASS_NAME, "topic"))).text
                mask = WebDriverWait(Test, wait_time).until(EC.visibility_of_element_located((By.CLASS_NAME, "mask"))).text
                options:list = WebDriverWait(Test, wait_time).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "content")))
                print("\n\n"+question+mask)
                SelectedOptions = []
                for option in options:
                    print(f"{options.index(option)}:{option.text}")
                options_index = str(input("输入选项索引:"))

                for i in options_index:
                    i = int(i)
                    options[i].click()
                    SelectedOptions.append(options[i].text)
                try:
                    with open("internalTest/Collct/data/questions.json", "r", encoding="utf-8") as r:data = json.load(r)
                except:
                    data = {}
                data[question] = SelectedOptions
                with open("internalTest/Collct/data/questions.json", "w", encoding="utf-8") as w:json.dump(data,fp=w,indent=2,ensure_ascii=False)
                WebDriverWait(Test, wait_time).until(EC.visibility_of_element_located((By.CLASS_NAME, "button"))).click() # 点击下一题
            except:
                Test.refresh()
                pass