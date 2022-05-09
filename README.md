# Jhih_Ai_Assistant

安装

阿里云sdk nls包

```
cd ./lib/alibabacloud-nls-python-sdk-0.0.1 
pip install -r requirements.txt 
python -m pip install .
```

语音交互 Ai智能助手

## 打包

`pyinstaller .\guyu.spec`

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