import matplotlib
from keras.engine.saving import load_model

matplotlib.use("Agg")
from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.pooling import AveragePooling2D
from keras.applications import ResNet50
from keras.layers.core import Dropout
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras.layers import Input
from keras.models import Model
from keras.optimizers import SGD
from keras.callbacks import ModelCheckpoint
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import pickle
import cv2
import os
from sklearn.metrics import f1_score


checkpoint = ModelCheckpoint("best_model.pickle", monitor='loss', verbose=1,
    save_best_only=True, mode='auto', period=1)

##variable for command line
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="path to input dataset")
ap.add_argument("-m", "--model", required=True, help="path to output serialized model")
ap.add_argument("-l", "--label-bin", required=True, help="path to output label binarizer")
ap.add_argument("-e", "--epochs", type=int, default=25, help="# of epochs to train our network for")
ap.add_argument("-p", "--plot", type=str, default="plot.png", help="path to output loss/accuracy plot")
ap.add_argument("-r", "--ReloadModel", required=True, help="path to unfinished model")

args = vars(ap.parse_args())

##LABELS = set(["F01", "F02", "F03", "F04", "F07", "F11","F12","F13"])
LABELS = set(["F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08","F09", "F10", "F11","F12","F13","F14","F15","F16","F17", "F18","AS00","AS01","AS02","AS03"])

##LABELS = set(["F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08", "F09", "F10", "F11","F12","F13", "FXX"])
print("[INFO] loading images...")
imagePaths = list(paths.list_images(args["dataset"]))
data = []
labels = []
for imagePath in imagePaths:
    label = imagePath.split(os.path.sep)[-2]
    if label not in LABELS:
        continue
    image = cv2.imread(imagePath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    data.append(image)
    labels.append(label)
data = np.array(data)
labels = np.array(labels)
lb = LabelBinarizer()
labels = lb.fit_transform(labels)
(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.30, stratify=labels, random_state=42)
##print("labels",labels)
print(testY)
trainAug = ImageDataGenerator(rotation_range=0, zoom_range=0.05, width_shift_range=0.02, height_shift_range=0.02, shear_range=0.005, horizontal_flip=True, fill_mode="nearest")
valAug = ImageDataGenerator()
mean = np.array([123.68, 116.779, 103.939], dtype="float32")
trainAug.mean = mean
valAug.mean = mean

model = load_model(args["ReloadModel"],compile=False)


print("[INFO] compiling model...")
opt = SGD(lr=1e-4, momentum=0.9, decay=1e-4 / args["epochs"])
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

print("[INFO] training ...")
H = model.fit_generator(trainAug.flow(trainX, trainY, batch_size=50),steps_per_epoch=len(trainX) // 32,validation_data=valAug.flow(testX, testY),validation_steps=len(testX) // 32, epochs=args["epochs"],callbacks=[checkpoint])
print("[INFO] evaluating network...")
predictions = model.predict(testX, batch_size=32)

print(classification_report(testY.argmax(axis=1), predictions.argmax(axis=1), target_names=lb.classes_))
N = args["epochs"]
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), H.history["accuracy"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy on Dataset")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig(args["plot"])
print("[INFO] serializing network...")
model.save(args["model"])
f = open(args["label_bin"], "wb")
f.write(pickle.dumps(lb))
f.close()
