## 基础教程

> 请注意，在大部分计算机操作中，达成目标的方法不唯一

!> 此文档为早期版本，说明并不完善，也可能存在错误，如有错误请加群进行反馈，或在 Github 中提出



### 下载

**从 [Release](https://github.com/funnygeeker/XiMeng/releases) 界面下载最新版本的溪梦框架**
- 溪梦框架暂时不计划提供 **Windows x86** 和 **Linux x86** 的可执行文件，由于打包环境受限，也暂时无法提供 **Linux arm** 的可执行文件
- 名称中含有 **“_windows”** 的文件代表含有 **windows_amd64** 平台适用的：溪梦框架可执行文件 和 go-cqhttp可执行文件
- 名称中含有 **“_linux”** 的文件代表含有 **linux_amd64** 平台适用的：溪梦框架可执行文件 和 go-cqhttp可执行文件
- 若需要其他在平台运行，请使用**源码运行**或**安装必要第三方库**后使用**pyinstaller**打包运行

!>Releases 中提供的 **go-cqhttp可执行文件** 仅仅是**为了方便小白使用**，若go-cqhttp的维护人员不希望我们这样做，请在GitHub中联系我们移除（附：go-cqhttp的[Github页面](https://github.com/Mrs4s/go-cqhttp)）


### 解压
- Windows下请运行下载到的WinRAR自解压文件进行解压
- Linux下在命令行中输入 `tar -xzvf [文件名]`


### 启动
#### Windows 标准方法
1. 将需要运行的插件带着文件夹一起拖入 `./plugin` 目录
2. 修改 `./config` 目录下的 `config.ini` 配置文件
3. 修改各个插件的目录下的配置文件（如果有）
4. 双击 `“一键启动.bat”` ，根据提示扫码登录

#### Linux GUI 标准方法
1. 修改 ./config 目录下的 config.ini 配置文件
2. 修改各个插件的目录下的配置文件（如果有）
3. 打开两个终端窗口，cd 到解压目录
4. 窗口A运行：
```
cd ./go-cqhttp
./go-cqhttp
```
5. 窗口B运行：
```
./main
```

#### Linux 命令行标准方法
1. 使用 Vim 修改 ./config 目录下的 config.ini 配置文件
2. 修改各个插件的目录下的配置文件（如果有）
3. 如果没有安装 screen ，请安装 screen
```
# CentOS
sudo yum install screen
# Debian/Ubuntu
sudo apt install screen
```
4. 命令输入
```
screen -R gocq 
```
5. cd 到解压目录
6. 命令输入
```
cd ./go-cqhttp
./go-cqhttp
```
7. 扫码登录
8. 使用 **Ctrl + A + D** 快捷键从screen会话中分离
9. 命令输入
```
screen -R xm 
```
10. cd 到解压目录
11. 命令输入
```
./main
```

>附：[go-cqhttp使用文档](https://docs.go-cqhttp.org/)   [screen命令使用](https://www.jianshu.com/p/e91746ef4058)

### 关闭
#### Windows 标准方法
1. 点击窗口右上角的 “X” 关闭 溪梦框架 窗口
2. 点击窗口右上角的 “X” 关闭 go-cqhttp 窗口

#### Linux GUI 标准方法
1. 使用 **Ctrl + C** 分别退出 溪梦框架 和 go-cqhttp
2. 关闭不需要使用的终端窗口

#### Linux 命令行标准方法
1. 使用 **Ctrl + C** 退出 溪梦框架
2. 命令输入
```
screen -R xm gocq
```
3. 使用 **Ctrl + C** 退出 go-cqhttp
4. 使用 **Ctrl + A + D** 快捷键从screen会话中分离



## 使用说明

### 插件
- 当您解压后，会看到名为 `piugin` 的文件夹
- 在 `plugin` 文件夹中可以放入各种插件，插件会在框架启动时加载
- 在 `plugin` 文件夹下有各种文件夹，每个文件夹都存放了不同的插件
- 您可以通过更改 `config` 目录下的 `config.ini` 来修改插件的加载设置
- 不建议您更改各个插件发布时的文件夹名，这可能会导致未做适配的插件在运行时出现错误

### 配置
- 当您解压后，会看到名为 `config` 的文件夹
- 在 `config` 文件夹中有各种配置文件，您可以通过修改配置文件来调整框架的运行设置



## 进阶教程

### 使用 Pyinstaller 编译源码
- 敬请期待（或者您也可以在 Github 或群里提交您编写的文档）

### 在 Docker 中部署
- 敬请期待（或者您也可以在 Github 或群里提交您编写的文档）

### 在云主机上部署
- 敬请期待（或者您也可以在 Github 或群里提交您编写的文档）