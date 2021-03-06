import os
import numpy as np
from keras.utils import to_categorical
import librosa


class FeaturesLoader:
    def __init__(self, data_dir, labels, n_classes=15, method='mfcc', n_features=20):
        """Initialization"""
        self.data_dir = data_dir
        self.n_classes = n_classes
        self.file_names = self.__get_file_names()
        self.labels = labels
        self.method = method
        self.n_features = n_features

    def __get_file_names(self):
        file_names = os.listdir(self.data_dir)
        file_names = list(filter(lambda x: x.endswith('.wav'), file_names))

        return file_names

    def get_data(self):
        list_x = []
        list_y = []
        print('Processing ' + str(len(self.file_names)) + ' audio files')
        for counter, file_name in enumerate(self.file_names):
            if counter % 100 == 0:
                print('Processed ' + str(counter) + ' audio files out of ' + str(len(self.file_names)))
            # It will convert to mono
            data, fs = librosa.load(os.path.join(self.data_dir, file_name), sr=None)

            if self.method == 'mfcc':
                x_i = librosa.feature.mfcc(y=data, sr=fs, n_mfcc=self.n_features)
            elif self.method == 'chroma_cqt':
                x_i = librosa.feature.chroma_cqt(y=data, sr=fs, n_chroma=self.n_features)
            elif self.method == 'both':
                mfcc = librosa.feature.mfcc(y=data, sr=fs, n_mfcc=self.n_features)
                chroma = librosa.feature.chroma_cqt(y=data, sr=fs, n_chroma=self.n_features)
                x_i = np.concatenate((mfcc, chroma), axis=1)
            else:
                raise Exception('Method not recognized')

            class_name = file_name.split('-')[-1].split('.')[0]

            y_i = self.labels.index(class_name)

            list_x.append(x_i)
            list_y.append(y_i)

        x = np.stack(list_x, axis=0)
        x = x[:, :, :, np.newaxis]
        y = np.asarray(list_y)

        return x, to_categorical(y, num_classes=self.n_classes)
