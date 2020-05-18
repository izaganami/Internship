import os
import argparse
from pathlib import Path


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--videos", required=True, help="absolute path to videos folder")
ap.add_argument("-s", "--subtitles", required=True, help="absolute path to subtitles folder")
ap.add_argument("-o", "--output", required=True, help="absolute path to output folder")
ap.add_argument("-e", "--epoch", type=int, default=50, help="number of epochs to train the model on")
ap.add_argument("-mf", "--maxframe", type=int, default=15, help="maximum number of frames to keep for each event (default is 15). This is to make sure the training data stays homogenous")
args = vars(ap.parse_args())

print("[INFO] Phase 0 : Conversion srt --> json")
json_output = args['output']+"/json"
Path(json_output).mkdir(parents=True, exist_ok=True)

for (dirpath, dirnames, filenames) in os.walk(args['subtitles']):
    for filename in filenames:
        cmd = "python3 data_preparation/utils/json_subtitles_converter.py -i "+os.path.join(dirpath,filename)+" -o "+json_output
        print('--> converting '+filename)
        os.system(cmd)

print("[INFO] Phase 1 : Frame extraction")
cmd = "python data_preparation/data_formatting/data_formatting_train_set.py -o "+args['output'] + " -v " + args['videos'] + " -j " + json_output
os.system(cmd)

print("[INFO] Phase 2 : Reducing training data size")
cmd = "python3 data_preparation/utils/max_frame_per_event.py -p "+args['output']+"/output/ "+"-mf "+str(args['maxframe'])
os.system(cmd)

print("[INFO] Phase 3 : Sorting frames in directories")
cmd = "python3 data_preparation/utils/tri_training_data.py -s "+args['output']+"/output/frames_max_15"+" -d "+args['output']+"/output/frames_triees"
os.system(cmd)

print("[INFO] Phase 4 : Training")
cmd = "python3 CNN_model_fine_tuning/main.py --dataset "+args['output']+"/output/frames_triees --model "+args['output']+"/output/fig_recognition.model --label-bin "+args['output']+"/output/fig_recognition.pickle --epochs "+str(args['epoch'])
os.system(cmd)
