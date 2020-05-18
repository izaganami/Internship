

#On considere que le script est dans le meme dossier que le dossier output

import random
import os
from os import listdir
from os.path import isfile
from shutil import copyfile
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="path working folder")
ap.add_argument("-mf", "--maxframe", type=int, default=15, help="maximum number of frames to keep for each event (default is 15). This is to make sure the training data stays homogenous")
args = vars(ap.parse_args())

path = args['path']

max_frames_per_event = args['maxframe']
#ratio = 0.25
framesfolder = [f for f in listdir(path + "frames") if not isfile(f)]
os.makedirs(path+"frames_max_{}".format(max_frames_per_event))
#print(framesfolder)
n = len(framesfolder)
compteur = 0
for d in framesfolder:
    print(str(compteur) + "/" + str(n))
    compteur +=1
    os.makedirs(path + "frames_max_{}/{}".format(max_frames_per_event,d))
    framelist = [f for f in listdir(path + "frames/{}".format(d))]
    size = len(framelist)
    already_picked = []
    number_to_be_picked = min(max_frames_per_event,size)
    #print(number_to_be_picked)
    if number_to_be_picked == size:
        for f in framelist:
            copyfile(path + "frames/{}/{}".format(d,f),path+"frames_max_{}/{}/{}".format(max_frames_per_event,d,f))
    else:
        for i in range(number_to_be_picked):
            r = random.randint(0,size-1)
            if r not in already_picked:
                already_picked.append(r)
                img_name = framelist[r]
                copyfile(path + "frames/{}/{}".format(d,img_name),path+"frames_max_{}/{}/{}".format(max_frames_per_event,d,img_name))
