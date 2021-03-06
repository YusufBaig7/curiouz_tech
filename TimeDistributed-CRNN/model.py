# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 13:00:37 2019

@author: tornado
"""
from tensorflow.keras.layers import TimeDistributed, Activation, Dense, Input, Bidirectional, LSTM, Masking, GaussianNoise
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Reshape, Flatten, Dense
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
from CTCModel import CTCModel
import pickle
from tensorflow.keras.preprocessing import sequence
import numpy as np

from read_images import prepareData

#%%
input_data = Input(shape= (144, 64, 32, 1))  #frame, height, width, channels

convolution1 = TimeDistributed(Conv2D(filters=64, kernel_size=(1,1), activation='relu'))(input_data)
bn = TimeDistributed(BatchNormalization())(convolution1)
convolution1 = TimeDistributed(Conv2D(filters=64, kernel_size=(1,1), activation='relu'))(bn)
bn = TimeDistributed(BatchNormalization())(convolution1)
pooling1 = TimeDistributed(MaxPooling2D(pool_size=(2,2)))(convolution1)

convolution2 = TimeDistributed(Conv2D(filters=128, kernel_size=(1,1), activation='relu'))(pooling1)
bn = TimeDistributed(BatchNormalization())(convolution2)
convolution2 = TimeDistributed(Conv2D(filters=128, kernel_size=(1,1), activation='relu'))(convolution2)
bn = TimeDistributed(BatchNormalization())(convolution1)
pooling2 = TimeDistributed(MaxPooling2D(pool_size=(2,2)))(bn)

convolution3 = TimeDistributed(Conv2D(filters=256, kernel_size=(1,1), activation='relu'))(pooling2)
bn = TimeDistributed(BatchNormalization())(convolution3)
convolution3 = TimeDistributed(Conv2D(filters=256, kernel_size=(1,1), activation='relu'))(convolution3)
bn = TimeDistributed(BatchNormalization())(convolution3)
pooling3 = TimeDistributed(MaxPooling2D(pool_size=(2,2)))(bn)

flatten = TimeDistributed(Flatten())(pooling3)

dense = TimeDistributed(Dense(24))(flatten)

blstm = Bidirectional(LSTM(128, return_sequences=True, dropout=0.1))(dense)
blstm = Bidirectional(LSTM(128, return_sequences=True, dropout=0.1))(blstm)
y_pred = Bidirectional(LSTM(128, return_sequences=True, dropout=0.1))(blstm)

dense = TimeDistributed(Dense(49 + 1, name="dense"))(y_pred)

Model(inputs = input_data, outputs = dense).summary()

network = CTCModel([input_data], [y_pred])
network.compile(Adam(learning_rate=0.0001))


#%%    
x_train, y_train, x_train_len, y_train_len = prepareData(r"E:\Code\Test\TimeDistributed-CRNN\Data\final.csv")

x_test_pad, y_test_pad, x_test_len, y_test_len = prepareData(r"E:\Code\Test\TimeDistributed-CRNN\Data\final.csv")

nb_labels = 49#??number of labels (10, this is digits)
batch_size = 5 # size of the batch that are considered
padding_value = 1305 #??value for padding input observations
nb_epochs = 1 # number of training epochs
nb_train = 1633
nb_test = 1633
nb_features = 64

# define a recurrent network using CTCModel
#network = create_network(nb_features, nb_labels, padding_value)

# CTC training
network.fit(x=[x_train, y_train, x_train_len, y_train_len], y=np.zeros(nb_train), \
            batch_size=batch_size, epochs=2)

#%%

network.save_model(r"E:\Code\Test\TimeDistributed-CRNN\chomu")
print(r"Saved model to disk")

# Evaluation: loss, label error rate and sequence error rate are requested
eval = network.evaluate(x=[x_test_pad, y_test_pad, x_test_len, y_test_len],\
                        batch_size=batch_size, metrics=['loss', 'ler', 'ser'])


# predict label sequences
pred = network.predict(x =[x_test_pad, x_test_len], batch_size=batch_size, max_value=padding_value)
for i in range(100):  # print the 10 first predictions
    print("Prediction :", [j for j in pred[i] if j!=-1], " -- Label : ", y_train[i]) #??