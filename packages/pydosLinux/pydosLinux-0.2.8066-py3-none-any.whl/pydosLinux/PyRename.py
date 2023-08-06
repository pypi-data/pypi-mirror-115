import os

print("PyRename  0.0.1(for Linux/macOS)")
srcName = input("请输入需要重命名目标文件或文件夹：")
dstName = input("请输入重命名后目标文件或文件夹：")


os.rename(srcName , dstName)