pyinstaller .\__init__.spec


## 发版本

1. 修改 RELEASE.md
2. AppSetting.py
3. 创建Tag `git tag v1.0.0` 并提交 `git push origin --tags`

注：

删除tag

本地 `git tag -d v1.1.0`

远程 `git push origin tag -d v1.1.0`