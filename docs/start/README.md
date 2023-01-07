## 基础教程


!> 此文档为早期版本，说明并不完善，也可能存在错误，如有错误请加群进行反馈，或在 Github 中提出



### 下载

**从 [Release](https://github.com/funnygeeker/keiyume/releases) 界面下载最新版本的溪梦框架**

!>本框架所需要的 go-cqhttp 请前往 go-cqhttp 的 [Release](https://github.com/Mrs4s/go-cqhttp/releases/) 自行下载


### 解压
- Windows 下请运行下载到的自解压文件进行解压
- Linux下在命令行中输入 `tar -xzvf [文件名]`


### 启动
#### Windows 标准方法
1. 将需要运行的插件带着文件夹一起拖入 `./plugins` 目录
2. 修改框架目录下的 `config.ini` 配置文件
3. 修改各个插件下的配置文件（如果有）
4. 启动 go-cqhttp，[教程](https://docs.go-cqhttp.org/guide/quick_start.html#%E5%9F%BA%E7%A1%80%E6%95%99%E7%A8%8B)
5. 启动框架目录下的 `main.exe`

#### Linux 标准方法
1. 将需要运行的插件带着文件夹一起拖入 `./plugins` 目录
2. 修改框架目录下的 `config.ini` 配置文件
3. 修改各个插件下的配置文件（如果有）
4. 启动 go-cqhttp，[教程](https://docs.go-cqhttp.org/guide/quick_start.html#%E5%9F%BA%E7%A1%80%E6%95%99%E7%A8%8B)
5. 启动框架目录下的 `main` 或 `mian.py`

>附：[go-cqhttp使用文档](https://docs.go-cqhttp.org/)   [screen命令使用](https://www.jianshu.com/p/e91746ef4058)

### 关闭
- 关闭框架时可以在框架中直接输入 `exit` 进行退出
- 也可以通过结束框架的程序退出


## 使用说明

### 插件
- 当您解压后，会看到名为 `piugins` 的文件夹
- 在 `plugins` 文件夹中可以放入各种插件，插件会在框架启动时加载
- 在 `plugins` 文件夹下有各种文件夹，每个文件夹都存放了不同的插件
- 您可以通过更改框架所在目录下的 `config.ini` 来修改插件的加载设置
- 不建议您更改各个插件发布时的文件夹名，这可能会导致未做适配的插件在运行时出现错误

### 配置
- 当您解压后，会看到名为 `config.ini` 的配置文件
- 在配置文件中，您可以通过修改各项设置来调整框架的运行设置


## 进阶教程

### 使用 Pyinstaller 编译源码
- 敬请期待（或者您也可以在 Github 或群里提交您编写的文档）

### 在 Docker 中部署
- 敬请期待（或者您也可以在 Github 或群里提交您编写的文档）

### 在云主机上部署
- 敬请期待（或者您也可以在 Github 或群里提交您编写的文档）

### 在手机上部署
- 敬请期待（或者您也可以在 Github 或群里提交您编写的文档）