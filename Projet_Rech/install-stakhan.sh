https://github.com/Stakhan/Projet_Recherche

### Git Install

mkdir -p /local/data/line/Projet_ENSG/Training_data

cd /local/data/line/Projet_ENSG/

git clone git@github.com:Stakhan/Projet_Recherche.git

mv Projet_Recherche Projet_Recherche_ENSG

### Dependencies install

 with python3.7 and pip3 already installed

su

#### CNN_model_fine_tuning

dnf install python3-virtualenv.noarch

dnf install python3-opencv.x86_64

pip3 install tensorflow==1.15

pip3 install keras

pip3 install imutils

pip3 install sklearn

pip3 install scikit-video

#### data_preparation

dnf install ffmpeg opencv.x86_64

dnf install python3-matplotlib.x86_64

pip3 install moviepy

pip3 install matplotlib

dnf install python3-pytest-shutil.noarch

#### subtitles utility

dnf install aegisub.x86_64

### Some tests

cd /local/data/line/Projet_ENSG/Projet_Recherche_ENSG/CNN_model_fine_tuning

python3 predict.py --help

python3 predict.py -m output/activity.model -l output/lb.pickle -i /local/data/line/Projet_ENSG/Training_data/example_clips/p207lise.mp4 -o /local/data/line/Projet_ENSG/Training_data/result/example_clips_p207lise_result.mp4

