print("ASCII转换器，0.0.2 by 一架飞稽")
print("模式1：字符转为ASCII码  ；模式2：ASCII转为字符")
c = int(input("请选择一个模式"))

if c == 1 :
    name = input("输入字符：")
    print(name+"的ASCII码为：",ord(name))
elif c == 2 :
    ascii = int(input("输入ASCII码："))
    print(ascii, "的字符为：", chr(ascii))