import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkFont
import pyautogui # py -m pip install pyautogui
import sys
import os
import time
import imageio # pip install imageio; pip install imageio-ffmpeg
from functools import partial

STARTBREAK = False

# Get absolute path to resource, works for dev and for PyInstaller
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.getcwd())
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# create a tkinter window which we are going to place our pet
window = tk.Tk()
# get screen width and height
ws = window.winfo_screenwidth() # width of the screen
hs = window.winfo_screenheight() # height of the screen
pos = '+' + str(ws-550) + '+50'

# add video and store all its frames in an array
# make th-e video move by setting the image to different frames in the array
def getFrameArr(path):
    print(path)
    video_path = resource_path(path)
    video = imageio.get_reader(video_path)
    videoStream = []
    for image in video.iter_data():
        frame_image = ImageTk.PhotoImage(image = Image.fromarray(image))
        videoStream.append(frame_image)
    print("done")
    return videoStream

break_Stream = getFrameArr("flower.mp4")
starSky_videoStream = getFrameArr("starSky.mp4")
# cloud_videoStream = getFrameArr("cloud.mp4")
nyc_videoStream = getFrameArr("nyc.mp4")
mountains_videoStream = getFrameArr("mountains.mp4")
sunrise_videoStream = getFrameArr("sunrise.mp4")

videoStreamGlob = sunrise_videoStream
print("set sunrise")

def configView():
    global videoStreamGlob
    if videoStreamGlob == sunrise_videoStream:
        cv.coords(imgIt, -300, 0)
        cv.itemconfig(clockIt, fill="#FBAC95")
        cv.itemconfig(notificationIt, fill="#FBAC95")
        break_button.configure(bg="#FBAC95")
    elif videoStreamGlob == nyc_videoStream:
        cv.coords(imgIt, -300, -50)
        cv.itemconfig(clockIt, fill="#FFFFFF")
        cv.itemconfig(notificationIt, fill="#FFFFFF")
        break_button.configure(bg="#FFFFFF")
    elif videoStreamGlob == mountains_videoStream:
        cv.coords(imgIt, -300, -50)
        cv.itemconfig(clockIt, fill="#D9D9D9")
        cv.itemconfig(notificationIt, fill="#D9D9D9")
        break_button.configure(bg="#D9D9D9")
    elif videoStreamGlob == starSky_videoStream:
        cv.coords(imgIt, -300, -150)
        cv.itemconfig(clockIt, fill="#A2A2A2")
        cv.itemconfig(notificationIt, fill="#A2A2A2")
        break_button.configure(bg="#D9D9D9")

def updateClock(frameNum):
    # the time intervals set to be small are for demo purpose
    if (not STARTBREAK):
        t = time.time()
        current = time.strftime('%H:%M', time.localtime(t))
        global videoStreamGlob
        configView()
        minute = int(time.strftime('%M', time.localtime(t))) % 5
        second = time.strftime('%S', time.localtime(t))
        if minute == 0 and second == "00":
            videoStreamGlob = sunrise_videoStream
            frameNum = 0
        elif minute == 2 and second == "00":
            videoStreamGlob = nyc_videoStream
            frameNum = 0
        elif minute == 3 and second == "00":
            videoStreamGlob = mountains_videoStream
            frameNum = 0
        elif minute == 4 and second == "00":
            videoStreamGlob = starSky_videoStream
            frameNum = 0
        # remove notification
        cv.itemconfig(notificationIt, text = '')
        cv.itemconfig(break_message, text = '')
        break_button.configure(text='Start Break!', command=partial(callStartBreak,10,bgVideo=videoStreamGlob))
        if (frameNum < len(videoStreamGlob)):
            # show notification at certain time 
            if second == "00":
                window.after(1, showNotification, 'Good \nMorning!', frameNum, 0)
                return
            elif second == "20":
                window.after(1, showNotification, 'Time for \nLunch!', frameNum, 0)
                return
            elif second == "40":
                window.after(1, showNotification, 'All set for \nthe day?', frameNum, 0)
                return
            # update clock
            cv.itemconfig(clockIt, text=current, font=("Arial", 40, "bold"))
            # reset clock position
            cv.coords(clockIt, 250, 300)
            cv.itemconfig(imgIt, image = videoStreamGlob[frameNum])
            window.after(10, updateClock, frameNum+1)
        else:
            # restart the video
            window.after(1, updateClock, 0)

def showNotification(message, frameNum, timeCnt):
    if (not STARTBREAK):
        configView()
        if timeCnt > 300:
            # updateClock(frameNum)
            window.after(1, updateClock, frameNum)
            return
        if (frameNum < len(videoStreamGlob)):
            cv.itemconfig(imgIt, image = videoStreamGlob[frameNum])
            # show notification message
            cv.itemconfig(notificationIt, text = message)
            # update clock and change font and position
            t = time.time()
            current = time.strftime('%H:%M', time.localtime(t))
            cv.itemconfig(clockIt, text=current, font=("Arial", 15))
            cv.coords(clockIt, 100, 65)
            window.after(10, showNotification, message, frameNum+1, timeCnt+1)
        else:
            window.after(1, showNotification, message, 0, timeCnt)

def endBreak(frameNum, bgVideo):
    global STARTBREAK
    global videoStreamGlob
    STARTBREAK = False
    videoStreamGlob = bgVideo
    updateClock(frameNum)

def callStartBreak(frameNum, bgVideo):
    global STARTBREAK
    global videoStreamGlob
    STARTBREAK = True
    videoStreamGlob = break_Stream
    startBreak(frameNum, bgVideo)

def startBreak(frameNum, bgVideo):
    global STARTBREAK
    # remove notification
    cv.itemconfig(notificationIt, text = '')
    if STARTBREAK:
        if (frameNum < len(videoStreamGlob)):
            cv.itemconfig(imgIt, image = videoStreamGlob[frameNum])
            cv.coords(imgIt, 0, 75)
            # update clock and change font and position
            t = time.time()
            current = time.strftime('%H:%M', time.localtime(t))
            cv.itemconfig(clockIt, text=current, font=("Arial", 40, "bold"))
            # reset clock position
            cv.coords(clockIt, 250, 300)
            window.after(100, startBreak, frameNum+1, bgVideo)
            # can't end break before the video ends because STARTBREAK not set to false
            break_button.configure(text='End Break', command=partial(endBreak,0,bgVideo=bgVideo))
        else:
            STARTBREAK = False
            cv.itemconfig(break_message, text = 'How was \nyour break?')

# edit logo and title
# TODO: change icon
window.title('Mindfall')
window.iconbitmap(resource_path('mindfallLogo.ico'))

# keep the app on the top layer on desktop
window.wm_attributes("-topmost", True)
window.geometry('500x500' + pos)
window.resizable(width=False, height=False)
# canvas
bg_image = videoStreamGlob[0]
# initiate canvas
cv = tk.Canvas(width=500, height=500)
cv.pack(side='top', fill='both', expand='no')
# set background image
imgIt = cv.create_image(-300, -150, image=bg_image, anchor='nw')
# add clock text item to canvas
clockIt = cv.create_text(150, 20, text="", fill="#FBAC95", anchor='n')
# add notification item to canvas
notificationIt = cv.create_text(250, 250, text="", font=("Arial", 30, "bold"), fill="#FBAC95", anchor='n')
break_message = cv.create_text(250, 150, text = '', font =("Arial", 20, "bold"), fill="#FBAC95", anchor='n')
# create break button
break_button = tk.Button(window, text='Start Break!', bg="#FBAC95", fg="black", command=partial(callStartBreak,10,bgVideo=videoStreamGlob), anchor='n')
break_window = cv.create_window(350, 10, anchor='nw', window=break_button)

# start the clock
updateClock(0)
window.mainloop()