#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 11:43:41 2019

@author: EAL
"""
import json
import os
import subprocess
import numpy as np

def fetch_video(id):
    """
    Not usefull anymore
    """
    bashCommand = "curl -L -O -C - {}".format('https://drive.google.com/uc?export=download&confirm=uGRA&id='+id)
    print(bashCommand)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

def extract_video_ids(json_path):
    """
        Extracts google drive ids from JSON file
    """
    with open('list2.id', 'w') as write_file:
        
        for filename in os.listdir(json_path):
            
            with open(json_path+filename) as json_file:
                    data = json.load(json_file)
                    videoId = data["videoUrl"]
                    if data["clicks"]:
                        write_file.write(videoId+'\n')
            
def create_bash_download_file(list_id):
    """
        Generates a bash file that automatically download all video files using curl. Requires a list of video id (google drive id)
    """
    read_file = open(list_id, 'r')
    with open('download_videos.sh', 'a') as write_file:             
        write_file.write('#!/bin/bash\n')
        #write_file.write('echo -e "########## DOWNLOADING '+read_file.readlines()[0]+' ########\n"\n')
        for line in read_file:
            bashCommand = "curl -L -O -C - {}".format('https://drive.google.com/uc?export=download&confirm=uGRA&id='+line.rstrip('\n')+'\n')
            write_file.write(bashCommand)

def count_FXX_configs(json_path):
    count = 0
    mean = []
    for filename in os.listdir(json_path):
            count_unit = 0
            with open(json_path+filename) as json_file:
                    data = json.load(json_file)
                    clicks = data["clicks"]
                    if clicks:
                        for click in clicks:
                            if "F" in click["click"]:
                                count += 1
                                count_unit += 1
                        mean.append(count_unit)
                    
    return [count, np.mean(mean), mean]


if __name__ == "__main__":
    results = count_FXX_configs('all_json/')
    print(results[2])
