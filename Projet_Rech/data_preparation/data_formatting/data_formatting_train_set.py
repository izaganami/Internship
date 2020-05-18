# coding: utf-8
"""
DEPENDENCIES : ffmpeg, opencv, moviepy, matplotlib, pytest-shutil
"""


import json
import os
from os import listdir
from os.path import isfile, join, exists
import subprocess
from moviepy.video.io.VideoFileClip import VideoFileClip
import matplotlib.pyplot as plt
import time
#import data_augmentation
import numpy as np
import shutil
import cv2
import argparse
import skvideo.io



#A FAIRE : 
#vider les dossiers extract, frames etc.. automatiquement si besoin
#rendre l'algo moins dépendant du nom des données ?
#appliquer la data augmentation plusieurs fois pour avoir plus de mosaique
# ressortir les mosaiques non transformées en plus des transformées

#travailler avec des expressions régulière pour chopper l'identifiant ?
#ligne 152     if outputFolder != "" and "output" not in os.listdir(outputFolder):
#        os.makedirs(outputFolder + "output")
#    else:
#        os.makedirs("output") : attention si outputFolder est vide mais qu'il existe un dossier output, ça bug
# if eventType[0] == "A": attention, il faut le rendre dépendant de listre_labels
#pour les path d'entrée: ne fonctionnent pas si il ya des accents, espaces, même avec des guillemets autour. utiliser Path
#refaire fonctionner le get_and_save_frames


def get_duration_linux(file):
        clip = VideoFileClip(file)
        return(clip.duration)


def decoupe_multiple_vid():
    """
        On considere que les video sont dans le dossier videos et les json dans le dossier json
        les videos suivent la convention suivante : pXXXvariable
        les json suivent la convention suivante : CC-pXXXvariable
    """
    #on recupere tous les JSON
    onlyfiles = [f for f in listdir(jsonPath) if isfile(join(jsonPath, f))]
    #pour chaque JSON, on appelle decoupe
    for file in onlyfiles:
        print(file)
        decoupe_multiple_jeu_entrainement(jsonPath + file)
    
def decoupe_multiple(json_filename):
    """
        Prend en entrée le nom (ou le chemin ?) du fichier json et découpe en sous extraits vidéo la vidéo associée
    """
    with open(json_filename) as json_file:
        
        video_filename = "ERREUR, la video associe au json " + json_filename + " n'as pas ete trouvee, verifiez l'absence de majuscule"
        #on recupere le nom de toutes les videos du dossier video
        onlyvideos = [f for f in listdir(videoPath) if isfile(join(videoPath, f))]
        for video in onlyvideos:
            #on cherche la video dont le nom contient le même identifiant pXXX
            if json_filename.split("/")[-1][0:4] in video:
                video_filename = video
                break
        data = json.load(json_file)

        #On recupere la duree de la video
        duration = get_duration_linux(videoPath + video_filename)
        i = 0
        
        #pour chaque clic, on va decouper la video en sous extrait grâce a la fonction Ellie
        for p in data['clicks']:
            time = p["time"]
            eventType = p["click"]
            t_begin = max(int(time) - 2, 0)
            duration = min(4,abs(int(time)-duration))
            if eventType in liste_labels:
                trim_video(video_filename,t_begin,duration, str(i)+'_'+eventType)
            i += 1

def decoupe_multiple_jeu_entrainement(json_filename):
    """
        Prend en entrée le nom (ou le chemin ?) du fichier json et découpe en sous extraits vidéo la vidéo associée
    """
    with open(json_filename) as json_file:
        
        video_filename = "ERREUR, la video associe au json " + json_filename + " n'as pas ete trouvee, verifiez l'absence de majuscule"
        #on recupere le nom de toutes les videos du dossier video
        onlyvideos = [f for f in listdir(videoPath) if isfile(join(videoPath, f))]
        for video in onlyvideos:
            #on cherche la video dont le nom contient le même identifiant pXXX
            if json_filename.split("/")[-1].split(".")[-2] in video:
                video_filename = video
                break
        data = json.load(json_file)
        #pour chaque clic, on va decouper la video en sous extrait grâce a la fonction Ellie
        nonVide = True
        i = 1
        p = data["1"]
        while (nonVide):
            start = p["start"]
            end = p["end"]
            eventType = p["label"]
            if eventType in liste_labels:
                trim_video(video_filename,float(start),float(end)-float(start), str(i)+'_'+eventType)
            i += 1
            try:
                p = data[str(i)]
            except:
                nonVide = False



def trim_video(video_filename,time_begin,duration, event_id):
    """
        Découpe une vidéo suivant le time begin et duration donne
    
    #solution 1 : moyennement rapide --- 60.02729105949402 seconds ---
    ffmpeg_extract_subclip("videos/" + video_filename, time_begin, time_begin+duration, targetname="extract/"+video_filename[0:-4]+"_{}.mp4".format(event_id))
    
    """
    #solution 3 :

    bashCommand = "ffmpeg -ss {} -i \"{}\" -t {} -c copy \"{}extract/".format(time_begin, videoPath+video_filename, duration,outputFolder + "output/") +video_filename[0:-4]+"_{}.mp4\"".format(event_id)
    os.system(bashCommand)


def get_and_save_frames(video_filename):
    """
        récupère et enregistre les frames de la video donnee en entree
        Le nombre de frames en sortie peut etre parametree : https://ffmpeg.org/ffmpeg-filters.html#Examples-136

        NON FONCTIONNEL sous windows, preferer get_and_save_frames_cv2
    """
    os.makedirs(outputFolder + "output/" + "frames/frames_" + video_filename[0:-4])
    #cmd = 'ffmpeg -i \"{}\" -vf select="not(mod(n\,8))" -vsync vfr -vframes 6 \"{}frames/frames_{}/{}_frame-%02d.png\"'.format(outputFolder + "output/extract/"+video_filename,outputFolder,video_filename[0:-4],video_filename[0:-4])
    cmd = 'ffmpeg -i {} -vf select="not(mod(n\,8))" -vsync vfr -vframes 6  test/{}_frame-%02d.png'.format(outputFolder + "output/extract/"+video_filename,video_filename[0:-4])
    os.system(cmd)

def get_and_save_frames_cv2(video_filename):
    # Opens the Video file
    cap= cv2.VideoCapture(outputFolder + "output/extract/" + video_filename)
    i=0
    frames_captured = 0
    os.makedirs(outputFolder + "output/frames/frames_{}".format(video_filename[0:-4]))
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False or frames_captured == 6:
            break
        if i % 8 == 0:
            frames_captured += 1
            cv2.imwrite('{}frames/frames_{}/{}_frame-{}.png'.format(outputFolder + "output/",video_filename[0:-4],video_filename[0:-4],frames_captured),frame)
        i+=1
     
    cap.release()
    cv2.destroyAllWindows()

def get_and_save_frames_cv2_V3(video_filename, modulo_frames=8):
    # Opens the Video file
    cap= cv2.VideoCapture(outputFolder + "output/extract/" + video_filename)
    i=0
    frames_captured = 0
    os.makedirs(outputFolder + "output/frames/frames_{}".format(video_filename[0:-4]))
    while(cap.isOpened()):
        ret, frame = cap.read()
        #on limite volontairement le nombres de frames à 10 pour un évènement donné
        if ret == False or frames_captured == 150:
            break
        #if i % modulo_frames == 0:
         #   frames_captured += 1
        img = cv2.resize(frame, (224,224))
        print("Writing to : ", '{}frames/frames_{}/{}_frame-{}.png'.format(outputFolder + "output/",video_filename[0:-4],video_filename[0:-4],frames_captured))
        cv2.imwrite('{}frames/frames_{}/{}_frame-{}.png'.format(outputFolder + "output/",video_filename[0:-4],video_filename[0:-4],frames_captured),img)
        frames_captured += 1
        i+=1
     
    cap.release()
    cv2.destroyAllWindows()

def scikit(video_filename):
    # Opens the Video file
    cap= skvideo.io.vreader(outputFolder + "output/extract/" + video_filename)
    i=0
    frames_captured = 0
    os.makedirs(outputFolder + "output/frames/frames_{}".format(video_filename[0:-4]))
    for frame in cap:
            
        #on limite volontairement le nombres de frames à 150 pour un évènement donné
        if frames_captured == 150:
            break
        img = cv2.resize(frame, (224,224))

        #Log pour contrôle du bon déroulement
        if i == 0 :
                print("Writing to : ", '{}frames/frames_{}/{}_frame-{}.png'.format(outputFolder + "output/",video_filename[0:-4],video_filename[0:-4],frames_captured))

        cv2.imwrite('{}frames/frames_{}/{}_frame-{}.png'.format(outputFolder + "output/",video_filename[0:-4],video_filename[0:-4],frames_captured),img)
        frames_captured += 1
        i+=1
     
    cv2.destroyAllWindows()

def concatenate(dossier):
    """
        Prend en entree le dossier où sont contenues les images a concatener et renvoie une image concatenenee sans l'enregistrer
    """
    #on recupere les images du dossier

    onlyimgs = [f for f in listdir(dossier) if isfile(join(dossier, f))]
    imgs = [plt.imread(dossier + "/" + i) for i in onlyimgs]
    return np.concatenate(imgs)

def init_workplace():

    if outputFolder != "" and "output" not in os.listdir(outputFolder):
        os.makedirs(outputFolder + "output")
    elif "output" not in os.listdir():
        os.makedirs("output")
    else:
        shutil.rmtree("output")
        os.makedirs("output")


    if "frames_augmented" in os.listdir(outputFolder + "output/"):
        shutil.rmtree(os.path.join(outputFolder + "output/" + "frames_augmented"))
    os.makedirs(outputFolder + "output/frames_augmented")

    if "mosaiques" in os.listdir(outputFolder + "output/"):
        shutil.rmtree(os.path.join(outputFolder + "output/" + "mosaiques"))
    os.makedirs(outputFolder + "output/mosaiques")


def init_extract():
    if "extract" in os.listdir(outputFolder + "output/"):
        shutil.rmtree(os.path.join(outputFolder + "output/" + "extract"))
    os.makedirs(outputFolder + "output/extract")

def init_frames():
    if "frames" in os.listdir(outputFolder + "output"):
        shutil.rmtree(os.path.join(outputFolder + "output/" + "frames"))
    os.makedirs(outputFolder + "output/frames")
     
    
if __name__ == "__main__":
    
    """
        MODE D'EMPLOI : 
    """
    start_time = time.time()

    liste_labels = ["F01","F02","F03","F04","F05","F06","F07","F08","F09","F10","F11","F12","F13","F14","F15","F16","F17","F18","F19","F20"]
    """
    videoPath = "test_22.01.2020/vid/"
    jsonPath = "test_22.01.2020/json_22.01.2020/"
    outputFolder = "test_22.01.2020/output/"

    """
    videoPath = "videos"
    jsonPath = "json"
    outputFolder = ""

    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video-path", required=False, help="path to videos, if NONE, default is videos. No special character, no whitespace nor quotes")
    ap.add_argument("-j", "--json-path", required=False, help="path to jsons, if NONE, default is json. No special character, no whitespace nor quotes")
    ap.add_argument("-o", "--output", required=True, help="relative path to our output folder, if NONE, default is current workplace folder. No special character, no whitespace nor quotes")
    args = vars(ap.parse_args())

    if args["video_path"] != None :
        videoPath = args["video_path"].replace("\\","/")
    if args["json_path"] != None :
        jsonPath = args["json_path"].replace("\\","/")
    if args["output"] != None :
        outputFolder = args["output"].replace("\\","/")

    if videoPath != "":
        videoPath += "/"
    if jsonPath != "":
        jsonPath += "/"
    if outputFolder != "":
        outputFolder += "/"
        
    if outputFolder != "" and not exists(outputFolder):
        os.makedirs(outputFolder)
    


    print("préparation de la sortie")
    init_workplace()
    print("Fin de la préparation")
    r_decoup_vid = input("Voulez vous redécouper les vidéos ? (y/n) : ")
    r_extract_frames = input("Voulez vous ré-extraire les frames ? (y/n) : ")
    
    if r_decoup_vid == "y":
        init_extract()
        print("Début découpage de vidéo")
        decoupe_multiple_vid()
        print("Fin découpage de vidéo")
    else:
        if "extract" not in [f for f in listdir(outputFolder + "output/")]:
            print("Le chemin de sortie a changé, le redécoupage des videos est nécessaire")
            init_extract()
            print("Début découpage de vidéo")
            decoupe_multiple_vid()
            print("Fin découpage de vidéo")

        

    if r_extract_frames == "y":
        init_frames()
        print("Début récupération des frames")
        onlyfiles = [f for f in listdir(outputFolder + "output/" + "extract") if isfile(join(outputFolder + "output/" + "extract", f))]
        for f in onlyfiles:
            print("F : " + f)
            scikit(f)
        print("Fin récupération des frames")
    else:
        if "frames" not in [f for f in listdir(outputFolder + "output/")]:
                print("Le chemin de sortie a changé, la réextration des frames est nécessaire")
                init_frames()
                print("Début récupération des frames")
                onlyfiles = [f for f in listdir(outputFolder + "output/" + "extract") if isfile(join(outputFolder + "output/" + "extract", f))]
                for f in onlyfiles:
                    print("F : " + f)
                    scikit(f)
                print("Fin récupération des frames")

        
    onlydossiers = [d for d in listdir(outputFolder + "output/" + "frames") if not isfile(join(outputFolder + "output/" + "frames", d))]
    """
    if (input("Voulez vous faire la data augmentation et les mosaiques ? (y/n) : \n") == "y"):
        print("Début data_augmentation et mosaique")
    
        for i in liste_labels:
            os.makedirs(outputFolder + "output/" + "mosaiques/"+i)
        for d in onlydossiers:
                    
            os.makedirs(outputFolder + "output/" + "frames_augmented/" + d)
            onlyfiles = [plt.imread(outputFolder + "output/" + "frames/"+ d + "/" + f[0:-4] + ".png") for f in listdir(outputFolder + "output/" + "frames/"+d) if isfile(join(outputFolder + "output/" + "frames/" + d, f))]
            
            
            
            data_augmentation.data_augmentation(np.array(onlyfiles),outputFolder, d)
            print("CHECKPOINT : " + d)
            for i in liste_labels:
                if ("_"+i) in d:
                    plt.imsave(outputFolder + "output/" +"mosaiques/"+i+"/mosaique_{}.png".format(d),concatenate(outputFolder + "output/" + "frames_augmented/"+d))
        
        print("Fin data_augmentation et mosaique")
    
    """
    print("--- %s seconds ---" % (time.time() - start_time))

    
    
    
