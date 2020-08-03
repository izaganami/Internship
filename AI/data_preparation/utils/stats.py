#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: EAL
"""

import json
import os
import subprocess
import numpy as np
import random
import datetime
from collections import Counter
from collections import OrderedDict

def count_configs(json_path, config):
    """
    Gives some information for the given configuration over all the data
    
    :type json_path: str
    :param config: a configuration is for instance 'FO3'
    :type config: str
    :rtype: list( int, int, list(int))
    :return: [number of config, mean appearance, [appearance in each video]] 
    """
    total_count = 0
    labels = []
    videos_count ={}
    mean = []
    for filename in os.listdir(json_path):
            count_unit = 0
            with open(json_path+filename) as json_file:
                    data = json.load(json_file)
                    clicks = data["clicks"]
                    idParticipant = data["idParticipant"]
                    if clicks:
                        for click in clicks:
                            if config in click["click"][:len(config)]:
                                labels.append(click["click"])
                                total_count += 1
                                count_unit += 1
                        videos_count[idParticipant] = count_unit
                        mean.append(count_unit)
    labels_count = Counter(labels)
    print('Nombre de '+str(config)+':',str(total_count))
    print('Nombre moyen de '+str(config)+' par vidéo:',str(np.mean(mean)))
    print('Fréquence de chaque label:',OrderedDict(sorted(labels_count.items())))
    print('Nombre de label par vidéo:',OrderedDict(sorted(labels_count.items())))
    
    return [total_count, np.mean(mean), videos_count, labels_count]

def create_sample_infos(config, size, json_path, video_path):
    """
    creates informations for sample : time for each click and its label in each video
    This will be used to manually point out the time interval it corresponds to
    """
    video_number = len(os.listdir(video_path))
    nb_sample_per_video = int(size/video_number)
    rest = size - nb_sample_per_video*video_number
    print(video_number,nb_sample_per_video)
    
    with open('samples.info', 'w') as write_file: #wrting infos in a file
        for filename in os.listdir(json_path): #going over all json file
            with open(json_path+filename) as json_file: 
                data = json.load(json_file)
                idParticipant = data["idParticipant"]
                clicks = data["clicks"]
                write_file.write(idParticipant+':\n')
                for i in range(nb_sample_per_video):
                    clicks = [item for item in clicks if config in item["click"][len(config)-1]]
                    rand_click = random.choice(clicks)
                    write_file.write('time:'+str(datetime.timedelta(seconds=int(rand_click['time'])))+',label:'+rand_click['click']+'\n')
                write_file.write('\n')



if __name__ == "__main__":
    json_path = "data_2019.12.03/json/"
    video_path = "data_2019.12.03/videos/"
    #create_sample_infos('F', 35, json_path, video_path)
    
#    for i in range(10):
#        print('F0'+str(i)+':',count_configs(json_path, 'F'+str(i))[0])
#    for i in [10,11,12,13]:
#        print('F'+str(i)+':',count_configs(json_path, 'F'+str(i))[0])
    results = count_configs(json_path, 'F')
    import matplotlib.pyplot as plt
    
    la = [item[0] for item in results[3].items()]
    count = [item[1] for item in results[3].items()]
    print(count)
    plt.hist(count, la)
    
    #print(results)

