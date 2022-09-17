#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import time 

import random 
from datetime import datetime
import matplotlib.pyplot as plt
import deepchem as dc
from sklearn.metrics import accuracy_score

import numpy as np
np.random.seed(456)

import  tensorflow as tf
tf.random.set_seed(456)
tf.compat.v1.disable_eager_execution()
import tensorboard

"""
The program predicts whether a given compound will be toxic. 
"""

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

# Generate tensorflow graph
d = 1024
n_hidden = 50
learning_rate = .001
n_epochs = 10
batch_size = 100
rand_placeholder = random.randrange(1, 50)
 
# define placeholders that accept minibatches of different sizes
with tf.name_scope("placeholders"):
  x = tf.compat.v1.placeholder(tf.float32, (None, d))
  y = tf.compat.v1.placeholder(tf.float32, (None,))

with tf.name_scope("hidden-layer"):
  # d = in_features, n_hidden = out_features
  W = tf.Variable(tf.random.normal((d, n_hidden)))
  b = tf.Variable(tf.random.normal((n_hidden,))) 
  x_hidden = tf.nn.relu(tf.matmul(x, W) + b)

# hidden layer with dropout
with tf.name_scope("dropout-layer"):
  x_drop = tf.nn.dropout(x_hidden, rate = 0.5, seed = 1)

# complete the fully connected architecture
with tf.name_scope("output"):
  W = tf.Variable(tf.random.normal((n_hidden, 1)))
  b = tf.Variable(tf.random.normal((1,)))
  y_logit = tf.matmul(x_drop, W) + b

  # the sigmoid gives the class probability of 1
  y_one_prob = tf.sigmoid(y_logit)

  # Rounding P(y=1) will give the correct Prediction
  y_pred = tf.round(y_one_prob)

with tf.name_scope("loss"):
  # Compute the cross-entropy term for each datapoint
  y_expand = tf.expand_dims(y, 1)
  entropy = tf.nn.sigmoid_cross_entropy_with_logits(logits=y_logit, labels=y_expand)
  # Sum all contributions
  l = tf.reduce_sum(entropy)

with tf.name_scope("optim"):
  train_op = tf.compat.v1.train.AdamOptimizer(learning_rate).minimize(l)

with tf.compat.v1.Session() as sess:

  step = 0
  N = train_X.shape[0]
  sess.run(tf.compat.v1.global_variables_initializer())
  train_writer = tf.compat.v1.summary.FileWriter("/tmp/fcnet-tox21-final", sess.graph)
  tf.compat.v1.summary.scalar("loss", l)
  merged = tf.compat.v1.summary.merge_all()

  for epoch in range(n_epochs):
    pos = 0

    while pos < N:
      batch_X = train_X[pos:pos+batch_size]
      batch_y = train_y[pos:pos+batch_size]
      feed_dict = {x: batch_X, y: batch_y}

      _, summary, loss = sess.run([train_op, merged, l], feed_dict=feed_dict)
      train_writer.add_summary(summary, step)
      print("epoch %d, step %d, loss: %f" % (epoch, step, loss))

      step += 1
      pos += batch_size

  # make predictions
  valid_y_pred = sess.run(y_pred, feed_dict={x: valid_X})

# events out
# dir \tmp\fcnet-tox21-final

# model and loss graphs
# tensorboard --logdir=/tmp/fcnet-tox21-final
