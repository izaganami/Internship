#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#author: elie-alban.lescout@ensg.eu
#

import json
import datetime
import os
import argparse

def jsonToSrt(input_file, output_folder):
    with open(input_file, "r") as read_file:
        data = json.load(read_file)
    
    with open(os.path.join(output_folder,input_file.split('.')[0]+".srt"), "w") as write_file:
        i = 1
        for click in data['clicks']:
            action = click['click']
            time_start = str(datetime.timedelta(seconds=click['time']))
            time_end = str(datetime.timedelta(seconds=click['time']+2))
            #print("{}\n{},000 --> {},000\n{}\n".format(i, time_start, time_end, action))
            write_file.write("{}\n{},000 --> {},000\n{}\n\n".format(i, time_start, time_end, action))
            i += 1

def srtToJson(input_file, output_folder):
    data = {}
    count = 1
    with open(input_file, "r") as read_file:  
        lines = read_file.readlines()
        
        for i in range(0, len(lines)):
            line = lines[i]
            if '-->' in line:
                data[count] = {}
                line = line.replace(',','.')
                time = line.split(' --> ')
                
                start = time[0].split(':')
                start = [float(item) for item in start]
                end = time[1].split(':')
                end = [float(item) for item in end]
                
                time_start = str(start[0]*3600+start[1]*60+start[2])
                time_end = str(end[0]*3600+end[1]*60+end[2])
                #print(time_start,time_end,lines[i+1])
                data[count]['start'] = time_start
                data[count]['end'] = time_end
                data[count]['label'] = lines[i+1].strip('\n')
            
                count += 1
    #print('saving to '+os.path.join(output_folder,input_file.split('/')[-1].split('.')[0]+".json"))
    with open(os.path.join(output_folder,input_file.split('/')[-1].split('.')[0]+".json"), "w") as write_file:
        json.dump(data, write_file)
        
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="absolute path to input file (srt or json)")
    ap.add_argument("-o", "--output", required=True, help="absolute path to output folder")
    args = vars(ap.parse_args())
    
    if '.srt' in args['input']:
        srtToJson(args['input'],args['output'])
    elif '.json' in args['input']:
        jsonToSrt(args['input'],args['output'])
    else:
        print('Invalid file format.')