#系统BL程序

def bootloader():
    import time
    print("BootLoader running....done")
    time.sleep(1)
    from pydosLinux import sysver
    sysver.sysver()
    print("System Staring....")
    print("Welcome to PyDos")
    print()
    print()
    print()
    print()
    from pydosLinux import kernel
    kernel.kernel()