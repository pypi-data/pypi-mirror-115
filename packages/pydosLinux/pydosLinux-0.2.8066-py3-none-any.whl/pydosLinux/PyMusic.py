import tkinter
from tkinter import Button
from tkinter import Entry
from tkinter import Scale
from tkinter import Label
from PIL import Image, ImageTk
from tkinter import Toplevel
from pymediainfo import MediaInfo
import re
from tkinter import Message
import threading
import pygame
import time
import os
import random
from tkinter.filedialog import askopenfilename
from tkinter import StringVar
import sys

print("PyMusic Player组件 0.0.1 Beta")
top = tkinter.Tk()
top.geometry("800x400")
top.title("PyMusic Player")


def printsrceen(texts):
    t = int(texts)
    top.attributes("-alpha", t / 100)


screenwidth = top.winfo_screenwidth()
screenheight = top.winfo_screenheight() - 100

pygame.init()
path = StringVar()
paths = StringVar()
patht = StringVar()
v = StringVar()
v1 = StringVar()
file_dir = ".\Download"

def callback():
    path_ = askopenfilename()
    return path_


musicPath = os.path.abspath(os.path.dirname(__file__))


def selectPath():

    def file_name(file_dir):
        global files
        for root, dirs, files in os.walk(file_dir):
            # 当前路径下所有非目录子文件
            print(files)
        return files
    fil = file_name(file_dir)
    count = len(file_name(file_dir))

    s = random.randint(0, count - 1)
    fil2 = file_dir + "\\" + fil[s]
    pygame.mixer.music.load(fil2)
    pygame.mixer.music.play(1, 0)
    media_info = MediaInfo.parse(fil2)
    data = media_info.to_json()
    rst = re.search('other_duration.*?(.*?)min(.*?)s.*?', data)
    t = int(rst.group(0)[19:20])
    r = int(rst.group(0)[-4:-2])
    m = (t * 60 + r) * 1000

    musictime = str(t) + ':' + str(r)
    l2.config(text=fil2)
    l3.config(text=musictime)
    lbTime = tkinter.Label(top, anchor='w')
    lbTime.place(x=25, y=150)


def printScale(text):
    t = int(text)
    pygame.mixer.music.set_volume(t / 100)


def update_timeText():
    current = time.strftime("%H:%M:%S")

    timeText.configure(text=current)

    top.after(1000, update_timeText)


def remind():
    top = Toplevel()
    top.title('使用提示')
    top.geometry("200x200")
    t = "半分钟后开始播放音乐"
    msg = Message(top, text=t)
    msg.config(font=('times', 18, 'italic'))
    msg.place(x=0, y=0)
    lbTime = tkinter.Label(top, fg="red", anchor='w')
    lbTime.place(x=100, y=45)

    def autoclose():
        for i in range(30):
            lbTime['text'] = '距离窗口关闭还有{}秒'.format(30 - i)
            time.sleep(1)
        top.destroy()

    t = threading.Thread(target=autoclose)
    t.start()
    loopl = top.after(60 * 59500, remind)


def play():
    f = callback()
    pygame.mixer.music.load(f)
    pygame.mixer.music.play()
    path.set(f)
    media_info = MediaInfo.parse(f)
    data = media_info.to_json()
    rst = re.search('other_duration.*?(.*?)min(.*?)s.*?', data)
    t = int(rst.group(0)[19:20])
    r = int(rst.group(0)[-4:-2])
    m = (t * 60 + r) * 1000
    musictime = str(t) + ':' + str(r)
    l2.config(text=f)
    l3.config(text=musictime)
    lbTime = tkinter.Label(top, anchor='w')
    lbTime.place(x=25, y=150)

    def autoclose():
        for i in range(m // 1000):
            lbTime['text'] = '-{} /'.format((m // 1000) - i)
            time.sleep(1)

    t = threading.Thread(target=autoclose)
    t.start()
    loopl = top.after(m, selectPath)


def stop(loopl):
    pygame.mixer.music.stop()
    top.after_cancel(loopl)


def pause():
    pygame.mixer.music.pause()


def unpause():
    pygame.mixer.music.unpause()


def choosepic():
    path_s = askopenfilename()
    paths.set(path_s)
    img_open = Image.open(e1.get())
    img = ImageTk.PhotoImage(img_open)
    l1.config(image=img)
    l1.image = img


def loop():
    top.after(60 * 59500, remind)


def loops():
    selectPath()


def gettime():
    t = time.strftime('%H%M%S')
    s = int(t[0:2])
    d = int(t[2:4])
    f = int(t[4:6])
    g = s * 60 * 60 + d * 60 + f
    return g


def download():
    path = sys.path
    spath = path[5]
    mdPath = spath + '/pydosLinux/MusicDownload.py'
    os.system("python3 " + mdPath)


errmsg = 'Error!'
timeText = Label(top, text="", font=("Helvetica", 15))
timeText.place(x=180, y=370)
update_timeText()
Button(top, text="选择文件/播放", command=play, width=10, bg="sky blue").place(x=20, y=20)
Entry(top, text=path, width=25, state='readonly').place(x=120, y=20)

Button(top, text='选择图片', command=choosepic, width=10, bg="sky blue").place(x=20, y=55)
e1 = Entry(top, text=paths, state='readonly', width=25)
e1.place(x=120, y=55)
l1 = Label(top)
l1.place(x=320, y=0)

Button(top, text="随机播放", command=selectPath, width=7, bg="sky blue").place(x=20, y=225)
l2 = Label(top, text='', width=25, font=("Helvetica", 16))
l2.place(x=0, y=100)
Button(top, text="下一首", command=loops, width=5, bg="sky blue").place(x=100, y=225)
l3 = Label(top, text='', width=15)
l3.place(x=24, y=150)

Button(top, text="暂停", command=pause, width=7, bg="sky blue").place(x=170, y=245)
Button(top, text="继续播放", command=unpause, width=7, bg="sky blue").place(x=170, y=205)
Button(top, text="结束播放", command=stop, width=7, bg="sky blue").place(x=240, y=205)
Button(top, text="下载歌曲", command=download, width=7, bg="sky blue").place(x=240, y=245)

w1 = Scale(top, from_=0, to=100, orient="horizontal", length=75, variable=v, command=printScale, label="音量")
w1.place(x=240, y=145)

top.mainloop()
