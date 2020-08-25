

### Git and python Install

https://github.com/izaganami/Internship
```
$ sudo apt-get install git
```
Si python est deja installé il faut verifiier que c'est la version 3.6 : 
```
python3 --version
```
Sinon:
```
 $ sudo apt-get install python3.6
```
```
 $ sudo apt-get install python3-pip
```
```
mkdir -p /local/data/line/CubicScout
```
```
cd /local/data/line/CubicScout
```
```
git clone https://github.com/izaganami/Internship.git
```
```
mv Internship CubicScout
```
### Cuda and Cudnn install
La commande ci-dessous va renvoyer la version à utiliser dans la comande : nvidia-driver-version
```
$ sudo apt-get purge nvidia*
```

```
$ sudo add-apt-repository ppa:graphics-drivers
$ sudo apt-get update
$ sudo apt-get install nvidia-utils-430
```
```
sudo apt-get install nvidia-driver-418
```

Pour cuda:
```
sudo wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-repo-ubuntu1804_10.0.130-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1804_10.0.130-1_amd64.deb
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
sudo apt-get update
```

```
sudo apt-get install cuda-10-0
```

Pour  la partie Cudnn:
```
sudo wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
sudo apt install ./nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
sudo apt-get update
```

```
sudo apt-get install libcudnn7
sudo apt-get install libcudnn7-dev
```
 [codeanywhere](https://codeanywhere.com/editor/#)
 
#### Tensofrflow 1.9.0:

```
$ pip install tensorflow-gpu==1.9.0 
```

Si cela ne marche pas on installe: 
```
$ pip install tensorflow-gpu
```

#### fine-tunning-deeplearning
```
sudo pip3 install virtualenv 

sudo apt update

sudo apt-get install opencv-python

pip3 install keras

pip3 install imutils

pip3 install sklearn

pip3 install scikit-video

apt-get install python-tk

```
#### data_preparation
```
sudo apt install ffmpeg

sudo apt-get install python3-matplotlib

pip3 install moviepy

pip3 install matplotlib

pip install pytest-shutil
```
#### subtitles utility
```
sudo apt-get install aegisub
```
### Some tests
```
cd /local/data/line/CubicScout/Projet_Rech/fine-tunning-deeplearning
```
```
python3 predict.py --help
```
Pour le chemin de la video pour le moment c'est en local et on doit specificier le chemin comme dans l'exemple ci-dessous:
```
python predict.py --model output/activity.model --label-bin output/lb.pickle --input example_clips/p207lise.mp4 --output output/results.mp4 --size 128 --proba 10.00
```

###launch node server
```
npm start
```


###launch ngrok server (free trial version with random URL)
Authentication:
```
ngrok authtoken 1gYNGCw1ZRgzRTMckejZJ68fbOe_3dFZJfLuA8tTseLCmjYWK
```
Launching:
```
ngrok 8989
```
Browse the "http://1a36156244a8.ngrok.io" URL with the path to the video:
```
https://394724320e20.ngrok.io/page?url=C:/Users/youne/Desktop/example_clips/p207lise
```




