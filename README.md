# Jhih_Ai_Assistant

TODO

1. 升级用线程 无法直接退出，用立即重启对话框
2. 计时提醒
3. 任务栏图标，最小化托盘图标
4. 功能启动中，按钮提示并设置disable
5. guyu qq 输入数字使用功能
6. 分数共同保存

-----------------------------------
pynput 以async模式使用

pynput 示例包含使用 pynput 的两种不同变体，您需要从中选择后者，因为它更容易连接到 asyncio。键盘侦听器将允许程序继续执行 asyncio 事件循环，同时从单独的线程调用回调。


-----------------------------------
使用qt界面，再使用multiprocessing 会导致新创建进程，再次作MainWindows 的init操作 会出现多个窗口，不停的创建

解决方法，在main下调用`multiprocessing.freeze_support()`

在qt应用中，每个被创建的进程都应该有个窗口，所以会默认提供窗口的初始化

每个 kivy 应用程序都有自己的窗口，您正在启动另一个应用程序。如果您不想要窗口，只需将其设为纯 Python（不是 kivy 应用程序）？请注意，多处理在 iOS 中不可用，

当您“创建线程”时，您不会创建线程，而是启动第二个 python 解释器，该解释器首先使用一些管道、套接字或共享内存魔法连接。因为 GIL 你没有更好的方法在 python 中完全加载
cpu，所以唯一的修复方法是检查线程并通过创建第二个窗口。

如果您在 Windows 上，多处理将启动导入主模块的新进程。确保通过将 GUI 创建代码放在下面来保护它if __name__ == '__main__':

更好的是，为了避免在子进程中不必要地导入 PyQt 的开销，创建一个简单的新主模块，如下所示：

```
if __name__ == '__main__':
    import old_main_module
    old_main_module.main()
```

----------------------
Git push 报错

test

```commandline
error: dst refspec main matches more than one
```

git pull 报错

```
fatal: refusing to merge unrelated histories
```

--allow-unrelated-histories


有branch和tag 同名的情况 删除分支 `git push origin :refs/tags/<tagname>`
----------------------
自动更新功能

1. 怎么知道有新的版本号
   https://github.com/JhihJian/Jhih_Ai_Assistant/releases/latest

2. 怎么下载最新的release包
   https://github.com/JhihJian/Jhih_Ai_Assistant/releases/download/v1.0.0/guyu-v1.0.0-windows-amd64.zip

3. 项目需要公开，否则无法访问release，既然要公开就必须得脱敏

使用bfg工具 删除敏感文件提交历史 [下载|文档]( https://rtyley.github.io/bfg-repo-cleaner/)

1. 下载jar包到根目录
2. `java -jar bfg.jar --no-blob-protection --delete-files AliRecognizer.py` AliRecognizer.py 为要清除记录的文件
3. `git reflog expire --expire=now --all && git gc --prune=now --aggressive`
   还是能查到 https://github.com/JhihJian/Jhih_Ai_Assistant/blob/a1435d3fc717f4f2815e6880a1d096a2007c182d/src/function/AliRecognizer.py?spm=5176.12948882.sas.7.448369c6GGLeqO&file=AliRecognizer.py

搞了两种方法，都无法完全删除，搞了半天，翻到最下面，还要联系支持。。。 不说了，改key 去了

从 GitHub 中完全删除数据 在使用 BFG 工具或git filter-repo删除敏感数据并将更改推送到 GitHub 后，您必须采取更多步骤才能从 GitHub 中完全删除数据。

联系GitHub 支持，要求他们删除缓存的视图和对 GitHub 上拉取请求中敏感数据的引用。请提供存储库的名称和/或您需要删除的提交的链接。

下载release过程中遇到问题
`urllib.request.urlretrieve(download_url, file_path)`
报错
`TimeoutError: [WinError 10060] 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。`

使用代理 写法一

```python
import urllib

proxy_support = urllib.request.ProxyHandler({'http': 'localhost:10809',
                                             'https': 'localhost:10809'})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)
urllib.request.urlopen("http://www.google.com")



```

写法二

```python
from urllib import request as urlrequest

proxy_host = 'localhost:10809'  # host and port of your proxy
url = 'http://www.httpbin.org/ip'

req = urlrequest.Request(url)
req.set_proxy(proxy_host, 'http')

response = urlrequest.urlopen(req)
print(response.read().decode('utf8'))
```

自动更新时，调用QApplication.quit() 退出进程,好像会导致 调用MainWindow.__init__()方法

sys.exit() 在线程内调用，只会退出线程

线程中调用process 启动进程会报错 `AttributeError: Can't get attribute 'f' on <module '__main__' (built-in)>`

原因 多进程执行的函数在某一个函数内部，如果是，那么就会报上述错误。解决办法是把那个函数放到这个函数外面

正确的qt进程 退出方法 closing = QCloseEvent()
window.closeEvent(closing)
在方法内关闭线程

app.shutdown()

```
import os
import threading
from multiprocessing import Process


def f():
    os.system('{}'.format("sleeper.bat"))


def runProcess():
    p = Process(target=f)
    p.start()


if __name__ == '__main__':
    t = threading.Thread(target=runProcess)
    print("thread ready")
    t.start()
    print("main finish")

```

----------------------

## 发版本

1. 修改 RELEASE.md
2. 创建Tag `git tag v1.0.0` 并提交 `git push origin --tags`

注：

删除tag

本地 `git tag -d v1.0.0`

远程 `git push origin tag -d v1.0.0`

----------------------
1.0.0版本包括以下内容

    - title: 已完成的功能 🎉
      labels:
        - GitHub Package Action
        - 开机自启设置
        - 监测在游戏内禁用Win键
        - 日志界面

    - title: 1.0.1版本的计划 🛠
      labels:
        - 增加 qq消息监听
        - GitHub Page 健康检查
        - 软件自动更新

**Full Changelog**: https://github.com/JhihJian/Jhih_Ai_Assistant/commits/1.0.0

guyu-1.0.0-windows-amd64.zip

Python 版本 3.8.10


-------------------------
功能管理

1. 功能注册,功能名称，配置信息
2. 查询功能当前状态
3. 启动功能
4. 结束功能

---------------------------------------------------------------------
主体：

- 数据库连接
- ui界面
- qq监听
- 语音识别
- 语音唤醒
- 插件管理

插件：

- 分数对话
- 按键禁用
- 检查网站

功能列表

1. 监听qq消息
2. 按键禁用

-------------------------------------------------------------------

### 打包

`pyinstaller .\__init__.spec`

遇到问题，打包的时候，resources_rc.py没有加载，运行Guyu.exe 报错，No module name resources_rc

因为生成路径不对

import resources_rc 改为 import gui.resources_rc

pyside6-uic 增加参数 --from-imports

遇到问题，设置注册表自动启动后，无法应用无法随windows启动，报错 plyvel._plyvel.Error: b'NotFound: guyu-db/LOCK:

创建DB时使用的是相对路径，所以出错 plyvel.DB("guyu-db")
改为 plyvel.DB(os.path.join(os.path.dirname(sys.executable), DB_NAME))

-------------------------------------------------------------------

### 编译

qt ui file to python file --import- from=gui
`pyside6-uic --from-imports asserts/MainWindows.ui -o src/gui/Ui_MainWindows.py`

qt resource file to python file，注意，这个名字my_r_rc 要和ui py导入中的相同

`pyside6-rcc -o src/gui/resources_rc.py asserts/resources.qrc`

使用自定组件

`pyside6-uic asserts/FunctionItem.ui -o src/gui/Ui_FuntionItem.py`
-------------------------------------------------------------------
待完成功能

1. 上线 下线通知
2. 加分协商
3. 运动日安排
4. 日志

plyvel 使用leveldb 作嵌入式数据库

联合了qq机器人， 功能 注册机器人服务开机自启

```
nssm install GuyuQQ
配置
Application
- Path  start.cmd的路径
- Startup directory start.cmd的目录
Details
- DisplayName GuyuQQService
Sevice name:GuyuQQ 
```

注：[nssm 下载地址](http://nssm.cc/download)
阿里云sdk nls包

```
cd ./lib/alibabacloud-nls-python-sdk-0.0.1 
pip install -r requirements.txt 
python -m pip install .
```

语音交互 Ai智能助手

## 功能点

1. 学习辅助
2. 身体健康监控
3. 学习辅助
4. 知识学习 对是否只是进行学习存储，当问询时能够回答

## 逻辑结构

语音唤醒 -> 语音识别 -> 语义分析 -> 执行命令 -> 语音合成

## 使用的相关依赖

1. PySimpleGUI 提供python ui实现
   https://github.com/PySimpleGUI/PySimpleGUI

## 安装依赖

### 基本以来

pip -r install requirement.txt

### 语音输入支持 pyaudio

cd Guide

pip install PyAudio-0.2.11-cp38-cp38-win_amd64.whl

在docker 中安装

该错误基本上是由丢失的portaudio.h文件引起的，它抱怨找不到它。

PyAudio 依赖于 Portaudio，它是一个免费的、跨平台的、开源的音频 I/O 库。

解决方案 将这些行添加到您的 Dockerfile ：

RUN apt-get update RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y RUN pip install
pyaudio

### 语音识别支持 (阿里云API)

#### 开通服务

你需要先到阿云开发者控制台开通 **RAM访问控制** ，进入 **RAM访问控制** 的控制台，新建一个用户，记下它的 **accessID**、**accessKey**，然后再为它添加 **管理智能语音交互（NLS）** 的权限。

接下来开通 **智能语音交互** 服务，新建一个项目：

- 类别：非电话
- 分类：通用
- 场景：中文普通话 或 其它语言（想识别哪个语言就用哪个）

#### 阿里云依赖

```
pip install aliyun-python-sdk-core==2.13.3
```

```
测试
cd alibabacloud-nls-python-sdk
python setup.py bdist_egg
python setup.py install 
```

#### 训练语音唤醒

https://github.com/mycroftai/mycroft-precise

pip install -r requirements.txt

安装ubuntu

#### 在docker 使用windows 的麦克风

I was able to get playback on Windows using pulseaudio.exe.

1] Download pulseaudio for windows: https://www.freedesktop.org/wiki/Software/PulseAudio/Ports/Windows/Support/

2] Uncompress and change the config files.

2a] Add the following line to your $INSTALL_DIR/etc/pulse/default.pa:

load-module module-native-protocol-tcp listen=0.0.0.0 auth-anonymous=1 This is an insecure setting: there are IP-based
ones that are more secure but there's some Docker sorcery involved in leveraging them I think. While the process is
running anyone on your network will be able to push sound to this port; this risk will be acceptable for most users.

2b] Change $INSTALL_DIR/etc/pulse//etc/pulse/daemon.conf line to read: exit-idle-time = -1

This will keep the daemon open after the last client disconnects.

3) Run pulseaudio.exe. You can run it as

start "" /B "pulseaudio.exe"
to background it but its tricker to kill than just a simple execution.

4) In the container's shell:

export PULSE_SERVER=tcp:127.0.0.1 One of the articles I sourced this
from (https://token2shell.com/howto/x410/enabling-sound-in-wsl-ubuntu-let-it-sing/) suggests recording may be blocked in
Windows 10.

### WSL ubuntu

https://docs.microsoft.com/en-us/windows/wsl/install-manual
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

curl.exe -L -o ubuntu-2004.appx https://aka.ms/wslubuntu2004

Add-AppxPackage .\ubuntu-2004.appx

问题 安装无效 没报错 Rename-Item .\ubuntu-2004.appx .\Ubuntu.zip Expand-Archive .\Ubuntu.zip .\Ubuntu

解决方法，直接解压 运行exe安装

System information as of Wed Feb 23 14:19:00 DST 2022

System load:            0.52 Usage of /home:         unknown Memory usage:           42% Swap usage:             0%
Processes:              7 Users logged in:        0 IPv4 address for eth1:  172.18.82.193 IPv4 address for wifi0:
10.63.228.88 IPv6 address for wifi0: 2001:da8:204:1921:6:a3fd:751:f73

```
问题
'Add-AppxPackage' is not recognized as an internal or external command

解决 
管理员模式

docker pull ubuntu
```

换源 sudo cp /etc/apt/sources.list /etc/apt/sources.list_backup sudo vim /etc/apt/sources.list

deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse

deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse

deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse

deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse

deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse

# deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse focal

sudo apt-get update

sudo apt-get upgrade

sudo apt-get install build-essential

#### 开启麦克风功能

遇到问题 启动 .\pulseaudio.exe 失败 pulsecore/core-util.c: Secure directory creation not supported on Win32.

开启服务 .\nssm.exe install PulseAudio

参数 -F C:\0-Portable\pulseaudio\etc\pulse\config.pa --exit-idle-time=-1 Details - Display Name :PulseAudio

在任务管理器Services里启动 PulseAudio

卸载方法 ./nssm.exe remove PulseAudio

在wsl ubuntu 中 sudo add-apt-repository ppa:therealkenc/wsl-pulseaudio 或者

sudo vim /etc/apt/sources.list

deb https://ppa.launchpadcontent.net/therealkenc/wsl-pulseaudio/ubuntu xenial main
deb-src https://ppa.launchpadcontent.net/therealkenc/wsl-pulseaudio/ubuntu xenial main

sudo apt-get update

遇到问题 wsl ping 不通主机，主机可以ping通ubuntu 把主机防火墙关了就成功

pulseaudio -nC 遇到问题 启动报错  
E: [pulseaudio] core-util.c: Failed to connect to system bus: Failed to connect to socket
/var/run/dbus/system_bus_socket: No such file or directory server-lookup.c: Unable to contact D-Bus

解决方法 sudo /etc/init.d/dbus start

遇到问题 shared memfd open() failed: Function not implemented

#### 测试麦克风

使用 arecord 和 aplay 工具.其中 arecord 查看 microphone (capture or input device):
sudo apt install alsa-utils arecord -l aplay -l 查看 speaker (output device) :

sudo apt install cmus cmus is a small, fast and powerful console music player for Unix-like operating systems.

遇到问题 nano打开不显示任何东西 wsl ubuntu

解决方法 export TERM=xterm-color And to make it permanent add it to your ~/.profile or ~/.bashrc

### 安装 Windows 终端

curl.exe -L -o windows-terminal.appx https://aka.ms/windows-terminal
Windows Terminal Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol
= [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient)
.DownloadString('https://community.chocolatey.org/install.ps1'))

https://github.com/microsoft/terminal

Add-AppxPackage Microsoft.WindowsTerminalPreview_1.12.10394.0_8wekyb3d8bbwe.msixbundle

C:\0-Portable\pulseaudio-1.1

export PULSE_SERVER=tcp:127.0.0.1

docker run -d -p 8182:8182 -e PULSE_SERVER=tcp:127.0.0.1 --name mycroft_precise_train ubuntu

按照这个设置
https://www.linuxuprising.com/2021/03/how-to-get-sound-pulseaudio-to-work-on.html