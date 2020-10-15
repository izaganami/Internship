

### Git and python Install

install git from:
``` 
https://git-scm.com/download/win
```
configure your github with the command:
```
git config --global user.email youremail
git clone https://github.com/izaganami/Internship.git
cd Internship
```



Install python from:(Windows x86-64 executable installer)
```
https://www.python.org/downloads/release/python-377/
```
Verify you have the right version:
```
python3 --version
```

### Cuda and Cudnn install
Download nvidia toolkit:
```
http://developer.nvidia.com/cuda-downloads
```

Follow the steps in the windows section on this site to install the right version of cudnn:
```
https://docs.nvidia.com/deeplearning/cudnn/install-guide/index.html
```

#### Tensofrflow 1.9.0:

```
$ pip install tensorflow-gpu==1.9.0 
```

Follow the link below if you get stuck at some point:
```
https://tolotra.com/2018/07/24/how-to-install-tensorflow-gpu-1-5-0-and-1-7-and-1-8-0-on-windows-10/ 
```

#### fine-tunning-deeplearning
```
pip3 install virtualenv 

pip3 install opencv-python

pip3 install keras

pip3 install imutils

pip3 install sklearn

pip3 install scikit-video

pip3 install tk

```
#### data_preparation
```
pip install ffmpeg

pip3 install moviepy

pip3 install matplotlib

pip install pytest-shutil
```
#### subtitles utility
```
pip install pysubs2
```
### Some tests
```
cd /local/data/line/CubicScout/Projet_Rech/fine-tunning-deeplearning
```
```
python main.py --help
python main.py --dataset C:/Users/youne/Desktop/Form-Type-Classifier/data --model output/activity.model --label-bin output/lb.pickle --epochs 50
python predict.py --help
```
Check the file below for more infos:
```
Internship/AI/fine-tunning-deeplearning-master/script-to-train
```

###launch node server
follow this guide to install nodejs and npm
```
https://phoenixnap.com/kb/install-node-js-npm-on-windows
```
Launch the web-service on the Internship root:
```
npm start
```


To launch from a local server and a local file ex:
```
localhost:8989/page?url=C:/Users/youne/Desktop/example_clips/p207lise
```



