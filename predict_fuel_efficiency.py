#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals    
import pathlib    
import matplotlib.pyplot as plt  
import numpy as np  
import pandas as pd  
import seaborn as sns

import tensorflow as tf    
from tensorflow import keras  
from tensorflow.keras import layers    
print(tf.__version__)

import tensorflow_docs as tfdocs  
import tensorflow_docs.plots  
import tensorflow_docs.modeling

"""
The program builds a model to predict the fuel efficiency of late-1970s and early-1980s automobiles. 
"""

dataset_path = keras.utils.get_file("auto-mpg.data", "http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data")
print(dataset_path)

column_names = ['MPG','Cylinders','Displacement','Horsepower','Weight','Acceleration', 'Model Year', 'Origin']
raw_dataset = pd.read_csv(dataset_path, names=column_names, na_values = "?", comment='\t', sep=" ", skipinitialspace=True)
dataset = raw_dataset.copy()
dataset = dataset.dropna()
print(dataset.tail())

train_dataset = dataset.sample(frac=0.8,random_state=0)  
test_dataset = dataset.drop(train_dataset.index)

def create_pairplot(): 
    sns.pairplot(train_dataset[["MPG", "Cylinders", "Displacement", "Weight"]], diag_kind="kde")
    plt.savefig('pairplot.png')

create_pairplot()

train_stats = train_dataset.describe()  
train_stats.pop("MPG")  
train_stats = train_stats.transpose()  
print(train_stats)

# split features from labels
train_features = train_dataset.copy()
test_features = test_dataset.copy()

train_labels = train_features.pop('MPG')
test_labels = test_features.pop('MPG')

# normalize the data
normalizer = layers.Normalization(input_shape=[1,], axis=None)
normalizer.adapt(np.array(train_features))

# build model
def build_model():    
  model = keras.Sequential([    
        tf.keras.layers.InputLayer(input_shape=[len(train_dataset.keys()) - 1]),
        normalizer,
        layers.Dense(64, activation='relu'),      
        layers.Dense(64, activation='relu'),      
        layers.Dense(1)    
      ])      
  optimizer = tf.keras.optimizers.RMSprop(0.001)      
  model.compile(loss='mse', optimizer=optimizer, metrics=['mae', 'mse'])    
  return model  

model = build_model()

EPOCHS = 1000    
history = model.fit(    
    train_features, 
    train_labels,    
    epochs=EPOCHS, 
    validation_split = 0.2, 
    verbose=0,
    callbacks=[tfdocs.modeling.EpochDots()])

print(model.summary())

# the model's training progress using the stats stored in the history object
hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
print(hist.tail())

def plot_hist_tail(history):
    plt.figure()
    plotter = tfdocs.plots.HistoryPlotter(smoothing_std=2)   
    plotter.plot({'Basic': history}, metric = "mae")  
    plt.ylim([0, 10])  
    plt.ylabel('MAE [MPG]')
    plt.savefig('tail_history.png')
    plt.show()

plot_hist_tail(history)

def plot_history(history):
    plt.figure()
    plotter = tfdocs.plots.HistoryPlotter(smoothing_std=2)  
    plotter.plot({'Basic': history}, metric = "mse")  
    plt.ylim([0, 20])  
    plt.ylabel('MSE [MPG^2]')   
    plt.savefig('history.png')
    plt.show()

plot_history(history)
