import json
import logging
import os.path
import shutil
import sys
import urllib.request

from util import AppSetting

from util.RunBat import runBat

RELEASE_LATEST_API_URL = "https://api.github.com/repos/JhihJian/Jhih_Ai_Assistant/releases/latest"
import urllib.request


def getFileNameFromUrl(url):
    # url = "http://www.computersolution.tech/wp-content/uploads/2016/05/tutorialspoint-logo.png"
    if url.find('/'):
        return (url.rsplit('/', 1)[1])


cmd_file_content = """

waitfor SomethingThatIsNeverHappening /t 3 >NUL

powershell Expand-Archive guyu-v*.*.*-windows-amd64.zip -DestinationPath . 

move /Y dist\* .

rmdir dist

start %~dp0Guyu.exe

del /f guyu-v*.*.*-windows-amd64.zip

(goto) 2>nul & del "%~f0"

pause
"""


def downloadFileFromUrl(download_url, store_dir):
    file_name = getFileNameFromUrl(download_url)
    file_path = os.path.join(store_dir, file_name)
    # 如果文件存在就直接跳过下载
    if os.path.isfile(file_path):
        return file_path
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
    def __init__(self):
        self.logger = logging.getLogger("MainWindow")

    # 检查更新
    def checkForUpdate(self):
        try:
            contents = urllib.request.urlopen(RELEASE_LATEST_API_URL).read()
            result = json.loads(contents)
            self.release_version = result["tag_name"]
            self.logger.info("query latest release:{}".format(self.release_version))
            if AppSetting.APP_VERSION == self.release_version:
                return False
            self.download_url = self.__getDownloadUrl__(result)

            return True
        except Exception as e:
            self.logger.error("check for update failed:{}".format(e))

    # app_quit_hook 退出app的函数
    def updateApp(self, quit_app_hook):
        # 下载安装包
        store_dir = os.path.dirname(sys.executable)
        self.logger.info("begin download release file...")
        release_file_path = downloadFileFromUrl(self.download_url, store_dir)
        self.logger.info("download {} release in {}".format(self.release_version, release_file_path))
        # 运行bat
        bat_file_path = os.path.join(os.path.dirname(sys.executable), "update.bat")
        with open(bat_file_path, 'w') as f:
            f.writelines(cmd_file_content)

        p = runBat(bat_file_path)
        self.logger.info("run update bat pid:{}".format(p.pid))
        self.logger.info("退出程序...")
        # 退出程序
        quit_app_hook()
        os._exit(0)

    def __getDownloadUrl__(self, result):
        assets = result["assets"]
        for asset in assets:
            browser_download_url = asset["browser_download_url"]
            if "windows-amd64" in browser_download_url:
                return browser_download_url
        raise Exception("not parse release download url")

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
