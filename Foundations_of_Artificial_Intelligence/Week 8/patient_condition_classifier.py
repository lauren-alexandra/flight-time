import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

import pandas as pd
import numpy as np

from sklearn import preprocessing
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.data import Dataset
from tensorflow.keras import losses
from tensorflow.keras.layers import Dense, InputLayer, Activation
from tensorflow.keras.models import Sequential

"""### Load and read the data"""

# load user data from text file 

def get_user_data():
  response_file = open('user_data.txt', 'r')
  user_data = []

  while True:
      # Get next line from file
      res = response_file.readline()

      if (res != ''):
          res = res.strip().upper()
          if (res == 'Y'):
            res = 1
          else:
            res = 0
          user_data.append(res)
      else:
          break
  
  response_file.close()

  return user_data

user_data = get_user_data() 
user_data = np.array([user_data])

data = pd.read_csv("mayo_clinic_data.csv")
data.head()

data['TYPE'].unique()

data.columns

data.shape

label_encoder = preprocessing.LabelEncoder()
 
# Encode labels in column 'TYPE'.
data['TYPE']= label_encoder.fit_transform(data['TYPE'])
 
data['TYPE'].unique()

labels = data['TYPE']
labels

data.drop(['TYPE'], axis=1, inplace=True)
features = data
features.head()

"""### Data Split"""

SEED = 100

X = features

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

AUTOTUNE = tf.data.AUTOTUNE
BATCH_SIZE = 32
BUFFER_SIZE = 2000

train_numeric_ds = Dataset.from_tensor_slices((X_train, y_train))

train_numeric_ds = train_numeric_ds.batch(BATCH_SIZE).shuffle(BUFFER_SIZE).prefetch(AUTOTUNE)

# val dataset
val_numeric_ds = Dataset.from_tensor_slices((X_validation, y_validation))
val_numeric_ds = val_numeric_ds.batch(BATCH_SIZE).shuffle(BUFFER_SIZE).prefetch(AUTOTUNE)

# test dataset 
test_numeric_ds = Dataset.from_tensor_slices((X_test, y_test))
test_numeric_ds = test_numeric_ds.batch(BATCH_SIZE).shuffle(BUFFER_SIZE).prefetch(AUTOTUNE)

print(train_numeric_ds.element_spec)

"""### Modelling"""

model = Sequential([
                    InputLayer(input_shape=X_train.shape[1:]),
                    Dense(300, activation='relu'),
                    Dense(100, activation='relu'),
                    Dense(4, activation="softmax") # 4 neurons, 1 per class
                  ]) 

model.compile(
    loss=losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer='sgd',
    metrics=['accuracy'])

history = model.fit(
    train_numeric_ds, validation_data=val_numeric_ds, epochs=10)

print(model.summary())

model_loss, model_accuracy = model.evaluate(test_numeric_ds)

print("Model accuracy: {:2.2%}".format(model_accuracy))

"""### Run inference on new data"""

CONDITION = {
    0: 'ALLERGY',
    1: 'COLD',
    2: 'COVID',
    3: 'FLU'
}

"""
A function to find the label with the maximum score.
"""
class_values = tf.constant([0, 1, 2, 3])

def get_label(user_input):
  predicted_scores_batch = model.predict(user_input)
  predicted_int_labels = tf.argmax(predicted_scores_batch, axis=1)
  predicted_labels = tf.gather(class_values, predicted_int_labels)
  return predicted_labels

"""
Now, the model can take user input (symptoms) and predict a score for each label using Model.predict. 
"""

predicted_condition = get_label(user_data)
patient_prediction = predicted_condition[0].numpy()