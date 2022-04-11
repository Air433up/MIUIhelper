# 此处是新坑
* [旧版在这](https://github.com/azurstar/MIUIhelper/tree/main)  

* <a target="_blank" href="https://qm.qq.com/cgi-bin/qm/qr?k=pXxSae9XLz6Sid63B1zDlAM7gFTEc_Pm&jump_from=webapi"><img border="0" src="//user-images.githubusercontent.com/91844313/162752581-15a414ab-50bb-4dd3-b13b-001e6dc245cd.jpg" alt="" title="一个小群"></a>

## 声明
* 使用 MIUIhelper  即表明，您知情并同意：  
    * 该项目仅供学习交流，严禁用于商业用途  
    * MIUIhelper 不会对您的任何损失负责，包括但不限于账号异常、核弹爆炸、第三次世界大战等

## 使用  
* 使用的第三方库
```
pip3 install requests_toolbelt
pip3 install requests
```

* 每日任务  
    * 每日五题(10分)和每日打开App(4分)  
    * 将账号密码填入`Daily\data\accounts.json`  
    * 在该项目的根目录下输入`python3 daily.py`即可运行  
        * 建议设置定时运行  
        * 若出现未收录题目将会随机选择, 并在之后自动收录题目的正确选项  
    * 青龙面板部署:
        * 将以下命令添加至`定时任务`并运行  

        ```
        ql repo https://github.com/azurstar/MIUIhelper.git Daily/ql_panel
        ```

        * 立即执行一次产生的`main.py`生成所需json文件 
        * 在Python3的依赖管理中添加`requests_toolbelt`和`requests`  
        * 然后在生成的`accounts.json`中填入所需的账号即可  
        * 若账号在非常用设备上登录, 可能会需要验证码, 使用该设备自行前去验证https://web-alpha.vip.miui.com/page/info/mio/mio/internalTest

* 测试答题    
    * 将账号密码填入`Test\data\accounts.json`,tasks对应需要答题的测试项目,具体查看[相关参数](#相关参数)  
    * 在该项目的根目录下输入`python3 test.py`即可运行  
    * 注意: 请避免使用后台运行, 若出现未收录的题目需要自行判断!  

* 自定义机型申请      
    * 将账号密码填入`Apply\data\accounts.json`,devices对应需要申请的设备代号  
    * 在该项目的根目录下输入`python3 apply.py`即可运行  

## 待解决  
* 写readme...

## 已解决  
* 自定义内测机型申请  
* 三项内测答题  
* 每日打开app的4分  
* 每日五题  
* cookie更新  

## 相关参数  
|  项目id  |  项目名称  |
|  ----  |  ----  |
|  10001  |  开发版公测  |
|  10002  |  开发版内测  |
|  10003  |  稳定版内测  |

## 记录一下需要的信息  
* https://web-alpha.vip.miui.com/page/info/mio/mio/internalTest  
* https://miuiver.com/xiaomi-device-codename/  
 
