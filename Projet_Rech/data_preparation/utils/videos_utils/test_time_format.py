#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s
"""

import json
import os
import subprocess
import numpy as np
import random
import datetime

def get_duration(file): 
    """ 
        prend en entrée le nom du fichier (ou son chemin ?) et renvoie la durée 
    """ 
    #Get the duration of a video using ffprobe. 
    cmd = 'ffprobe -show_entries format=duration -v quiet -of csv="p=0" -i {}'.format(file) 
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True) 
    out = p.communicate()[0].decode('utf-8')
    print(out)
    return(float(out))
    
def get_framecount(file): 
    """ 
        prend en entrée le nom du fichier (ou son chemin ?) et renvoie son nombre de frame
    """ 
    #Get the duration of a video using ffprobe. 
    cmd = 'ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 {}'.format(file) 
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True) 
    out = p.communicate()[0].decode('utf-8') 
    
    return(int(out))

def test(json_path, video_path):
    list_videofiles = os.listdir(video_path)
    
    for filename in os.listdir(json_path): #going over all json file
        with open(json_path+filename) as json_file:
            problem = False
            data = json.load(json_file)
            idParticipant = data["idParticipant"]
            video_filename = [file for file in list_videofiles if idParticipant in file][0]
            clicks = data["clicks"]
            t_seconde = get_duration(video_path+video_filename)
            t_frame = get_framecount(video_path+video_filename)
            print(t_seconde, t_frame)
            for click in clicks:
                if click['time'] < t_seconde or click['time'] < t_frame:
                    continue
                else:
                    problem = True
            if problem:
                print(video_filename)
            

if __name__ == "__main__":
    
    json_path = "sorted_json/single/"
    video_path = "videos/single/"

    test(json_path, video_path)

