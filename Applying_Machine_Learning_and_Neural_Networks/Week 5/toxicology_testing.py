#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys
import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from itertools import product
import random 
from datetime import datetime
import matplotlib.pyplot as plt
import deepchem as dc
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

import numpy as np
np.random.seed(456)

import  tensorflow as tf
tf.random.set_seed(456)
from tensorboard.plugins.hparams import api as hp
import tensorboard

"""
The program improves the accuracy of the deep learning Tox21 model through hyperparameter tuning.
"""

# loss function 
def cross_entropy_loss(y, y_pred):
  return tf.reduce_sum(tf.nn.sigmoid_cross_entropy_with_logits(
    labels=y, logits=y_pred
  ))

# load the data 
_, (train, valid, test), _ = dc.molnet.load_tox21()
train_X, train_y, train_w = train.X, train.y, train.w
valid_X, valid_y, valid_w = valid.X, valid.y, valid.w
test_X, test_y, test_w = test.X, test.y, test.w

# remove extra tasks
train_y = train_y[:, 0]
valid_y = valid_y[:, 0]
test_y = test_y[:, 0]
train_w = train_w[:, 0]
valid_w = valid_w[:, 0]
test_w = test_w[:, 0]

# generate a TensorFlow graph using a random forest classifier 
sklearn_model = RandomForestClassifier(class_weight="balanced", n_estimators=50)

print("About to fit model on train set.")
sklearn_model.fit(train_X, train_y)

train_y_pred = sklearn_model.predict(train_X)
valid_y_pred = sklearn_model.predict(valid_X)
test_y_pred = sklearn_model.predict(test_X)

weighted_score = accuracy_score(train_y, train_y_pred, sample_weight=train_w)
print("Weighted train Classification Accuracy: %f" % weighted_score)

weighted_score = accuracy_score(valid_y, valid_y_pred, sample_weight=valid_w)
print("Weighted valid Classification Accuracy: %f" % weighted_score)

weighted_score = accuracy_score(test_y, test_y_pred, sample_weight=test_w)
print("Weighted test Classification Accuracy: %f" % weighted_score)

HP_NUM_UNITS = hp.HParam('num_units', hp.Discrete([10, 50, 100]))
HP_DROPOUT = hp.HParam('dropout', hp.RealInterval(0.1, 0.5)) 
HP_LEARNING_RATE = hp.HParam('learning_rate', hp.RealInterval(0.0001, 0.1))
HP_NUM_EPOCHS = hp.HParam('num_epochs', hp.Discrete([10, 45, 100]))
HP_BATCH_SIZE = hp.HParam('batch_size', hp.Discrete([50, 100, 200]))
METRIC_ACCURACY = 'accuracy'

with tf.summary.create_file_writer('tmp/hparam_tuning').as_default():
  hp.hparams_config(
    hparams=[HP_NUM_UNITS, HP_DROPOUT, HP_LEARNING_RATE, HP_NUM_EPOCHS, HP_BATCH_SIZE],
    metrics=[hp.Metric(METRIC_ACCURACY, display_name='Accuracy')],
  )

def train_test_model(hparams, train_X, train_y, test_X, test_y):
    d = 1024 # input features

    model = tf.keras.Sequential([
      tf.keras.layers.InputLayer(input_shape=(d,)),
      tf.keras.layers.Dense(hparams[HP_NUM_UNITS], activation=tf.nn.relu),
      tf.keras.layers.Dropout(rate=hparams[HP_DROPOUT]),
      tf.keras.layers.Dense(1)
    ])

    model.compile(
          optimizer=tf.keras.optimizers.Adam(learning_rate=hparams[HP_LEARNING_RATE]),
          loss=cross_entropy_loss,
          metrics=['accuracy'],
      )

    model.fit(train_X, train_y, batch_size=hparams[HP_BATCH_SIZE], epochs=hparams[HP_NUM_EPOCHS])
    _, accuracy = model.evaluate(test_X, test_y)
    print(f"acc: {accuracy}")
    return accuracy 

def run(run_dir, hparams, train_X, train_y, test_X, test_y):
  with tf.summary.create_file_writer(run_dir).as_default():
    hp.hparams(hparams)
    accuracy = train_test_model(hparams, train_X, train_y, test_X, test_y)
    tf.summary.scalar(METRIC_ACCURACY, accuracy, step=1)

session_num = 0

for num_units in HP_NUM_UNITS.domain.values:
  for dropout_rate in (HP_DROPOUT.domain.min_value, HP_DROPOUT.domain.max_value):
    for learning_rate in (HP_LEARNING_RATE.domain.min_value, HP_LEARNING_RATE.domain.max_value):
      for num_epochs in HP_NUM_EPOCHS.domain.values: 
        for batch_size in HP_BATCH_SIZE.domain.values: 
          hparams = {
              HP_NUM_UNITS: num_units,
              HP_DROPOUT: dropout_rate,
              HP_LEARNING_RATE: learning_rate,
              HP_NUM_EPOCHS: num_epochs,
              HP_BATCH_SIZE: batch_size,
          }
          run_name = "run-%d" % session_num
          print('--- Starting trial: %s' % run_name)
          print({h.name: hparams[h] for h in hparams})
          run('tmp/hparam_tuning/' + run_name, hparams, train_X, train_y, test_X, test_y)
          session_num += 1

# events out
# dir \tmp\hparam_tuning
# tensorboard --logdir=/tmp/hparam_tuning
