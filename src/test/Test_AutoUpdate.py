import unittest

from util.AutoUpdate import *


class Test_AutoUpdate(unittest.TestCase):
    def test_getFileNameFromUrl(self):
        file_name = getFileNameFromUrl(
            "http://www.computersolution.tech/wp-content/uploads/2016/05/tutorialspoint-logo.png")
        self.assertEqual("tutorialspoint-logo.png", file_name)
        file_name = getFileNameFromUrl(
            "https://github.com/JhihJian/Jhih_Ai_Assistant/releases/download/v1.0.0/guyu-v1.0.0-windows-amd64.zip")
        self.assertEqual("guyu-v1.0.0-windows-amd64.zip", file_name)

    def test_downloadFileFromUrlWithBar(self):
        url = "https://github.com/JhihJian/Jhih_Ai_Assistant/releases/download/v1.0.0/guyu-v1.0.0-windows-amd64.zip"
        downloadFileFromUrl(url, "K:\\3-WorkSpace\\2-Python-Projects\\Jhih_Ai_Assistant")
