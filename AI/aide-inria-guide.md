### miniconda Installation

#### Copy the link of the most updated version of 'Python 3.8 Miniconda3 Linux 64-bit from: https://docs.conda.io/en/latest/miniconda.html

```wget the-copied-link```
```chmod 700 execName.ssh```
```bash execName.sh```

### Restart terminal.

### In case the command conda doesn't work: Path configuration to use it
```export PATH="/user/YOUR_USERNAME/home/miniconda3/bin:$PATH"```

### Create conda environment 
```conda create -n envName python=3.8```

### Activate conda environment
```conda activate envName```

### Verify you have python 3.8
```which python```
```python --version```

### Install Tensorflow
```conda install -c kitware-danesfield-df tensorflow-base```

### fine-tunning-deeplearning
```conda install virtualenv```
```pip3 install opencv-python```
```conda install keras```
```conda install -c conda-forge imutils```
```conda install scikit-learn```
```conda install -c conda-forge scikit-video```
```sudo yum install python3-tkinter```

### data_preparation
```conda install ffmpeg```
```conda install -c conda-forge moviepy```
```conda install matplotlib```
```conda install -c conda-forge pytest-shutil```

### subtitles utility
```pip3 install pysubs2```

### Test installation
```cd AI/fine-tunning-deeplearning-master```
```python main.py --help```

### Train the model
```python main.py --dataset Form-Type-Classifier/data --model output/activity.model --label-bin output/lb.pickle --epochs 50```
