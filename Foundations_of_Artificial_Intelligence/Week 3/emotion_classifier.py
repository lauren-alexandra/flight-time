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
- emotions: class label
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

"""### Load and read the data"""

train_path = "data/emotion_train.txt"
test_path = "data/emotion_test.txt"
val_path = "data/emotion_val.txt"

data = pd.read_csv(train_path, sep=";", header=None, names=['text', 'emotion'],
                               engine="python")
data.emotion.unique()

data.head()

data.count()

# label_encoder object knows how to understand word labels.
label_encoder = preprocessing.LabelEncoder()
 
# Encode labels in column 'emotion'.
data['emotion']= label_encoder.fit_transform(data['emotion'])
 
data['emotion'].unique()

text = data.text
labels = data.emotion
data.head()

"""### Data Split"""

SEED = 100

X = data['text']
labels = data['emotion']

# create training and validation sets with 80-20 split
X_train, X_validation, y_train, y_validation = train_test_split(X, labels, test_size=0.2, random_state = SEED)

# split the validation sets to get a holdout dataset (for testing) 50-50 split
X_validation, X_test, y_validation, y_test = train_test_split(X_validation, y_validation, test_size=0.5, random_state = SEED)

print(X_train.shape)
print(X_validation.shape)
print(y_train.shape)
print(y_validation.shape)
print(X_test.shape)
print(y_test.shape)

"""### Prepare data for training"""

"""
If you want to apply tf.data transformations to a DataFrame of a uniform dtype, the Dataset.from_tensor_slices method will create a dataset 
that iterates over the rows of the DataFrame. 
Each row is initially a vector of values. 
To train a model, you need (inputs, labels) pairs.
"""

AUTOTUNE = tf.data.AUTOTUNE
BATCH_SIZE = 32
BUFFER_SIZE = 2000

# train dataset
train_numeric_ds = Dataset.from_tensor_slices((X_train, y_train))

# in tensorflow it is expected that you pass batches. tf.keras models are optimized to make predictions on a batch, or collection, of examples at once. 
# in this case, batches of (text, emotion) pairs
# also shuffle the data for training 
# prefetch overlaps data preprocessing and model execution while training
train_numeric_ds = train_numeric_ds.batch(BATCH_SIZE).shuffle(BUFFER_SIZE).prefetch(AUTOTUNE)

# val dataset
val_numeric_ds = Dataset.from_tensor_slices((X_validation, y_validation))
val_numeric_ds = val_numeric_ds.batch(BATCH_SIZE).shuffle(BUFFER_SIZE).prefetch(AUTOTUNE)

# test dataset 
test_numeric_ds = Dataset.from_tensor_slices((X_test, y_test))
test_numeric_ds = test_numeric_ds.batch(BATCH_SIZE).shuffle(BUFFER_SIZE).prefetch(AUTOTUNE)

print(train_numeric_ds.element_spec)

for text, emotion in train_numeric_ds.take(1):
    print("Sentence: ", text.numpy())
    print("Label:", emotion.numpy())

"""### Vectorize"""

VOCAB_SIZE = 1000

binary_vectorize_layer = TextVectorization(
    max_tokens=VOCAB_SIZE,
    output_mode='binary')

binary_vectorize_layer.adapt(train_numeric_ds.map(lambda text, labels: text))

def binary_vectorize_text(text, label):
  text = tf.expand_dims(text, -1)
  return binary_vectorize_layer(text), label

# apply the TextVectorization layers you created earlier to the training, validation, and test sets:

binary_train_ds = train_numeric_ds.map(binary_vectorize_text)
binary_val_ds = val_numeric_ds.map(binary_vectorize_text)
binary_test_ds = test_numeric_ds.map(binary_vectorize_text)

"""### Modelling"""

binary_model = Sequential([Dense(6)]) # param passed is the number of labels + 1

binary_model.compile(
    loss=losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer='adam',
    metrics=['accuracy'])

history = binary_model.fit(
    binary_train_ds, validation_data=binary_val_ds, epochs=10)

print("Linear model on binary vectorized data:")
print(binary_model.summary())

binary_loss, binary_accuracy = binary_model.evaluate(binary_test_ds)

print("Binary model accuracy: {:2.2%}".format(binary_accuracy))

"""### Model Export"""

"""
You applied tf.keras.layers.TextVectorization to the dataset before feeding text to the model. 

To make the model capable of processing raw strings (for example, to simplify deploying it), you include the TextVectorization layer inside the model.
Create a new model using the weights you have just trained:
"""

export_model = Sequential(
    [binary_vectorize_layer, binary_model,
     Activation('sigmoid')])

export_model.compile(
    loss=losses.SparseCategoricalCrossentropy(from_logits=False),
    optimizer='adam',
    metrics=['accuracy'])

# Test it with `test_numeric_ds`, which yields raw strings
loss, accuracy = export_model.evaluate(test_numeric_ds)
print("Accuracy: {:2.2%}".format(binary_accuracy))

"""
A function to find the label with the maximum score.
"""
class_values = tf.constant([0, 1, 2, 3, 4, 5])

def get_string_labels(predicted_scores_batch):
  predicted_int_labels = tf.argmax(predicted_scores_batch, axis=1)
  predicted_labels = tf.gather(class_values, predicted_int_labels)
  return predicted_labels

"""### Run inference on new data"""

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
Now, the model can take raw strings as input and predict a score for each label using Model.predict. 
"""

inputs = [
    "i can't escape the tears after the loss of my pet", 
    "i am ever feeling nostalgic about the house"
]
predicted_scores = export_model.predict(inputs)
predicted_labels = get_string_labels(predicted_scores)
for input, label in zip(inputs, predicted_labels):
  print("User text: ", input)
  print("Predicted label: ", EMOTIONS[label.numpy()])

if __name__ == "__main__" : 
    #get_user_input()
    print("it ran.")