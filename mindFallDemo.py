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

def updateClock(frameNum):
    if (not STARTBREAK):
        cv.itemconfig(end_break, width=0, height=0)
        # remove notification
        cv.itemconfig(notificationIt, text = '')
        cv.coords(imgIt, -300, -150)
        if (frameNum < len(starSky_videoStream)):
            t = time.time()
            current = time.strftime('%H:%M', time.localtime(t))
            # show notification at certain time
            # TODO: change the time (using seconds to demo for mow)
            if time.strftime('%S', time.localtime(t)) == '00':
                window.after(1, showNotification, 'Good \nMorning!', frameNum, 0)
                return
            elif time.strftime('%S', time.localtime(t)) == '20':
                window.after(1, showNotification, 'Time for \nLunch!', frameNum, 0)
                return
            elif time.strftime('%S', time.localtime(t)) == '40':
                window.after(1, showNotification, 'All set for \nthe day?', frameNum, 0)
                return
            # update clock
            cv.itemconfig(clockIt, text=current, font=("Arial", 40, "bold"))
            # reset clock position
            cv.coords(clockIt, 250, 350)
            cv.itemconfig(imgIt, image = starSky_videoStream[frameNum])

            window.after(100, updateClock, frameNum+1)
        else:
            # restart the video
            # TODO: add new video
            window.after(1, updateClock, 0)

def showNotification(message, frameNum, timeCnt):
    if (not STARTBREAK):
        if timeCnt > 30:
            # updateClock(frameNum)
            window.after(1, updateClock, frameNum)
            return
        if (frameNum < len(starSky_videoStream)):
            cv.itemconfig(imgIt, image = starSky_videoStream[frameNum])
            # show notification message
            cv.itemconfig(notificationIt, text = message)
            # update clock and change font and position
            t = time.time()
            current = time.strftime('%H:%M', time.localtime(t))
            cv.itemconfig(clockIt, text=current, font=("Arial", 15))
            cv.coords(clockIt, 100, 50)
            # end break btn
            cv.itemconfig(end_break, width=0, height=0)
            window.after(100, showNotification, message, frameNum+1, timeCnt+1)
        else:
            window.after(1, showNotification, message, 0, timeCnt)

# def startBreak(frameNum):
#     # remove notification
#     cv.itemconfig(notificationIt, text = '')
    
#     if (frameNum < len(break_Stream)):
#         cv.itemconfig(imgIt, image = break_Stream[frameNum])
#         # cv.move(imgIt, 400, 200)
#         # cv.create_window(10, 10, anchor ='nw', window = break_Stream[frameNum])
#         window.after(100, startBreak, frameNum+1)
#     else:
#         window.after(1, updateClock, 0)

def startBreak(frameNum):
    global STARTBREAK
    STARTBREAK = True
    # remove notification
    cv.itemconfig(notificationIt, text = '')
    
    if (frameNum < len(break_Stream)):
        # hide start break button
        cv.itemconfig(break_button, width=0, height=0)
        cv.itemconfig(imgIt, image = break_Stream[frameNum])
        cv.coords(imgIt, 0, 75)
        # cv.move(imgIt, 400, 200)
        # cv.create_window(10, 10, anchor ='nw', window = break_Stream[frameNum])
        # update clock and change font and position
        t = time.time()
        current = time.strftime('%H:%M', time.localtime(t))
        cv.itemconfig(clockIt, text=current)
        window.after(100, startBreak, frameNum+1)
    else:
        STARTBREAK = False
        cv.itemconfig(notificationIt, text = 'Break Over')
        
        

# create a tkinter window which we are going to place our pet
window = tk.Tk()
# get screen width and height
ws = window.winfo_screenwidth() # width of the screen
hs = window.winfo_screenheight() # height of the screen
pos = '+' + str(ws-550) + '+50'

# add video and store all its frames in an array
# make th-e video move by setting the image to different frames in the array
starSky_video_path = resource_path("starSky.mp4")
starSky_video = imageio.get_reader(starSky_video_path)
starSky_videoStream = []
for image in starSky_video.iter_data():
    frame_image = ImageTk.PhotoImage(image = Image.fromarray(image))
    starSky_videoStream.append(frame_image)

# break video
break_video = resource_path("flower.mp4")
bvid = imageio.get_reader(break_video)
break_Stream = []
for image in bvid.iter_data():
    fr_image = ImageTk.PhotoImage(image = Image.fromarray(image))
    break_Stream.append(fr_image)

# edit logo and title
# TODO: change icon
window.title('Mindfall')
window.iconbitmap(resource_path('mindfallLogo.ico'))

# keep the app on the top layer on desktop
window.wm_attributes("-topmost", True)
window.geometry('500x500' + pos)
window.resizable(width=False, height=False)
# canvas
bg_image = starSky_videoStream[0]
# initiate canvas
cv = tk.Canvas(width=500, height=500)
cv.pack(side='top', fill='both', expand='no')
# set background image
imgIt = cv.create_image(-300, -150, image=bg_image, anchor='nw')
# add clock text item to canvas
clockIt = cv.create_text(150, 20, text="", fill="#FBAC95", anchor='n')
# add notification item to canvas
notificationIt = cv.create_text(250, 250, text="", font=("Arial", 30, "bold"), fill="#FBAC95", anchor='n')

# create break button
break_button = tk.Button(window, text = 'Start Break!', bg = "#FBAC95", command = partial(startBreak,10), anchor = 'n')
break_window = cv.create_window(350, 10, anchor ='nw', window = break_button)
end_break = tk.Button(window, text = 'Return to Main', bg = "#FBAC95", command = partial(updateClock, 0), anchor = 'n')
endbreak_window = cv.create_window(350, 10, anchor ='nw', window = end_break)
# start the clock
# window.after(1, updateClock, 0)
updateClock(0)
window.mainloop()