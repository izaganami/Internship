import tkinter as tk
from PIL import Image, ImageTk
from keras.models import load_model
from collections import deque
import numpy as np
import argparse
import pickle
import cv2
import matplotlib.pyplot as plt

confR="F01"
# Set up GUI
window = tk.Tk()  # Makes main window
window.wm_title("Digital Microscope")
window.config(background="#FFFFFF")
window.resizable(0,0)





def update(conf,button):
    print("butt 1 clicked")
    conf=button['text'][-4:]
    global confR
    confR=conf
    print(confR)

def update1(conf,button1):
    print("butt 2 clicked")
    conf = button1['text'][-4:]
    global confR
    confR=conf
    print(confR)

# Graphics window
imageFrame = tk.Frame(window, width=900, height=900)
imageFrame.grid(row=0, column=0, padx=10, pady=2)
imageFrame.pack()
button_text = tk.StringVar()
button = tk.Button(window, text=tk.StringVar(), width=25, command=lambda: update(confR,button))
button.pack(side=tk.LEFT)

button_text1 = tk.StringVar()
button1 = tk.Button(window, text=tk.StringVar(), width=25, command=lambda: update1(confR,button1))
button1.pack(side=tk.RIGHT)



# Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True, help="path to trained serialized model")
ap.add_argument("-l", "--label-bin", required=True, help="path to  label binarizer")
ap.add_argument("-i", "--input", required=True, help="path to our input video")
ap.add_argument("-o", "--output", required=True, help="path to our output video")
ap.add_argument("-s", "--size", type=int, default=128, help="size of queue for averaging")
args = vars(ap.parse_args())

LABELS = ["F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08", "F09", "F10", "F11", "F12", "F13", "F14", "F15",
          "F16", "F17", "F18", "AS00", "AS01", "AS02", "AS03"]
A = [[0] for i in range(len(LABELS))]
print(A);
print("[INFO] loading model and label binarizer...")
model = load_model(args["model"], compile=False)
lb = pickle.loads(open(args["label_bin"], "rb").read())
mean = np.array([123.68, 116.779, 103.939][::1], dtype="float32")
Q = deque(maxlen=args["size"])

vs = cv2.VideoCapture(args["input"])

prev_config=""
def show_frame():
    writer = None
    (W, H) = (None, None)
    _, frame = vs.read()
    frame0 = frame
    if W is None or H is None:
        (H, W) = frame.shape[:2]
    output = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (224, 224)).astype("float32")
    frame -= mean
    preds = model.predict(np.expand_dims(frame, axis=0))[0]
    Q.append(preds)

    ##show predictions
    for i in range(len(preds)):
        A[i].append(preds[i])

    results = np.array(Q).mean(axis=0)
    i = np.argmax(results)
    results_j = np.delete(results, i)
    j = np.argmax(results_j)
    label_j = lb.classes_[j]
    label = lb.classes_[i]
    global confR
    global prev_config
    if prev_config=="":
        print("cas1")
        confR=label
        prev_config=confR

    if label==prev_config:
        if label==confR:
            print("cas2")
            prev_config=confR
        else:
            print("cas3")
            prev_config = label
    if label != prev_config:
        if label==confR:
            print("cas4")
            prev_config=confR
        else:
            print("cas5")
            confR=label
            prev_config = confR






    button_text.set("{}".format(label))
    button_text1.set("{}".format(label_j))

    text = "Config: {}".format(label)
    text_j = "Config: {}".format(label_j)
    button.config(text="{:.2f}% {}".format(round(results[i],2)*100,label))
    button1.config(text="{:.2f}% {}".format(round(results_j[j],2)*100,label_j))
    text_r ="Config: {}".format( confR)


    print("text_i:{}".format(text))
    print("text_j:{}".format(text_j))
    cv2.putText(output, text_r, (35, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1.25, (0, 255, 0), 5)
    if writer is None:
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(args["output"], fourcc, 30, (W, H), True)
    writer.write(output)
    print("Here")

    cv2image = cv2.cvtColor(output, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)




show_frame()  # Display 2
window.mainloop()  # Starts GUI

print("[INFO] cleaning up...")
j = 0
for k in range(len(A[0]) // 100):
    plt.style.use("ggplot")
    plt.figure()

    for i in range(len(A)):
        plt.plot(np.arange(100 * k, (100 * k) + 100), A[i][100 * k:(100 * k) + 100], label=LABELS[i])

    plt.title("Probs for each configuration")
    plt.xlabel("frame de: " + str(100 * k) + " a: " + str((100 * k) + 100))
    plt.ylabel("prob")
    plt.legend(loc="lower left")
    plt.savefig("plot" + str(k) + ".png")
    j = k

plt.style.use("ggplot")
plt.figure()
for i in range(len(A)):
    plt.plot(np.arange(100 * j, len(A[i])), A[i][100 * k:len(A[i])], label=LABELS[i])
plt.title("Probs for each configuration")
plt.xlabel("frame de: " + str(100 * j) + " jusqu a la fin")
plt.ylabel("prob")
plt.legend(loc="lower left")
plt.savefig("plot" + str(j) + ".png")

#writer.release()
vs.release()