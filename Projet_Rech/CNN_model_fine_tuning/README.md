# Modèle CNN et fine-tuning
Commands to setup the environment:\
----Install python 3.7 \
----Curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py\
----Pip3 install virtualenv\
----Pip3 install tensorflow==1.15\
----Pip3 install keras\
----Pip3 install opencv-python\
----Pip3 install imutils\
----Pip3 install sklearn

\
Project structure:\
![](https://github.com/Stakhan/Projet_Recherche/blob/master/fine-tunning-deeplearning-master/output/plots/Capture.PNG)

In order to run the training process, your frames must be on a file named "Form-Type-Classifier". The script to launch this process is :\
```bash
python main.py --dataset Form-Type-Classifier/data --model output/activity.model --label-bin output/lb.pickle --epochs 50
```
As for the testing part, a folder containing the video must be created with the name "example_clips" and the script to generate a file with the subtitles for each configuration is :


```bash
python predict.py --model output/activity.model --label-bin output/lb.pickle --input example_clips/YourFileName.mp4 --output output/results.avi --size 128```

