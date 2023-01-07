## 可用的内置第三方库

### 内置第三方库说明
由溪梦框架官方打包的可执行文件中，默认包含以下第三方库，可供插件导入运行。

如果需要使用其他库，请使用源代码运行。

#### 框架核心库
`运行框架时必须需要这些库`

- 彩色日志：`colorlog`

- HTTP 请求：`requests`

- 文件编码识别：`chardet`

- 计划任务：`apscheduler`

- INI配置文件：`configobj`

- Websocket连接：`websocket-client`

```
APScheduler==3.9.1.post1
backports.zoneinfo==0.2.1
certifi==2022.12.7
chardet==5.1.0
charset-normalizer==2.1.1
colorama==0.4.6
colorlog==6.7.0
configobj==5.0.6
idna==3.4
pytz==2022.7
pytz-deprecation-shim==0.1.0.post0
requests==2.28.1
six==1.16.0
tzdata==2022.7
tzlocal==4.2
urllib3==1.26.13
websocket-client==1.4.2
```
