import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import argparse
import pickle
import cv2
import matplotlib.pyplot as plt


ap = argparse.ArgumentParser()

ap.add_argument("-i", "--input", required=True, help="path to our input video")
ap.add_argument("-s", "--size", type=int, default=128, help="size of queue for averaging")
args = vars(ap.parse_args())

#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("Digital Microscope")
window.config(background="#FFFFFF")

#Graphics window
imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

#Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)
cap =  cv2.VideoCapture(args["input"])
def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)






show_frame()  #Display 2
window.mainloop()  #Starts GUI



