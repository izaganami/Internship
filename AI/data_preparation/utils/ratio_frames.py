

#On considère que le script est dans le même dossier que le dossier frames

import random
import os
from os import listdir
from os.path import isfile
import matplotlib.pyplot as plt
from shutil import copyfile

ratio = 0.25
framesfolder = [f for f in listdir("frames") if not isfile(f)]
os.makedirs("frames_ratio_{}".format(ratio))
print(framesfolder)
compteur = 0
for d in framesfolder:
    print(compteur)
    compteur +=1
    os.makedirs("frames_ratio_{}/{}".format(ratio,d))
    framelist = [f for f in listdir("frames/{}".format(d))]
    size = len(framelist)
    already_picked = []
    number_to_be_picked = int(ratio*size)
    for i in range(number_to_be_picked):
        r = random.randint(0,size-1)
        if r not in already_picked:
            already_picked.append(r)
            img_name = framelist[r]
            copyfile("frames/{}/{}".format(d,img_name),"frames_ratio_{}/{}/{}".format(ratio,d,img_name))
