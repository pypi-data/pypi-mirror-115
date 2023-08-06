import sys, platform, time

from requests.api import patch
def sysver():
    sysVer = "PyDOS 0.2 Mn  PyShell 2.0 Cheetah  Build at 2021.8.5"
    print(sysVer)

    print("*support: https://gitee.com/yizhigezi_yijiafeiji/py-dos/blob/master/README.md")
    print("*Official website: https://gitee.com/yizhigezi_yijiafeiji/py-dos/tree/master")
    print("*Feedback: https://gitee.com/yizhigezi_yijiafeiji/py-dos/issues")
    print()
    a = sys.version_info
    print("Python Runtime Ver: {a[0]}.{a[1]}.{a[2]}".format(a=a))

    ret = {}

    plat_form = platform.platform()
    if "Linux" in plat_form:
        ret["plat_form"] = "Linux"
    else:
        ret['plat_form'] = "Mac"

    ret["version"] = platform.version()
    ret['version_bit'] = platform.architecture()[0][0:2]
    print("*Platform OS:{ret[plat_form]}".format(ret=ret))
    print("*Platform OS Version: {ret}".format(ret=ret['version'].split(" ")[0]))
    print("*{ret[version_bit]}Bit OS".format(ret=ret))

    print("本项目基于MIT开源协议")

    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    print("*System information as of ", date)
