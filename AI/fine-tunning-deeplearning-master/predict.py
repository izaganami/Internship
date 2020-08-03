import tkinter as tk
from PIL import Image, ImageTk
from keras.models import load_model
from collections import deque
import numpy as np
import argparse
import pickle
import cv2
import matplotlib.pyplot as plt
import json

confR = "F01"
prob = "0%"
# Set up GUI
window = tk.Tk()  # Makes main window
window.wm_title("Digital Microscope")
window.config(background="#FFFFFF")
window.resizable(0, 0)
LABELS = ["F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08", "F09", "F10", "F11", "F12", "F13", "F14", "F15",
          "F16", "F17", "F18", "AS00", "AS01", "AS02", "AS03"]

pressed = False


def update(conf, button):
    print("butt 1 clicked")
    conf = button['text'][-4:]
    global confR
    confR = conf
    print(confR)


def update1(conf, button1):
    print("butt 2 clicked")
    conf = button1['text'][-4:]
    global confR
    confR = conf
    print(confR)


# Graphics window
imageFrame = tk.Frame(window, width=900, height=900)
imageFrame.grid(row=0, column=0, padx=10, pady=2)
imageFrame.pack()
button_text = tk.StringVar()
button = tk.Button(window, text=tk.StringVar(), width=25, command=lambda: update(confR, button))
button.pack(side=tk.LEFT)

button_text1 = tk.StringVar()
button1 = tk.Button(window, text=tk.StringVar(), width=25, command=lambda: update1(confR, button1))
button1.pack(side=tk.RIGHT)

v = tk.StringVar(window)
e = tk.Entry(window, textvariable=v, width=25)
e.pack()


def update2(conf,bool):
    print("Entry point clicked")
    conf = v.get().upper()
    if conf in LABELS:
        global confR, prob, pressed
        confR = conf
        prob = "99%"
        pressed = bool
        print(confR)

    else:
        v.set("Enter a valid configuration")


button2 = tk.Button(window, text='Submit', width=25, command=lambda: update2(confR,True))
button2.pack()

# Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True, help="path to trained serialized model")
ap.add_argument("-l", "--label-bin", required=True, help="path to  label binarizer")
ap.add_argument("-i", "--input", required=True, help="path to our input video")
ap.add_argument("-o", "--output", required=True, help="path to our output video")
ap.add_argument("-s", "--size", type=int, default=128, help="size of queue for averaging")
ap.add_argument("-p", "--proba", type=float, default=20.00, help="probabilty to write or not a configuration in the json file")
ap.add_argument("-c", "--path", type=str, default="result.json", help="path to output json")

args = vars(ap.parse_args())

A = [[0] for i in range(len(LABELS))]
print(A)
print("[INFO] loading model and label binarizer...")
model = load_model(args["model"], compile=False)
lb = pickle.loads(open(args["label_bin"], "rb").read())
mean = np.array([123.68, 116.779, 103.939][::1], dtype="float32")
Q = deque(maxlen=args["size"])

vs = cv2.VideoCapture(args["input"])
fps = vs.get(cv2.CAP_PROP_FPS)
count = 0


def convert_frame_to_time(count, fps):
    time = count / fps
    if time / 60 < 1:
        return "00:00:{:.2f}".format(time)
    elif time / 60 >= 1 and time / 60 < 60:
        minutes = int(time // 60)
        secondes = time / 60 - (time // 60)
        return "00:{}:{:.2f}".format(minutes, secondes)
    else:
        heures = int(time // 3600)
        minutes = int((time / 3600 - time // 3600) * 60)
        secondes = ((time / 3600 - time // 3600) * 60 - minutes) * 60
        return "{}:{}:{:.2f}".format(heures, minutes, secondes)


prev_config = ""

jsondict = {-1: {"start": "null", "end": "null", "label": "null", "prob": "null"},
            -2: {"start": "null0", "end": "null0", "label": "null0", "prob": "null0"}}
startjson = ""
endjson = ""
configjson = ""
framejson = 0
togglestart = True
toggleend = False


def toggle_start(start0, config0, frame0, prob0):
    global start, configjson, framejson, togglestart, toggleend, startjson, prob
    startjson = start0
    configjson = config0
    framejson = frame0
    prob = prob0
    togglestart = False
    toggleend = True


def toggle_end(end0):
    global endjson, json, togglestart, toggleend
    endjson = end0
    jsondict[framejson] = {
        "start": startjson, "end": endjson, "label": configjson, "prob": prob
    }
    toggleend = False
    togglestart = True


def show_frame():
    writer = None
    (W, H) = (None, None)
    _, frame = vs.read()
    if _:
        global count
        count += 1
        print("time stamp current frame: {}".format(convert_frame_to_time(count, fps)))
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
        global prob, pressed
        print("'''''''''''''''''{}''''''''''''''''''".format(pressed))

        global confR
        global prev_config
        if prev_config == "":
            print("cas1")
            confR = label
            prev_config = confR

        if label == prev_config:
            if label == confR:
                print("cas2")
                prev_config = confR
            else:
                print("cas3")
                prev_config = label
        if label != prev_config:
            if label == confR:
                print("cas4")
                prev_config = confR
            else:
                print("cas5")
                confR = label
                prev_config = confR
        global toggleend
        global togglestart
        global final_elem, before_final_elem
        [final_elem, before_final_elem] = sorted(jsondict.keys(), reverse=True)[0:2]
        final_elem = jsondict[final_elem]['label']
        before_final_elem = jsondict[before_final_elem]['label']
        print(final_elem + " " + before_final_elem)
        print(final_elem + " " + before_final_elem)
        if bool(jsondict) == True and final_elem != confR and final_elem != before_final_elem:
            print(togglestart)
            print(toggleend)
            if togglestart == True and toggleend == False:
                togglestart = False
                toggle_start(convert_frame_to_time(count, fps), confR, count,
                             "99%" if pressed is True else "{:.2f}%".format(round(results[i], 2) * 100))
                print(jsondict)
            elif toggleend == True and togglestart == False:
                toggle_end(convert_frame_to_time(count, fps))
                toggleend = False

        button_text.set("{}".format(label))
        button_text1.set("{}".format(label_j))

        text = "Config: {}".format(label)
        text_j = "Config: {}".format(label_j)
        button.config(text="{:.2f}% {}".format(round(results[i], 2) * 100, label))
        button1.config(text="{:.2f}% {}".format(round(results_j[j], 2) * 100, label_j))
        text_r = "Config: {}".format(confR)

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
        pressed=False


show_frame()  # Display 2
window.mainloop()  # Starts GUI
del jsondict[-1]
del jsondict[-2]
elem=[]
for elt,value in jsondict.items():
    if float(value['prob'][0:-1]) < args["proba"]:
        elem.append(elt)
for e in elem:
    del jsondict[e]
with open(args["path"], 'w', encoding='utf-8') as outfile:
    json.dump(jsondict, outfile, ensure_ascii=True)

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

# writer.release()
vs.release()
