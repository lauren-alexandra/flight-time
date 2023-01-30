#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
## Emotion Classifier

A neural network-based classifier that identifies emotion in text limited to six basic emotions: anger, fear, joy, love, sadness, and surprise.

Dataset: 
https://github.com/dair-ai/emotion_dataset 

Data has been largely preprocessed already, using technique from this paper: https://www.aclweb.org/anthology/D18-1404/

Data dictionary:

- text: string 
- emotion: string
"""

import warnings
warnings.filterwarnings('ignore')

import pandas as pd

import sklearn
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.data import Dataset
from tensorflow.keras import losses
from tensorflow.keras.layers import Dense, TextVectorization, Activation
from tensorflow.keras.models import Sequential

print("\nGetting ready for you...\n")

"""### Load and read the data"""

train_path = "data/emotion_train.txt"
test_path = "data/emotion_test.txt"
val_path = "data/emotion_val.txt"

data = pd.read_csv(train_path, sep=";", header=None, names=['text', 'emotion'],
                               engine="python")

# label_encoder object knows how to understand word labels
label_encoder = preprocessing.LabelEncoder()
 
# Encode labels in column 'emotion'.
data['emotion']= label_encoder.fit_transform(data['emotion'])

text = data.text
labels = data.emotion

"""### Data Split"""

SEED = 100

X = data['text']
labels = data['emotion']

# create training and validation sets with 80-20 split
X_train, X_validation, y_train, y_validation = train_test_split(X, labels, test_size=0.2, random_state = SEED)

# split the validation sets to get a holdout dataset (for testing) 50-50 split
X_validation, X_test, y_validation, y_test = train_test_split(X_validation, y_validation, test_size=0.5, random_state = SEED)

"""### Prepare data for training"""

AUTOTUNE = tf.data.AUTOTUNE
BATCH_SIZE = 32
BUFFER_SIZE = 2000

# train dataset
train_numeric_ds = Dataset.from_tensor_slices((X_train, y_train))
train_numeric_ds = train_numeric_ds.batch(BATCH_SIZE).shuffle(BUFFER_SIZE).prefetch(AUTOTUNE)

# val dataset
val_numeric_ds = Dataset.from_tensor_slices((X_validation, y_validation))
val_numeric_ds = val_numeric_ds.batch(BATCH_SIZE).shuffle(BUFFER_SIZE).prefetch(AUTOTUNE)

# test dataset 
test_numeric_ds = Dataset.from_tensor_slices((X_test, y_test))
test_numeric_ds = test_numeric_ds.batch(BATCH_SIZE).shuffle(BUFFER_SIZE).prefetch(AUTOTUNE)

"""### Vectorize"""

VOCAB_SIZE = 1000

binary_vectorize_layer = TextVectorization(
    max_tokens=VOCAB_SIZE,
    output_mode='binary')

binary_vectorize_layer.adapt(train_numeric_ds.map(lambda text, labels: text))

def binary_vectorize_text(text, label):
  text = tf.expand_dims(text, -1)
  return binary_vectorize_layer(text), label

# apply the TextVectorization layers created earlier to the training, validation, and test sets:

binary_train_ds = train_numeric_ds.map(binary_vectorize_text)
binary_val_ds = val_numeric_ds.map(binary_vectorize_text)
binary_test_ds = test_numeric_ds.map(binary_vectorize_text)

"""### Modelling"""

print("\nBuilding emotion classifier...\n")

binary_model = Sequential([Dense(6)]) 

binary_model.compile(
    loss=losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer='adam',
    metrics=['accuracy'])

history = binary_model.fit(
    binary_train_ds, validation_data=binary_val_ds, epochs=10, verbose=0)

"""### Model Export"""

"""
To make the model capable of processing raw strings, the TextVectorization layer was included inside the model.
A new model using the weights just trained:
"""

export_model = Sequential(
    [binary_vectorize_layer, binary_model,
     Activation('sigmoid')])

export_model.compile(
    loss=losses.SparseCategoricalCrossentropy(from_logits=False),
    optimizer='adam',
    metrics=['accuracy'])

"""
A function to find the label with the maximum score.
"""
class_values = tf.constant([0, 1, 2, 3, 4, 5])

def get_string_labels(predicted_scores_batch):
  predicted_int_labels = tf.argmax(predicted_scores_batch, axis=1)
  predicted_labels = tf.gather(class_values, predicted_int_labels)
  return predicted_labels

"""### Run inference on new data"""

print("\nRunning inference...\n")

EMOTIONS = {
    # anger 
    0: "It sounds like you may be feeling angry. Perhaps going for a walk will give you clarity of mind.", 
    # fear 
    1: "It sounds like you are feeling afraid. Try to remember this: Fear is a reaction. Courage is a decision.",
    # joy 
    2: "It sounds like you’re feeling joyful. Congrats!",
    # love 
    3: "It sounds like you are feeling love. How wonderful!",
    # sadness 
    4: "It sounds like you are feeling blue. Try to remember this: we cannot cure the world of sorrows but we can choose to live in joy.", 
    # surprise
    5: "It sounds like you’re feeling…surprised!" 
}

"""
The model can take raw strings as input and predict a score for each label using Model.predict. 
"""

inputs = [
    "I can't escape the tears after the loss of my pet", 
    "I am ever feeling nostalgic about her",
    "I felt heartbroken after I found out",
    "I felt invaded and helpless in that situation",
    "I've been feeling grumpy in the past hour",
    "I feel dazed and confused by everything that happened"
]
predicted_scores = export_model.predict(inputs)
predicted_labels = get_string_labels(predicted_scores)
for input, label in zip(inputs, predicted_labels):
  print("\nUser text: ", input)
  print("Predicted feeling: ", EMOTIONS[label.numpy()])