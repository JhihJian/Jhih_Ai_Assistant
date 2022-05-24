import json
import logging
import os.path
import shutil
import sys
import urllib.request
import zipfile

RELEASE_LATEST_API_URL = "https://api.github.com/repos/JhihJian/Jhih_Ai_Assistant/releases/latest"
import urllib.request


def getFileNameFromUrl(url):
    # url = "http://www.computersolution.tech/wp-content/uploads/2016/05/tutorialspoint-logo.png"
    if url.find('/'):
        return (url.rsplit('/', 1)[1])


cmd_file_content = """
@ECHO OFF

:LOOP
tasklist | find /i "Guyu" >nul 2>&1
IF ERRORLEVEL 1 (
  GOTO CONTINUE
) ELSE (
  ECHO Guyu is still running
  Timeout /T 5 /Nobreak
  GOTO LOOP
)

:CONTINUE



powershell Expand-Archive guyu-v*.*.*-windows-amd64.zip -DestinationPath .

move /Y dist\* .

rmdir dist

(goto) 2>nul & del "%~f0"
"""


def downloadFileFromUrl_retrieve(download_url, store_dir):
    file_name = getFileNameFromUrl(download_url)
    file_path = os.path.join(store_dir, file_name)
    urllib.request.urlretrieve(download_url, file_path)
    return file_path


def downloadFileFromUrl(download_url, store_dir):
    file_name = getFileNameFromUrl(download_url)
    file_path = os.path.join(store_dir, file_name)
    # TODO 改为使用配置
    # 使用代理
    proxy_support = urllib.request.ProxyHandler({'http': 'localhost:10809',
                                                 'https': 'localhost:10809'})
    opener = urllib.request.build_opener(proxy_support)

    req = urllib.request.Request(url=download_url)

    # proxy_host = 'localhost:10809'
    # req.set_proxy(proxy_host, 'https')
    with opener.open(req) as response:
        # Create a file objec t
        with open(file_path, "wb") as f:
            # Copy the binary content of the response to the file
            shutil.copyfileobj(response, f)

    return file_path


class AutoUpdate:
    def __init__(self, current_version):
        self.logger = logging.getLogger("MainWindow")
        self.current_version = current_version

    def __isSameVersion__(self, version):
        return self.current_version == version

    # 检查更新
    def checkForUpdate(self):
        try:
            contents = urllib.request.urlopen(RELEASE_LATEST_API_URL).read()
            result = json.loads(contents)
            version = result["tag_name"]
            self.logger.info("query latest release:{}".format(version))
            if self.__isSameVersion__(version):
                return ""
            download_url = self.__getDownloadUrl__(result)
            store_dir = os.path.dirname(sys.executable)
            self.logger.info("begin download release file...")
            release_file_path = downloadFileFromUrl(download_url, store_dir)
            self.logger.info("download {} release in {}".format(version, release_file_path))
            return release_file_path
        except Exception as e:
            self.logger.error("check for update failed:{}".format(e))

    def updateApp(self):
        bat_file_path = os.path.join(os.path.dirname(sys.executable), "update.bat")
        with open(bat_file_path, 'w') as f:
            f.writelines(cmd_file_content)
        os.system(bat_file_path)
        sys.exit()

    def __getDownloadUrl__(self, result):
        assets = result["assets"]
        for asset in assets:
            browser_download_url = asset["browser_download_url"]
            if "windows-amd64" in browser_download_url:
                return browser_download_url
        raise Exception("not parse release download url")

    def config_log(self):
        # 日志基本配置
        log_format = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.logger.setLevel(logging.DEBUG)
        # 文件日志输出
        log_file_path = os.path.join(os.path.dirname(sys.executable), 'MainWindow.log')
        print(log_file_path)
        fh = logging.FileHandler(log_file_path)
        fh.setFormatter(log_format)
        self.logger.addHandler(fh)
        # 控制台日志输出
        ch = logging.StreamHandler()
        ch.setFormatter(log_format)
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)
        self.logger.info('程序已启动')

    def __install_release__(self, file_path):
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall("targetdir")


if __name__ == '__main__':
    ud = AutoUpdate("v0.0.0")
    if ud.checkForUpdate():
        ud.updateApp()

    # from urllib import request as urlrequest
    #
    # proxy_host = 'localhost:10809'  # host and port of your proxy
    # url = 'https://www.github.com'
    #
    # req = urlrequest.Request(url)
    # req.set_proxy(proxy_host, 'https')
    #
    # response = urlrequest.urlopen(req)
    # print(response.read().decode('utf8'))

# curl url result example
# {'url': 'https://api.github.com/repos/JhihJian/Jhih_Ai_Assistant/releases/67532623',
#  'assets_url': 'https://api.github.com/repos/JhihJian/Jhih_Ai_Assistant/releases/67532623/assets',
#  'upload_url': 'https://uploads.github.com/repos/JhihJian/Jhih_Ai_Assistant/releases/67532623/assets{?name,label}',
#  'html_url': 'https://github.com/JhihJian/Jhih_Ai_Assistant/releases/tag/v1.0.0', 'id': 67532623,
#  'author': {'login': 'github-actions[bot]', 'id': 41898282, 'node_id': 'MDM6Qm90NDE4OTgyODI=',
#             'avatar_url': 'https://avatars.githubusercontent.com/in/15368?v=4', 'gravatar_id': '',
#             'url': 'https://api.github.com/users/github-actions%5Bbot%5D',
#             'html_url': 'https://github.com/apps/github-actions',
#             'followers_url': 'https://api.github.com/users/github-actions%5Bbot%5D/followers',
#             'following_url': 'https://api.github.com/users/github-actions%5Bbot%5D/following{/other_user}',
#             'gists_url': 'https://api.github.com/users/github-actions%5Bbot%5D/gists{/gist_id}',
#             'starred_url': 'https://api.github.com/users/github-actions%5Bbot%5D/starred{/owner}{/repo}',
#             'subscriptions_url': 'https://api.github.com/users/github-actions%5Bbot%5D/subscriptions',
#             'organizations_url': 'https://api.github.com/users/github-actions%5Bbot%5D/orgs',
#             'repos_url': 'https://api.github.com/users/github-actions%5Bbot%5D/repos',
#             'events_url': 'https://api.github.com/users/github-actions%5Bbot%5D/events{/privacy}',
#             'received_events_url': 'https://api.github.com/users/github-actions%5Bbot%5D/received_events',
#             'type': 'Bot', 'site_admin': False}, 'node_id': 'RE_kwDOG42Xjc4EBndP', 'tag_name': 'v1.0.0',
#  'target_commitish': 'main', 'name': 'Guyu v1.0.0', 'draft': False, 'prerelease': False,
#  'created_at': '2022-05-23T10:40:07Z', 'published_at': '2022-05-23T11:26:00Z', 'assets': [
#     {'url': 'https://api.github.com/repos/JhihJian/Jhih_Ai_Assistant/releases/assets/66352022', 'id': 66352022,
#      'node_id': 'RA_kwDOG42Xjc4D9HOW', 'name': 'guyu-v1.0.0-windows-amd64.zip', 'label': '',
#      'uploader': {'login': 'github-actions[bot]', 'id': 41898282, 'node_id': 'MDM6Qm90NDE4OTgyODI=',
#                   'avatar_url': 'https://avatars.githubusercontent.com/in/15368?v=4', 'gravatar_id': '',
#                   'url': 'https://api.github.com/users/github-actions%5Bbot%5D',
#                   'html_url': 'https://github.com/apps/github-actions',
#                   'followers_url': 'https://api.github.com/users/github-actions%5Bbot%5D/followers',
#                   'following_url': 'https://api.github.com/users/github-actions%5Bbot%5D/following{/other_user}',
#                   'gists_url': 'https://api.github.com/users/github-actions%5Bbot%5D/gists{/gist_id}',
#                   'starred_url': 'https://api.github.com/users/github-actions%5Bbot%5D/starred{/owner}{/repo}',
#                   'subscriptions_url': 'https://api.github.com/users/github-actions%5Bbot%5D/subscriptions',
#                   'organizations_url': 'https://api.github.com/users/github-actions%5Bbot%5D/orgs',
#                   'repos_url': 'https://api.github.com/users/github-actions%5Bbot%5D/repos',
#                   'events_url': 'https://api.github.com/users/github-actions%5Bbot%5D/events{/privacy}',
#                   'received_events_url': 'https://api.github.com/users/github-actions%5Bbot%5D/received_events',
#                   'type': 'Bot', 'site_admin': False}, 'content_type': 'raw', 'state': 'uploaded', 'size': 36356238,
#      'download_count': 0, 'created_at': '2022-05-23T11:26:01Z', 'updated_at': '2022-05-23T11:26:02Z',
#      'browser_download_url': 'https://github.com/JhihJian/Jhih_Ai_Assistant/releases/download/v1.0.0/guyu-v1.0.0-windows-amd64.zip'}],
#  'tarball_url': 'https://api.github.com/repos/JhihJian/Jhih_Ai_Assistant/tarball/v1.0.0',
#  'zipball_url': 'https://api.github.com/repos/JhihJian/Jhih_Ai_Assistant/zipball/v1.0.0',
#  'body': '1.0.0版本发布\r\n\r\n已完成的功能 🎉\r\n\r\n- GitHub Package Action\r\n- 开机自启设置\r\n- 监测在游戏内禁用Win键\r\n- 日志界面\r\n\r\n1.0.1版本的计划 🛠\r\n\r\n- 增加 qq消息监听\r\n- GitHub Page 健康检查\r\n- 软件自动更新'}
