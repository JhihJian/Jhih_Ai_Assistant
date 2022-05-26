import os
import subprocess

import wmi

Listary_Path = "C:\\0-Portable\\ListaryPortable\\Listary.exe"
Listary_Name = "Listary.exe"


def runProgram(program_path):
    # os.system(program_path)
    # 以上会将新进程作为子程序执行
    subprocess.Popen(program_path, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)


def killProgram(program_name):
    # os.system(f"taskkill /F /IM {app_name}")
    # subprocess.Popen(f"taskkill /F /IM {app_name}", shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    # 以上两种方式都会报 ，权限不够的错误

    f = wmi.WMI()
    ti = 0
    for process in f.Win32_Process():
        if process.name == program_name:
            process.Terminate()
            ti += 1

    if ti == 0:
        print("Process not found!!!")


if __name__ == '__main__':
    # killProgram(Listary_Name)
    # runProgram(Listary_Path)

    def test():
        print("a")


    def print_function_name(function):
        print(f"{function.__name__}")


    print_function_name(test)
