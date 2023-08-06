import os
import sys

print("PyKernel 2.0 Cheetah")
print("On py-dos")

path = sys.path
spath = path[5]
pydosPath = spath + '/pydosLinux/'

prompt = "C:\>"

while True:
    command = input(prompt)
    cCode = "python3 " + pydosPath + command + ".py"
    if command == "exit":
        print("Bye")
        break
    else:
        os.system(cCode)