#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 19:58:13 2020

@author: eal
"""

import os
import subprocess
import argparse

def tri(source_path, destination_path):
    
    list_fig = ['F'+str(n).zfill(2) for n in range(1,20)]
    for fig in list_fig:
        if(not os.path.exists(os.sep.join([destination_path,fig]))):
            print("creating "+os.sep.join([destination_path,fig]))
            os.makedirs(os.sep.join([destination_path,fig]))

    for (dirpath, dirnames, filenames) in os.walk(source_path):
        for directory in dirnames:
            #print("dir "+directory)
            for (dirpath2, dirnames2, filenames2) in os.walk(os.sep.join([dirpath,directory])):
                for filename in filenames2:
                    #print(filename)
                    for fig in list_fig:
                        if fig in filename: 
                            #print("moving to "+os.sep.join([destination_path,fig,filename]))
                            bashCommand = "mv {} {}".format(os.sep.join([source_path,directory,filename]), os.sep.join([destination_path,fig,filename]))
                            print(bashCommand)
                            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                            output, error = process.communicate()
                            #os.rename(os.sep.join([source_path, filename]), os.sep.join([destination_path,fig,filename]))

                
if __name__ == "__main__":
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--source", required=True, help="path to source folder")
    ap.add_argument("-d", "--destination", required=True, help="path to destination folder")
    args = vars(ap.parse_args())
    
    tri(args['source'],args['destination'])
    #print(list_fig)
    #tri('/run/media/eal/CORSAIR/Extraction_frames/Extraction_frames_angleB/outputB/output/frames_ratio_0.25_angleB', '/run/media/eal/CORSAIR/Extraction_frames/frames_triees')
