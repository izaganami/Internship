from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, CSVLogger
from keras.layers import Dense, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential, load_model
from keras import optimizers
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from extractor import Extractor
import numpy as np
import time
import os


def extract_sequence_features(seq_length, model_extractor, sequences_folder, auth_labels):
        """
        extract frame features for each sequence
        """
        sequences = []
        labels = []
        total = len(os.listdir(sequences_folder))
        counter = 0
        for directory in os.listdir(sequences_folder):
            counter += 1
            print('Feature extraction {}/{}'.format(counter,total)) 
            if (directory.split('_')[3] in auth_labels):
                i = 0
                list_features = []
                for image_path in os.listdir(os.path.join(sequences_folder,directory)):
                    if(i < seq_length):
                        feature = model_extractor.extract(os.path.join(sequences_folder,directory,image_path))
                        list_features.append(feature)
                        i += 1
                features = np.concatenate(list_features, axis=0)
                sequences.append(features)
                labels.append(directory.split('_')[3])
        
        lb = LabelBinarizer()
        labels = np.array(lb.fit_transform(labels))
        
        #reshape for proper input
        sequences = np.array([sequence.reshape(seq_length,features_length) for sequence in sequences])
        
        return sequences,labels
        # Save the sequence.
        #np.save(path, sequence)

        
def lstm(input_shape, nb_classes):
        """Build a simple LSTM network. We pass the extracted features from
        our CNN to this model predomenently."""
        # Model.
        model = Sequential()
        model.add(LSTM(2048, return_sequences=False,
                       input_shape=input_shape,
                       dropout=0.5))
        model.add(Dense(512, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(nb_classes, activation='softmax'))

        return model

def train(data_type, seq_length, model_to_train, sequences, labels, model='lstm',
          batch_size=32, nb_epoch=1000):
    # Helper: Save the model.
    checkpointer = ModelCheckpoint(
        filepath=os.path.join('data', 'checkpoints', model + '-' + data_type + \
            '.{epoch:03d}-{val_loss:.3f}.hdf5'),
        verbose=1,
        save_best_only=True)

    # Helper: TensorBoard
    tb = TensorBoard(log_dir=os.path.join('data', 'logs', model))

    # Helper: Stop when we stop learning.
    early_stopper = EarlyStopping(patience=5)

    # Helper: Save results.
    timestamp = time.time()
    csv_logger = CSVLogger(os.path.join('data', 'logs', model + '-' + 'training-' + \
        str(timestamp) + '.log'))


    #Splitting data between train and test
    (trainX, testX, trainY, testY) = train_test_split(sequences, labels, test_size=0.30, stratify=labels, random_state=42)
    print('shape trainX:', trainX.shape)
    # Get the model.
    rm = model_to_train

    # Fit!
    # Use standard fit.
    rm.fit(
        trainX,
        trainY,
        batch_size,
        validation_data=(testX, testY),
        verbose=1,
        callbacks=[tb, early_stopper, csv_logger],
        epochs=nb_epoch)



if __name__ == '__main__':
       
        ##variable for command line
        ap = argparse.ArgumentParser()
        ap.add_argument("-d", "--dataset", required=True, help="path to input dataset")
        ap.add_argument("-m", "--pretrained-model", required=True, help="path to pretrained CNN model")
        ap.add_argument("-e", "--epochs", type=int, default=1000, help="# of epochs to train our RNN network")
        args = vars(ap.parse_args())

        auth_labels = ["F01", "F02", "F03", "F04", "F05", "F06", "F07", "F09", "F10", "F11","F12","F13","F15", "F18"]
        
        #LSTM Model imput parameters
        nb_classes = len(auth_labels)
        seq_length = 5 #WARNING : this is a number of frames so it doesn't always represent the same number of frames
        features_length = 2048
        input_shape = (seq_length, features_length)

        #LSTM Model
        model = lstm(input_shape, nb_classes)

        #loading pretrained CNN model
        if args['pretrained_model'] != None:
            model_path = args['pretrained_model']
        else:
            model_path = '../pretrained_CNN/activity.model'
        model_extractor = Extractor(model_path)
        trained_CNN_model = load_model(model_path)
        
        #Compiling the network
        metrics = ['accuracy']
        #optimizer = Adam(lr=1e-5, decay=1e-6)
        optimizer = keras.optimizers.SGD(learning_rate=0.01, momentum=0.0, nesterov=False)

        model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=metrics)

        print(model.summary())
        
        #Extracting features from CNN for further input into the RNN
        if args['dataset'] != None:
            dataset_path = args['dataset']
        else:
            dataset_path = 'frames'
        sequences,labels = extract_sequence_features(seq_length, model_extractor, dataset_path, auth_labels)
        
        # model parameters
        seq_length = 5
        nb_epoch = 1000
        data_type = 'features'
        image_shape = (224,224)
        
        #training the LSTM model
        train(data_type, seq_length, model, sequences, labels)
