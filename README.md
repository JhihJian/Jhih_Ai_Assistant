# Jhih_Ai_Assistant


语音交互 Ai智能助手

## 功能点
1. 学习辅助
2. 身体健康监控
3. 学习辅助

## 安装依赖
### 基本以来
pip -r install requirement.txt



### 语音输入支持 pyaudio


cd InstallGuide
pip install PyAudio-0.2.11-cp38-cp38-win_amd64.whl


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